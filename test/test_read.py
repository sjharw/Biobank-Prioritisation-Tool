import pytest
from unittest.mock import Mock
from os.path import join


@pytest.mark.parametrize(
    "file_input, expected",
    [
        ({}, "No file uploaded"),
        ({"file": None}, "No file uploaded"),
        ({"file": Mock(filename="")}, "Filename not found"),
        ({"file": Mock(filename="example.pdf")}, "File extension not supported"),
        ({"file": Mock(filename="example.csv")}, None),
    ],
)
def test_submit(file_input, expected):
    request = Mock(form={"submit": True})
    request.files = {**file_input}
    ALLOWED_EXTENSIONS = ["csv"]
    TEMP_FOLDER = "temp"

    result = None
    if "submit" in request.form:
        if "file" in request.files and request.files["file"]:
            if request.files["file"].filename != "":
                file = request.files["file"]
                file_ext = file.filename.split(".", 1)[1]
                if file_ext not in ALLOWED_EXTENSIONS:
                    result = "File extension not supported"
                # if extension is supported
                if file_ext in ALLOWED_EXTENSIONS:
                    # save file in temp folder
                    filepath = join(
                        TEMP_FOLDER,
                        "biobank_data" + "." + file.filename.split(".", 1)[1],
                    )
                    # save file
                    file.save(filepath)
            else:
                result = "Filename not found"
        else:
            result = "No file uploaded"
    assert result == expected
