# RankingETL Repository

RankingETL is a Python-based ETL (Extract, Transform, Load) application designed to process, clean, prioritize, and load business ranking data into a specified database. The application is highly modular and has a built-in web server to manage data processing.

Directory Structure
```
.
├── data
├── logs
├── src
│   ├── frontEnd
│   ├── pipeline
│   ├── server
│   ├── __init__.py
│   ├── app.py
│   ├── helpers.py
│   ├── main.py
├── systemConfig
│   └── testSystem.json
├── tests
├── README.md
└── requirements.txt
```
Components
data: Contains input and output data folders for extract and load operations.
logs: Log files generated during the ETL process.
requirements.txt: Lists required packages for the project.
src: Contains the source code for the ETL pipeline.
app.py: Application entry point.
frontEnd: Contains the code for the web-based user interface.
helpers.py: Utility functions used throughout the application.
main.py: Main script that triggers the ETL pipeline.
pipeline: ETL pipeline components, including data cleaning, extraction, loading, scoring, and transformation.
server: Code related to database connections and data insertion.
systemConfig: Contains configuration files.
tests: Test scripts and sample data for testing the ETL pipeline.
Installation
Clone the repository: 
```
git clone https://github.com/yourusername/rankingETL.git

cd rankingETL

pip install -r requirements.txt
```
Configure the `systemConfig/testSystem.json` file with your desired settings.

Run the main script: 
```
python src/main.py
```
Access the web interface at http://localhost:5000 (default) to manage data processing.
Testing