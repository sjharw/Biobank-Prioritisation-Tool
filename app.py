##----- Lribraries
from configparser import ConfigParser
from flask import Flask, request, render_template, redirect
import os
from functions.calculations import Calculations, enforce_float
from functions.utils import get_json_response, nonnumeric_rows, missing_data_rows, duplicate_rows
import pandas as pd
from functools import reduce
from flask import Flask, flash, url_for
import io


##----- App

# -- Setup env from config

# Read config.ini
config = ConfigParser()
config.read("config.ini")

from functions.utils import get_path_info, get_db_info


# flask secret key
SECRET_KEY = config["USER"]["SECRETKEY"]

# Paths
ROOT_DIR, TEMP_DIR, TAXON_DIR, DB_DIR, DS_DIR, DOWNLOAD_DIR = get_path_info(config)
# SQL connection information
SERVER, USERNAME, PASSWORD, DRIVER, DB_NAME = get_db_info(config)

ALLOWED_EXTENSIONS = {"csv"}


##-- Flask app

# Create instance of flask object
app = Flask(__name__)


# Route for root page
@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    """
    Home page for app.
    """
    # config
    config = ConfigParser()
    config.read("config.ini")
    DATE = config["USER"]["date"]
    return render_template("/home.html", access_date=DATE)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Upload page.
    """
    return render_template("/upload.html")


@app.route("/upload-display", methods=["GET", "POST"])
def upload_display():
    """
    Display priority dataframe
    and scoring/ scaling filters.
    """

    if request.method == "POST":

        ##------ If user sumbits biobank csv
        if "submit" in request.form:
            # if file not given
            if not request.files["file"]:
                flash("No file uploaded")
                return render_template("/upload.html")
            file = request.files["file"]
            file_ext = file.filename.split(".", 1)[1]
            # check if file extension is permitted
            if file_ext not in ALLOWED_EXTENSIONS: 
                flash("File extension not supported, only csv files are permitted.")
                return render_template("/upload.html")
            # read in content of upload file
            contents = file.read()
            string_io = io.StringIO(contents.decode('utf-8'))
            raw_uploaded_data = pd.read_csv(string_io)
            # get column names supplied by user
            sample_column, species_column, class_column = (request.form.get(column) for column in ["sampleColumn", "speciesColumn", "classColumn"])
            uploaded_data = raw_uploaded_data.rename(columns={sample_column: "biobank_samples", species_column: "full_name", class_column: "class"})
            # error if column names arent present
            if 'full_name' not in uploaded_data.columns or 'biobank_samples' not in uploaded_data.columns or 'class' not in uploaded_data.columns:
                flash(f"Error: Column names do not match or there are missing columns from your data. Please check 'full_name', 'class' and 'biobank_samples' are in your data column names: {[col for col in raw_uploaded_data.columns]}, or that you have supplied your files column names, your previous enteries were: {species_column, class_column, sample_column}.")
                return render_template("/upload.html")
            # error if full_name or class is non-object type
            if uploaded_data['full_name'].dtype != object or uploaded_data['class'].dtype != object:
                flash(f"Error: 'full_name' or 'class' column is not string type. 'full_name' must contain strings of species names. 'class' must contain strings of species class. Please check you data and try again.")
                return render_template("/upload.html")
            # error if biobank_samples contain non-numeric data
            nonnumeric_list = nonnumeric_rows(uploaded_data, 'biobank_samples')
            if len(nonnumeric_list) > 0:
                flash(f"Error: 'biobank_samples' column type is not numeric type: {nonnumeric_list}. 'biobank_samples' must be counts of samples for each species.")
                return render_template("/upload.html")
            # warn user of missing data in their upload
            missing_indexs = missing_data_rows(uploaded_data)
            if len(missing_indexs) > 0:
                flash(f"Warning: There is missing data that will be dropped when the data is added to database, see indexes: {missing_indexs}")
            # warn user if duplicate species enteries       
            dup_fullnames = duplicate_rows(uploaded_data, 'full_name')
            if len (dup_fullnames) > 0:
                flash(f"Warning: There are duplicate species in your data which could result in data being dropped: {dup_fullnames}")
            # save uploaded file to /temp folder
            uploaded_data.to_parquet(TEMP_DIR + "uploaded_data.parquet", engine="fastparquet", index=False)   
 
        ##------ If user adds data to database
        if "add" in request.form:
            uploaded_data = pd.read_parquet(TEMP_DIR + "uploaded_data.parquet")
            # save uploaded biobank data to /temp folder, replacing old biobank data
            uploaded_data.to_parquet(TEMP_DIR + "biobank.parquet", engine="fastparquet", index=False)         
            return redirect(url_for('display')) # display data
            
    # Find uploaded names that arent present in database
    data = pd.read_parquet(TEMP_DIR + "scored_dataset.parquet")
    isin_result = uploaded_data["full_name"].isin(data["full_name"])
    unmatched = uploaded_data.loc[~isin_result, 'full_name'].tolist()
    no_unmatched = len(unmatched)

    table = [
        uploaded_data.head(500).to_html(
            classes="table bg-light shadow table-striped \ table-hover m-0 shadow sticky-top table-light"
        )
    ]

    # render HTML with home.html and return post requests
    return render_template("/add.html", unmatched=unmatched, no_unmatched=no_unmatched, tables=table)


@app.route("/display", methods=["GET", "POST"])
def display():
    """
    Display priority dataframe
    and weigthing.
    """
    
    # If biobank data not provided yet
    if not os.path.exists(TEMP_DIR + "biobank.parquet"):
        # Redirect to upload page
        return redirect(url_for('upload'))

    data = pd.read_parquet(TEMP_DIR + "scored_dataset.parquet")
    biobank_data = pd.read_parquet(TEMP_DIR + "biobank.parquet")

    # rescale biobank data
    calc = Calculations(biobank_data["biobank_samples"])
    biobank_data["biobank_samples"]= calc.invert_max()

    # add biobank data to rest of dataset
    data = reduce(
                lambda left, right: pd.merge(
                    left, right, on=["full_name", "class"], how="outer"
                ),
                [biobank_data[["full_name", "class", "biobank_samples"]], data],
            ).drop_duplicates()
    
    # enforce float type
    cols = [col for col in data.columns if col not in ["full_name", "class"]]
    for col in cols:
        data[col] = enforce_float(data[col])

    # DataTable fails is any NaN are present in dataframe, failsafe- drop any rows that contain one or more NaN values
    data = data.dropna()

    # currently combining conservation value here as approach might change in future
    data["conservation_value"] = (
        data["iucn_category"] + data["cites_listing"] + data["ed_median"]
    ) / 3
    data = data.drop(["iucn_category", "cites_listing", "ed_median"], axis=1)

    #----- Weight data
    if request.method == "POST":
        # function that applies numeric weight to column
        def apply_weight(data, column_name, weight):
            try:
                weight = int(weight or 1)  # convert to integer or default to 1
            except ValueError: # catch non-integer enteries and raise warning
                flash(f"Invalid weight value for {column_name}: '{weight}'. Please supply numeric entry only")
                return render_template("/display.html")
            data[column_name] *= weight
        # conservation weighting
        weight = request.form.get(key='conservation', default=1)
        apply_weight(data, "conservation_value", weight)
        # demand weighting
        weight = request.form.get(key='demand', default=1)
        apply_weight(data, "demand", weight)
        # biobank samples weighting
        weight = request.form.get(key='samples', default=1)
        apply_weight(data, "biobank_samples", weight)

    # create parquet of weighted data
    data.to_parquet(TEMP_DIR + "weighted_dataset.parquet", engine="fastparquet", index=False)

    # download data if download button clicked
    if "download" in request.form:
        data.to_csv(os.path.join(DOWNLOAD_DIR + "priority-scores.csv"))
        flash(f"Dataset downloaded to '/downloaded' folder")

    # get class information for filters
    classes = list(data["class"].drop_duplicates())
    classes = [x for x in classes if x is not None]
    classes.sort()

    # Send the JSON response to the DataTable via Ajax
    return render_template("/display.html", classes=classes)


@app.route("/display-data", methods=["POST", "GET"])
def display_data():
    data = pd.read_parquet(TEMP_DIR + "weighted_dataset.parquet")
    data["priority_score"] = (data[['biobank_samples', 'demand','conservation_value']].sum(axis="columns")) / 3 # calculate priority scores
    data = data.sort_values("priority_score", ascending=False)  # sort by priority score
    data = data[['full_name', 'class', 'biobank_samples', 'demand', 'conservation_value', 'priority_score', 'null_percent']] # order columns
    data = data.round(2) # round data to 2 decimal place
    result = get_json_response(json_data= request.get_json(), data = data)
    return result


# run app
if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.config["SESSION_TYPE"] = "filesystem"
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port, threaded=True)
