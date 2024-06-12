"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv  #install using pip install python-dotenv
from psycopg2 import sql
import psycopg2   # for using optional connector method instead of Model ORM

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# NOTE Not utilizing .env currently

class Config:
    """Flask configuration variables."""
    
    # user configurations
    dash_debug = False
    dash_auto_reload = False
    
    # General Config
    FLASK_APP = "wsgi.py"
    # FLASK_ENV = environ.get("FLASK_ENV")
    # FLASK_ENV = 'development'
    FLASK_DEBUG = False
    # FLASK_DEBUG = False

    SECRET_KEY = environ.get("SECRET_KEY")

    # Assets
    # LESS_BIN = environ.get("LESS_BIN")
    LESS_BIN = "/c/Users/hp/AppData/Roaming/npm/lessc"
    # ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True
    # LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")
    
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    # to circumvnet error due to deprected parameter, see the design.txt doc for more detail
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)  
            
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #---------------------------------------------------------------
    # 1.
    # Function for creating Tables 
    # For using optional connector method instead of Model ORM
    # NOTE: I like to use the second function as shown below
    #-----------------------------------------------------------------
    # def create_table(connection_uri, sql_statement):
    #     try:
    #         # Establish a connection to the database which is ON CLOUD
    #         with psycopg2.connect(connection_uri) as connection:
    #             # Use a cursor to execute SQL commands
    #             with connection.cursor() as cursor:
    #                 # Execute the provided SQL statement
    #                 cursor.execute(sql_statement)
    
    #         print("Table created successfully!")
    
    #     except psycopg2.Error as e:
    #         print(f"Error: {e}")
    
    # # Example usage:
    # #Candidate table
    # SQL_CREATE_TABLE_CANDIDATE = """
    #     CREATE TABLE candidate (
    #         ("candidate_id" "SERIAL PRIMARY KEY"),
    #         ("first_name", "VARCHAR(50)"),
    #         ("last_name", "VARCHAR(50)"),
    #         ("email", "VARCHAR(100) UNIQUE"),
    #         ("phone_number", "VARCHAR(20)"),
    #     );
    # """
    
    # create_table(SQLALCHEMY_DATABASE_URI, SQL_CREATE_TABLE_CANDIDATE)
 
    #-------------------------------------------------------------------------------------------------
    # 2.
    # Another Function for creating Tables 
    #
    # The sql.SQL class in the psycopg2.sql module is a class designed to help with
    #
    # SQL query construction in a way that helps prevent SQL injection attacks. It is particularly useful
    #
    # when you need to dynamically construct SQL queries by incorporating variable values.
    #--------------------------------------------------------------------------------------------------- 
    
    #-------------------
    # CANDIDATE TABLE
    #-------------------
    
#     # Define the table schema
#     table_schema = [
#     ("candidate_id", "SERIAL PRIMARY KEY"),
#     ("Name", "VARCHAR(150)"),
#     ("Address", "VARCHAR(255)"),
#     ("Telephone", "VARCHAR(20)"),
#     ("EMAIL", "VARCHAR(100) UNIQUE"),
#     ("Website", "TEXT"),
#     ("JOBTITLE", "TEXT"),
#     ("Company Name", "VARCHAR(20)"),
#     ("Years Of Experience", "INTEGER"),
#     ("Job Responsibilities", "TEXT"),
#     ("College Subject", "VARCHAR(20)"),
#     ("College Name", "VARCHAR(20)"),
#     ("Years of Study", "INTEGER"),
#     ("SKILLS", "TEXT"),
#     ("Certifications", "TEXT"),
#     ("SUMMARY", "TEXT"),
#     ("HOBBIES", "TEXT"),
#     ("Languages", "TEXT"),
#     ("Date Of Birth", "DATE"),
#     ("Marks OR Grades Obtained", "TEXT"),  # Adjusted column name to remove special characters
#     ("Linkedin Profile", "TEXT"),
#     ("First Name", "VARCHAR(50)"),
#     ("Last Name", "VARCHAR(50)")
# ]

    
#     # Function to create the Candidates table
#     def create_candidates_table(connection_uri):
#         with psycopg2.connect(connection_uri) as connection:           
#             with connection.cursor() as cursor:
#                 # Check if the table already exists
#                 cursor.execute("""
#                     SELECT EXISTS (
#                         SELECT 1
#                         FROM information_schema.tables
#                         WHERE table_name = 'Candidates'
#                     )
#                 """)
#                 table_exists = cursor.fetchone()[0]
#                 # If the table doesn't exist, create it
#                 if not table_exists:
#                     columns = [sql.SQL("{} {}").format(sql.Identifier(name), sql.SQL(type_)) for name, type_ in table_schema]
#                     query = sql.SQL("CREATE TABLE Candidates ({})").format(sql.SQL(', ').join(columns))
#                     cursor.execute(query)
#                     print("Candidates table created successfully.")
#                 else:
#                     print("Candidates table already exists.")
    
#     # Executing the above function
#     create_candidates_table(SQLALCHEMY_DATABASE_URI)

    #-------------------------------------------------------------------------------------------------
    # 3.
    # This Function :
    #    - Use the provided text and parse it to extract the column names and values.
    #    - Create a SQL table with the extracted column names.
    #    - Insert the extracted values into the SQL table.
    #
    #-------------------------------------------------------------------------------------------------
    
    # def store_text_in_sql(connection_uri, text):
    #     try:
    #         # Establish a connection to the database
    #         with psycopg2.connect(connection_uri) as connection:
    #             # Use a cursor to execute SQL commands
    #             with connection.cursor() as cursor:
    #                 # Split the input text into lines
    #                 lines = text.split('\n')
    
    #                 # Extract column names and values
    #                 columns = [line.split('<--->')[0].strip() for line in lines if '<--->' in line]
    #                 values = [line.split('<--->')[1].strip() for line in lines if '<--->' in line]
    
    #                 # Construct the CREATE TABLE statement
    #                 table_name = "Candidate"
    #                 create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
    
    #                 # Execute the CREATE TABLE statement
    #                 cursor.execute(create_table_query)
    
    #                 # Insert values into the created table
    #                 insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(values)});"
    #                 cursor.execute(insert_query)
    
    #         print("Data stored in SQL successfully!")
    
    #     except psycopg2.Error as e:
    #         print(f"Error: {e}")
    
    # # Example usage:
    # DATABASE_URI = SQLALCHEMY_DATABASE_URI
    
    # # The Text predicted by the NER Spacy Model
    # input_text = """
    # PER  <--->  Salman Awan
    # EMAIL  <--->  Salmanawan222@gmail.com
    # """
    
    # store_text_in_sql(DATABASE_URI, input_text)

    
    
    
    #-----------------------------
    # Email related configuration
    #-----------------------------
    MAIL_SERVER=environ.get("MAIL_SERVER")
    MAIL_PORT = environ.get("MAIL_PORT")
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = environ.get("MAIL_USE_TLS")
    MAIL_USE_SSL = environ.get("MAIL_USE_SSL")