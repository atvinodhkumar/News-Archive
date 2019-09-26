# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.request import urlopen

import os
import sys
import time
import signal
import database


def signal_handler(signal, frame):
    """Interrupts the infinite loop.
    """
    global interrupted
    interrupted = True

   
def find_character(jump_to_line):
    """Executes loop to find the first character index in a given line.

    Arguments:
        jump_to_line: The line in which the first character index has to be found.

    Returns:
        The index of the first character in a given line.
    """
    for character in jump_to_line:
        if character.isalpha():
            string_index_4 = jump_to_line.index(character)
            break
    return string_index_4


def extract_title_sub_title(line, news_entries_list):
    """Extracts title and sub-title of the news in a given line.
    
    Arguments:
        line: The line in which the title and sub-title have to be extracted.
        news_entries_list: The list that is used to append news entries.

    Returns:
        The title, sub-title and news entries list which is in the line.
    """
    string_index_1 = line.index('headline-intro')
    string_index_2 = line.index('</span>') 
    string_index_3 = line.index('</span></a>')
    
    sub_title = line[string_index_1+16:string_index_2]
    title = line[string_index_2+31:string_index_3]
    
    news_entries_list.append(str(title))
    news_entries_list.append(str(sub_title))
    
    return title, sub_title, news_entries_list

    
def extract_abstract(jump_to_line, news_entries_list):
    """Extracts abstract of the news in a given line.
    
    Arguments:
        jump_to_line: The line in which the abstract have to be extracted.
        news_entries_list: The list that is used to append news entries.

    Returns:
        The abstract and news entries list which is in the line.
    """
    string_index_4 = find_character(jump_to_line)
    
    if "<" in jump_to_line:
        string_index_5 = jump_to_line.index('<')
        abstract = jump_to_line[string_index_4:string_index_5-1]
        
        news_entries_list.append(str(abstract)) 
    
    return abstract, news_entries_list
    
    
def crawler(file_path, counter):
    """Creates an HTML text file of the URL and extracts the title, sub-title, 
       abstract and download time of the various news. Also, fetchs the 
       news entry to database.

    Arguments:
        counter: Value to decide which operation to perform in the database.
    """
    
    text_file = file_path + "url_to_html_text.txt"
    
    crawl_url = urlopen("https://www.spiegel.de/international/")
    
    download_time = datetime.now().strftime("%H:%M:%S")
    
    with open(text_file, "w") as url_to_html:
        for line in crawl_url:
            line = line.decode()
            url_to_html.write(line + "\n")
    
    with open(text_file, "r") as in_text_file:
        lines_in_text_file = in_text_file.read().splitlines()
        
        for new_line in range(len(lines_in_text_file)):
            news_entries_list = []
            line = lines_in_text_file[new_line]
            
            if '<span class="headline-intro">' in line: 
                title, sub_title, news_entries_list = extract_title_sub_title(line, news_entries_list)
                
                if '<p class="article-intro">' in line:
                    jump_to_line = lines_in_text_file[new_line + 3]
                    abstract, news_entries_list = extract_abstract(jump_to_line, news_entries_list)
                    
                else:
                    string_find_loop = True
                    line_jump_incrementer = 0
                    
                    while string_find_loop:
                        line_jump_incrementer = line_jump_incrementer + 1
                        jump_to_line_1 = lines_in_text_file[new_line + line_jump_incrementer]
                        
                        if '<p class="article-intro">' in jump_to_line_1:
                            string_find_loop = False
                            jump_to_line_1 = lines_in_text_file[new_line + (line_jump_incrementer+3)]
                            abstract, news_entries_list = extract_abstract(jump_to_line_1, news_entries_list)
                            
                news_entries_list.append(str(download_time))
                database_object.compare_entries(title, sub_title, 
                                         abstract, download_time, news_entries_list, counter)

            else:
                pass
    
    
if __name__ == "__main__": 

    file_path = sys.argv[1]
    
    signal.signal(signal.SIGINT, signal_handler)
    
    interrupted = False
    
    if os.path.exists(file_path + "News_Entries.db"):
        counter = 1  
        
    else:
        counter = 0
        
    database_object = database.NewsDatabase(file_path)
    
    if counter == 0:
        database_object.create_table()
    
    while True:  
        counter = counter + 1
        crawler(file_path, counter)
        time.sleep(900)
        
        if interrupted:
            break
        
    database_object.convert_to_csv(file_path)
    database_object.close_database()
