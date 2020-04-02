#!/bin/sh

#  PostGresConnect.py
#  
#
#  Created by Rishi Patel on 3/28/20.
#  



import psycopg2
import sys
import pandas as pd
import csv
try:
    connection = psycopg2.connect(user = "%s"%sys.argv[1],
                                  password = "%s" %sys.argv[2],
                                  host = "%s" %sys.argv[3],
                                  port = "5432",
                                  database = "%s" %sys.argv[4])

    cursor = connection.cursor()
    
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
    df=pd.read_csv('CORD-19-research-challenge/metadata.csv', low_memory=False)
    listOfColumns=["sha","source_x","title","doi","pmcid","pubmed_id","license","abstract","publish_time","authors","journal","\"Microsoft Academic Paper\"","\"WHO #Covidence\"","has_full_text","full_text_file"]
    tablequery='\'\'\'CREATE TABLE CORD19('
    #for c in listOfColumns:
    #    tablequery=tablequery+c+" VARCHAR, "
    #tablequery=tablequery+');\'\'\''
    #print(tablequery)
    #tablequery='''CREATE TABLE CORD19(sha VARCHAR, source_x VARCHAR, title VARCHAR, doi VARCHAR, pmcid VARCHAR, pubmed_id VARCHAR, license VARCHAR, abstract VARCHAR, publish_time VARCHAR, authors VARCHAR, journal VARCHAR, "Microsoft Academic Paper" VARCHAR, \"WHO #Covidence\" VARCHAR, has_full_text VARCHAR, full_text_file VARCHAR );'''
    #cursor.execute(tablequery)
    #connection.commit()
    #print("Table created successfully in PostgreSQL ")
    #upload="\copy CORD19 FROM '/Users/rishipatel/ProjectStorage/AWS/CORD-19-research-challenge/metadata.csv' CSV"
    #HAVE TO USE PSQL: psql --host=rpatelaws.cjx53qyzsxyc.us-east-2.rds.amazonaws.com --port=5432 --username=rpatel --password --dbname=postgres then copy
    #print(upload)
    #cursor.execute(upload)
    postgreSQL_select_Query = "select * from CORD19 WHERE has_full_text iLike 'True' "
    cursor.execute(postgreSQL_select_Query)
    FullText_records = cursor.fetchall()
    #f = open(, 'w')
    #with open('/Users/rishipatel/ProjectStorage/AWS/CORD-19-research-challenge/FilteredCSV.csv', mode='w') as Filtered_file:
        #writer = csv.DictWriter(Filtered_file, fieldnames=listOfColumns)
        #writer = csv.writer('FilteredCSV.csv',mode='w',fieldnames=listOfColumns)
        #writer.writeheader()
    for row in FullText_records:
        print(row)
        #writer.writerow(row)
    #create_table_query();
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
