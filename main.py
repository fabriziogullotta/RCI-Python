#!/usr/bin/env python3
import csv
import sys
import sqlite3
import re
import json

line_counter = 0
delimiter = ""
db_name = ""
table_name = ""
cols = ""
column_headers = []
table_created = False;

while len(db_name) <= 0:
	db_name = input('Enter DB name: ')

while len(table_name) <= 0:
	table_name = input('Enter Table name: ')

# while len(delimiter) <= 0 :
# 	delimiter = input('Enter delimiter: ')

conn = sqlite3.connect(db_name+".sqlite")
cur = conn.cursor()

sql_drop = "DROP TABLE IF EXISTS {}".format(table_name)

cur.executescript(sql_drop)

def is_float(string):
	try:
		float(string)
		return True
	except:
		return False

def column_type(col):
	if isinstance(col,int):
		return "INTEGER"
	elif col.isdigit():
		return "INTEGER"
	elif isinstance(col,float):
		return "REAL"
	elif is_float(col):
		return "REAL"
	elif col.upper() =="TRUE" or col.upper() == "FALSE":
		return "INTEGER"
	else:
		return "TEXT"

with open(sys.argv[1], 'r') as csvfile:
	data_reader = csv.DictReader(csvfile)
	for line in data_reader:
		if line_counter == 0:
			column_headers = list(line.keys())
		else:
			insert_values = ""
			columns = ""
			for key,value in line.items():
				insert_values += '"'+value+'",'
				columns += key+","
			insert_values = insert_values[:-1]
			columns = columns[:-1]
			if not table_created:
				if "" not in line.values():
					cols = "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE"
					for key,value in line.items():
						column_type_name = column_type(value)
						cols += ","+ key + " " + column_type_name
					sql_create = "CREATE TABLE {} ({})".format(table_name,cols)
					cur.executescript(sql_create);
					table_created = True
			sql_insert = "INSERT OR IGNORE INTO {} ({})VALUES ({})".format(table_name,columns,insert_values)
			print(sql_insert)
			cur.executescript(sql_insert)
			conn.commit()
		line_counter += 1