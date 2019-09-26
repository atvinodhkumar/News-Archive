# News-Archive

To develop a news-database that is regularly updated using Python3. This code extract News-Entries (Title, Sub-Title and Abstract) with download time from HTML of the URL: [SPIEGEL-ONLINE](https://www.spiegel.de/international/ ) and stores them in a database. The database is automatically updated every 15 minutes. The updates are made with the following conditions:

* If entries are existing in the database, the duplicates should not be stored.
* For the duplicates, an additional timestamp should be stored: updated download time.


## Prerequisites

The following are the required to get the code up and running.

### Programming Language:

* [Python 3.7.1](https://www.python.org/downloads/release/python-371/ ) 

### Python Modules:

* [os — Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html )
* [sys — System-specific parameters and functions](https://docs.python.org/3/library/sys.html ) 
* [csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html )
* [time — Time access and conversions](https://docs.python.org/3/library/time.html )
* [signal — Set handlers for asynchronous events](https://docs.python.org/3/library/signal.html )
* [datetime — Basic date and time types](https://docs.python.org/3/library/datetime.html#module-datetime )
* [urllib.request — Extensible library for opening](https://docs.python.org/3/library/urllib.request.html#module-urllib.request )

### Database Module:

* [sqlite3 — DB-API 2.0 interface for SQLite databases](https://docs.python.org/3/library/sqlite3.html )

### Database Tool:

* [DB Browser for SQLite](https://sqlitebrowser.org/ ) 


## SQLite and DB Browser for SQLite

### SQLite: 

SQLite is a C library that provides a lightweight disk-based database that doesn’t require a separate server process and allows accessing the database using a nonstandard variant of the SQL query language.

### DB Browser: 

DB Browser for SQLite (DB4S) is a high quality, visual, open-source tool to create, design, and edit database files compatible with SQLite.


## Installation

Every module comes with Python3 including **sqlite3**. Only the DB Browser for SQLite tool needs to be installed. For this work, the DB Browser is used to view the database created using python. The DB Browser can be downloaded from [here](https://sqlitebrowser.org/dl/ ) for the corresponding operating system. After downloading, run it and please follow the steps displayed to get it installed in your system.

### Steps to view the database file using DB Browser

1. Open the DB Browser and select "Open Database" tab.
![Step 1](images/step1.png)

2. Find and select the database file to open it. 
![Step 2](images/step2.png)

3. Select the "Browse Data" tab which is right below the "Open Database" tab.
![Step 3](images/step3.png)


## Running the script

* Make sure that two python files, "news_entries_to_database.py" and "database.py" are in the same folder.
* Run the python file, "news_entries_to_database.py" in terminal with folder path as the command-line argument to pass it to the script.

Example of how to run the python script "news_entries_to_database.py" from terminal:

```shell
$ python news_entries_to_database.py C:\\Users\\atvin\\Desktop\\OPAX\\data\\
```


## Work-flow of the python script

The code will automatically re-run every 15 minutes in an endless loop. To stop the code and view the database file, press "CTRL+c" from the keyboard. **Please wait until the program is terminated.** This will store three files: HTML of the [URL](https://www.spiegel.de/international/ ) (*url_to_html_text.txt*) file, Database (*News_Entries.db*) file and CSV (*database_to_csv.csv*) file in that path. Once the program is terminated, the entries of the database can be viewed either from the CSV "database_to_csv.csv" file or from the database "News_Entries.db" file using DB Browser.
