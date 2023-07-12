import sqlalchemy
from sqlalchemy.engine import URL


def db_conn(driver, server, database, username: str = "", password: str = ""):
    """
    Creates connection to Microsoft Server SQL database.

    Parameters:
        driver (str): ODBC Driver to use for connection.
        server (str): Microsoft Server name to connect to.
        database (str): Microsoft SQL database to connect to.
        username (str, optional): Microsoft SQL server username. Defaults to an empty string.
        password (str, optional): Microsoft SQL server password. Defaults to an empty string.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine instance to interact with the database.

    Raises:
        Exception: If sqlalchemy fails to connect to database.

    """
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string}
    )
    engine = sqlalchemy.create_engine(connection_url)
    # check engine has connected correctly
    try:
        with engine.connect() as con:
            con.execute("SELECT 1")
        print("SQL engine is valid")
    except Exception as e:
        print(f"SQL engine invalid: {str(e)}")
    return engine
