#!/usr/bin/python
#------------------------------------------------
# Script name: sqlitedbtest1.py
#
# source    https://gist.github.com/richardschoen/408fd42aaa6769dfd47f175dc9408b53
#
#
# Description: 
# This script is a good test program for SQLite DB
# functionality.
#
# Parameters:
# P1=
# P2=
# p3=
# 
# Notes/reference links:
#https://www.sqlitetutorial.net/sqlite-python/
#https://www.sqlitetutorial.net/sqlite-python/create-tables/
#https://stackabuse.com/python-modules-creating-importing-and-sharing/
#
# Environment setup:
# pip install --upgrade pysqlite
# pip install --upgrade pysqlite3-binary
# pip install --upgrade pysqlite3
#------------------------------------------------

#------------------------------------------------
# Imports
#------------------------------------------------
import sqlite3
from sqlite3 import Error
import sys
import datetime
import traceback

#---------------------------------------------------
# Now let's define a couple of functions for SQLite DB access
#---------------------------------------------------
def create_connection(db_file):
	#-------------------------------------------------------
	""" Create a database connection to a SQLite database 
	:param db_file: SQLite database file name/path
	:return: Connection or None on error. 
	"""
	#-------------------------------------------------------

	conn = None

	# Let's try and open the database. Will auto-create if not found and written to disk
	try:
		conn = sqlite3.connect(db_file)			
		# print("sqlite3 version:         ",sqlite3.version) #pyselite version
		# print("sqlite engine version:   ",sqlite3.sqlite_version) #SQLLite engine version
		return conn;
	except Error as e:
		print(e)
		return None

def close_connection(db_file):
	#-------------------------------------------------------
	""" Close a database connection to a SQLite database 
	:param conn: Connection object
	:return: True-Success, False-Error
	"""
	#-------------------------------------------------------
	
	# Let's attempt to close our database connection 
	try:
		sqlite3.connect(db_file).close()
		return True;
	except Error as e:
		print(e)
		return False

def create_table(conn, create_table_sql):
	#----------------------------------------------------------
	""" create a table with pre-defined columns from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return: True-Success, False-Error
	"""
	# and without 'commit' written to disk
   
	 #----------------------------------------------------------
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
		return True
	except Error as e:
		print(e)  
		return False

def add_column(conn, create_col_row_sql):
	# pass
	#
	#----------------------------------------------------------
	""" create a new column and fill row cell from the create_create_col_row_sql statement
	:param conn: Connection object
	:param create_col_row_sql: a ALTER TABLE ADD COLUMN statement
	:return: True-Success, False-Error
	"""
	#----------------------------------------------------------
	
	try:
		c = conn.cursor()
		c.execute(create_col_row_sql)
		return True
	except Error as e:
		print(e)
		return False

# def data_entry(conn, entry_values_sql, element, value):
def data_entry(conn, entry_data_sql):
	#
	#----------------------------------------------------------
	""" fill row cells xy_sql statement
	:param conn: Connection object
	:param data_entry_sql: insert data statement
	:param mi_ev_ mediainfo element - value
	:return: True-Success, False-Error
	"""
	# an additional 'xy.db-journal' written to disk, original 'xy.db' not touched
	#----------------------------------------------------------
	
	try:
		c = conn.cursor()
		c.execute(entry_data_sql)
		
		return True
	except Error as e:
		print(e)
		return False
	
def execute(conn, sql):
	#----------------------------------------------------------
	""" Execute an SQL action query that does not return results
	:param conn: Connection object
	:param sql: SQL action query
	:return: True-Success, False-Error
	"""
	 #----------------------------------------------------------
	try:
		c = conn.cursor()
		c.execute(sql)
		return True
	except Error as e:
		print(e)  
		return False

def execute_query(conn, sql):
	#----------------------------------------------------------
	""" Execute an SQL query that does return results
	:param conn: Connection object
	:param sql: SQL query expecting results
	:return: Resulting cursor or None
	"""
	 #----------------------------------------------------------
	try:
		c = conn.cursor()
		c.execute(sql)
		return c
	except Error as e:
		print(e)  
		return None

def comm(conn, db_file):

	#conn = None

	try:
		#sqlite3.connect(db_file).commit()
		#conn = sqlite3.connect(db_file)
		#c = conn.cursor()
		conn.commit()			# 'xy.db-journal' deleted and original 'xy.db' updated (higher file size)
		return True
	except Error as e:
		print(e)
		return False


#------------------------------------------------
# Program level variables
#------------------------------------------------
dashes="--------------------------------------------------"

#---------------------------------------------------
# This is the main program
#			!!!		original source, not used here in 'mi2sqlite'	!!!
#---------------------------------------------------
if __name__ == '__main__':

	#------------------------------------------------
	# Main script logic
	#------------------------------------------------
	try: # Try to perform main logic

	#Output messages to STDOUT for logging
		begintime=datetime.datetime.now()
		print("Start of Main Processing - " + str(begintime.strftime("%H:%M:%S")))

	#define work variables
		# dbfile = r"C:\rjstemp\pythonsqlite3.db" # with r, don't need double \\
		dbfile = "pythonsqlite3.db" # with r, don't need double \\
	#dbfile = "C:\\rjstemp\\pythonsqlite3.db" # Need double slash \\

	#-- Create projects table 
		sqlprojectscrt = """CREATE TABLE IF NOT EXISTS projects (id integer PRIMARY KEY, name text NOT NULL, begin_date text, end_date text);"""
 
	#-- Create tasks table 
		sqltaskscrt = """CREATE TABLE IF NOT EXISTS tasks (
			id integer PRIMARY KEY,
			name text NOT NULL,
			priority integer,
			project_id integer NOT NULL, 
			status_id integer NOT NULL,
			begin_date text NOT NULL,
			end_date text NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (id)
			);"""

	# Connect to database 
		conn1=create_connection(dbfile)

	# Attempt to create each table
		if create_table(conn1,sqlprojectscrt):
			print("project table created successfully if it didn't exist.") 
		else:
			print("project table NOT created.") 

		if create_table(conn1,sqltaskscrt):
			print("task table created successfully if it didn't exist.") 
		else:
			print("task table NOT created.") 

	# Query project table
		cursor1=execute_query(conn1,"select * from projects")
  
	# If we got data results, fetch and display records   
		if cursor1 != None:
			rows = cursor1.fetchall()
		# Iterate and output data rows 
			for row in rows:
				print(row)
		else: 
			print("No data in project table.") 

	# Close connection
		if conn1 != False: 
			close_connection(conn1)
		# Set success info
		exitcode=0
		exitmessage='DB test program completed successfully'

	#------------------------------------------------
	# Handle Exceptions
	#------------------------------------------------
	except Exception as ex: # Catch and handle exceptions
		exitcode=99 # set return code for stdout
		exitmessage=str(ex) # set exit message for stdout
		print('Traceback Info') # output traceback info for stdout
		traceback.print_exc()        

	#------------------------------------------------
	# Always perform final processing
	#------------------------------------------------
	finally: # Final processing
		# Do any final code and exit now
		# We log as much relevent info to STDOUT as needed
		print('ExitCode:' + str(exitcode))
		print('ExitMessage:' + exitmessage)
		endtime=datetime.datetime.now()
		print("End of Main Processing - " + str(endtime.strftime("%H:%M:%S")))
		print("Elapsed Processing Time - " + str(endtime - begintime))
		print(dashes)
	
		# Exit the script now
		sys.exit(exitcode) 
