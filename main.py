# -*- coding: utf-8 -*-
#
# ''' based on:   http://markkeller.me/2016-09-19-media_info_extractor/
# '''

import os.path
import platform
import subprocess
import os
import datetime
import sys

from sqlitedbtest import close_connection, create_connection, create_table, data_entry, comm

dashes="--------------------------------------------------"

#Output messages to STDOUT for logging
begintime=datetime.datetime.now()
print("Start of Main Processing - " + str(begintime.strftime("%H:%M:%S")))

print("Python version : " + platform.python_version() + " on os: " + sys.platform,'\n')

# this is a list with items of the type 'string'
# these are extensions of files (in the 'media' folder) which are 'no media files':
# no_media_files = ['.evs', '.py', '.xml', '.pdf', '.docx', '.db', '.exe', '.hide', '.xls', '.xlsx', '.csv', '.log', '.txt']

# here i read an external text file (again with the 'no media file' extensions), i believe this is more flexible
with open ("extensions.txt") as file:
	no_media_files = file.read()
	file.close()
print("these are 'no media files': ", "\n", no_media_files, '\n')

no_media_files = no_media_files.split("\n")
print(no_media_files, '\n')

no_media_files = ["." + item for item in no_media_files]
print(no_media_files, '\n')

if __name__ == '__main__':

	dir_work = os.getcwd()					# Return a string representing the current working directory
	print('\n', "current 'working directory' :  ", dir_work)

	# path = directory + '/folder'     # os: linux
	# path = directory + '\\folder'  # os: windows
	dir_media = dir_work + '\\media'
	print('\n', "current 'media directory' :  ", dir_media)
	dir_log = dir_work + '\\log'
	print('\n', "current 'log directory' :  ", dir_log)
	dir_db = dir_work + '\\db'
	print('\n', "current 'db directory' :  ", dir_db)

	# return a list containing the names of the entries in the directory given by 'path' ,
	# here our 'media directory'; at this time, this 'list_of_files' contains all files, without any filter
	list_of_all_files = os.listdir(dir_media)
	print("\n", "list of all files in our 'media directory' :", '\n')
	for file in list_of_all_files:
		print("   ", file)

	only_media_files = []  # here we create an empty list

	# this for-loop starts with the keyword "for" followed by an arbitrary variable name ( in this source: 'file' ),
	# which will hold the values of the following sequence object, which is stepped through.
	# the items of the sequence object are assigned one after the other to the loop variable;
	# to be precise: the variable points to the items.
	# For each item the loop body is executed, 	(we apply the filter (.evs, .py, .xml  ...)
	# to get a list only with our media-files)
	for file in list_of_all_files:

		# os.path.isfile(path) : returns 'true' if 'path' is an existing regular file.
		# in this source, at the time of the first loop-step, 'path' is the first 'file' in our 'list_of_files'
		#
		# 'if' is a 'conditional statement' , and in this for-loop we have another for-loop:
		# it starts with 'for' followed by the variable name 'filter'
		# if the item 'file' of 'list_of_files' has no extension listed in our 'filters'-list,
		# than append this 'file' ( = filename ) to our 'only_media_files'
		if os.path.isfile(os.path.join(dir_media,file)):
			if all([filter not in file for filter in no_media_files]):
				only_media_files.append(file)

	# at this time we have applied our filter rule

	print('\n', " 'only media' files (this list is filtered):  ", '\n')
	for file in only_media_files:
		print("   ", file)

	print("\n")

	# create_connection("db\\mediainfo.db")	# only test for path  \db\...
	
	# for-loop: for every file in our 'only_media_files'
	for file in only_media_files:
	
		# if args is a list, then the first item in this list is considered as the executable and the rest
		# of the items in the list are passed as command line arguments to the program:     ??? -s
		# mi_cmd = ['mediainfo.exe', '-s', file]

		# in Python 3.6 + you can use the new f - strings:
		# https://docs.python.org/3/whatsnew/3.6.html#pep-498-formatted-string-literals

		mi_cmd = ['mediainfo', '--Language=raw', '--Full', (os.path.join(dir_media, file)),
			f"--Logfile={dir_log}\{file.replace('.', '_')}_raw.log"]

		print ('\n', "'mi_cmd' is a list: ", mi_cmd)

		media_info = {}		# 'media_info' is a dictionary

		media_info[file] = subprocess.check_output(mi_cmd, universal_newlines=True, encoding='utf-8').split('\n')

		# the answer of 'check_output' is a dictionary:
		# the 'media file name' as the key, and a list as the value to this key ,
		# this 'value'-list contains all categories and parameters / values

		print("-" * 100)
	
		# for-loop: for every 'mediafile' in our 'media_info' -dictionary,
		# we create 'category' - 'append_' and 'category_dictionary' :
		# depart the 'for loop' and 'if - else' with the debugger of your ide, and watch the content of all variables
		for file in media_info.keys():

			media_db = ("db\\" + (file.replace('.', '_') + '.db'))		# path to our new database
			db = create_connection(media_db)
			
			# a new, empty, variable 'category' :  (category means the category-names General - Video - Audio ...)
			category = ''

			# here starts a loop :
			for line in media_info[file]:
				if line == '':					# there are some empty lines, ignore , don't do anything, go on
					continue
				print("Line is:  ", line)

				# find the 'category' names (General, Audio, ...)
				# .strip() removes all whitespace at the start and end, including spaces, tabs, newlines and carriage returns
				if ':' not in line.strip():  # there is no colon ':' in the category-lines 'General' - 'Video' - 'Audio' - ....
					print('\n', "     No colon ':' in 'line':  ", line)

					category = line.strip()  # update the variable 'category' with the value of stripped 'line'

					print("category is: ", category)

					# a new table with the name of our current 'category', so 'General' 'Video' ...
					# these tables will be created with two columns 'MI_Element' and 'MI_Values'
					# sql_create_table = " CREATE TABLE IF NOT EXISTS " + category + " (ID INTEGER PRIMARY KEY AUTOINCREMENT, MI_Element VARCHAR(255), MI_Value VARCHAR(255)); "
					
					sql_create_table = " CREATE TABLE IF NOT EXISTS " + category + " (MI_Element VARCHAR(255), MI_Value VARCHAR(255)) "
					create_table(db, sql_create_table)
					
					print("table with the name of category ", "(",category,")", "created")

				else:
					# line = line.replace('  ', '')  # replace two (? or more ?) spaces '  '  by nothing ''
					line = line.strip()

					# example for 'line' from the 'Audio' category ( two ' : ') :      Channel positions : Front: L R
					# another example :     Tagged date : UTC 2013-12-13 15:39:16  , a lot of ' : '
					# again a second loop ' for - in' in a loop
					# second parameter for 'split' is called 'maxsplits', meaning the number of times 'line.split' should do
					mi_element, mi_value = [x.strip() for x in line.split(': ', 1)]		# mediainfo element, mediainfo value
					mi_element, mi_value = [category.strip() for category in line.split(': ', 1)]
					print(" 'MediaInfo Element' is:   ", mi_element)
					print(" 'MediaInfo Value' is:   ", mi_value)

					mi_e = str(mi_element)		# ?? are these lines necessary ?? is the output of 'MediaInfo' always 'string' ?
					mi_v = str(mi_value)		# i want to be shure, there are no 'integer' or 'float' in 'mi_e' and 'mi_v' 

					# sql_entry_data = f"INSERT INTO {category} (MI_Element, MI_Value) VALUES ('{mi_e}', '{mi_v}');"	# error
					sql_entry_data = f"INSERT INTO {category} VALUES ('{mi_e}', '{mi_v}');"
					
					data_entry(db, sql_entry_data)
			comm(db, media_db)
			close_connection(media_db)

	endtime=datetime.datetime.now()
	print('\n', dashes)
	print("End of Main Processing - " + str(endtime.strftime("%H:%M:%S")))
	print("Elapsed Processing Time - " + str(endtime - begintime))
	print(dashes)
	
	# Exit the script now
print("\n\n!!!   Done   !!!")
raise SystemExit()