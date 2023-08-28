#!/usr/bin/env python3
import sqlite3
import matplotlib.pyplot as plt

def create_connection(db_name):
	conn = None
	try:
		conn = sqlite3.connect(db_name)
	except Exception as e:
		print(e)
	return conn

def select_all(conn,table_name):
	result = []
	cur = conn.cursor()
	sql_select = "SELECT * FROM {}".format(table_name)
	cur.execute(sql_select)
	rows = cur.fetchall()
	columns = [col[0] for col in cur.description]
	dictionary = [dict(zip(columns,row)) for row in rows]
	return dictionary

def visualize(data):
	users = []
	progresses = []
	filename = ""
	for elem in data:
		users.append(elem['first_name'])
		progresses.append(elem['progress'])
	plt.figure(figsize=(15,8))
	plt.bar(users,progresses)
	plt.title("Progress per User")
	plt.xlabel('Users')
	plt.ylabel('Progress %')
	while len(filename) <= 0:
		filename = input('Save as: ')
	plt.tight_layout()
	plt.savefig(filename, format="pdf")

def main():
	db_name = ""
	table_name = ""
	data = []
	while len(db_name) <= 0:
		db_name = input('Enter DB name: ')
	while len(table_name) <= 0:
		table_name = input('Enter Table name: ')
	conn = create_connection(db_name+".sqlite")
	with conn:
		data = select_all(conn,table_name)
		visualize(data)

if __name__ == '__main__':
    main()
