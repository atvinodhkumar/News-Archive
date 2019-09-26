# -*- coding: utf-8 -*-

import csv
import sqlite3


class NewsDatabase:
    """Creates a database along with functions to insert, compare, update 
       in a database as well as convert the database to CSV file.
    """
    def __init__(self, file_path):
        self.conn = sqlite3.connect(file_path + "News_Entries.db")

    def create_table(self):
        """Creates a table in the database file.
        """
        try:
            self.conn.execute('''CREATE TABLE NewsEntries
                     (Title          TEXT     NOT NULL,
                      SubTitle       TEXT     NOT NULL,
                      Abstract       TEXT     NOT NULL,
                      DownloadTime   TEXT     NOT NULL);''')
        except:
            pass

    def database_empty(self):
        """Checks if the database is empty.
           
        Returns:
            A bool value indicating if the database is empty or not.
        """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT COUNT(*) from NewsEntries ''')
        table_contents = cursor.fetchall()
            
        if table_contents[0][0] == 0:
            empty = True
        else:
            empty = False
                
        return empty 

    def news_entry(self, title, sub_title, abstract, download_time):
        """Makes a news entry in the database.
        
        Arguments:
            title: Title of the news.
            sub_title: Sub-title of the news.
            abstract: Abstract of the news.
            download_time: Downloaded time of the news.
        """
        self.conn.execute("INSERT INTO NewsEntries (Title, SubTitle, Abstract, DownloadTime) VALUES (?, ?, ?, ?)",
                          (title, sub_title, abstract, download_time))
    
        self.conn.commit()

    def update_timestamp(self, download_time, news_title):
        """Updates a particular content in the database.

        Arguments:
            download_time: Time to be updated.
            news_title: Time to be updated for a particular content in the database.
        """
        self.conn.execute('''UPDATE NewsEntries SET DownloadTime = ? WHERE Title = ?''',
                          (download_time, news_title))
        self.conn.commit()

    def compare_entries(self, title, sub_title, abstract, download_time, news_entries_list, counter):
        """Compares the entries of the database.
        
        Arguments:
            title: Title of the news.
            sub_title: Sub-title of the news.
            abstract: Abstract of the news.
            download_time: Downloaded time of the news.
            news_entries_list: The list which has above four entries of the news.
            counter: Value to decide which operation to perform in the database.
        """
        if self.database_empty() or counter == 1:
            self.news_entry(title, sub_title, abstract, download_time)
        
        elif counter != 1:
            cursor = self.conn.execute("SELECT Title, SubTitle, Abstract, DownloadTime from NewsEntries")
            existing_news_entries_list = []
            
            for row in cursor:
                existing_news_entries_list.append(row[0])
            
            news_title = news_entries_list[0]
            
            if news_title in existing_news_entries_list:
                self.update_timestamp(download_time, news_title)
            else:
                self.news_entry(title, sub_title, abstract, download_time)
                
        else:
            pass

    def convert_to_csv(self, file_path):
        """Converts the contents of the database to a CSV file.
        """
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT Title, SubTitle, Abstract, DownloadTime from NewsEntries")
        
        with open(file_path + "database_to_csv.csv", "w", newline='') as csv_file:   
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([row[0] for row in cursor.description]) 
            csv_writer.writerows(cursor)

    def close_database(self):
        """Closes the database.
        """
        self.conn.close()
