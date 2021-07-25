import os
import csv
import sys

file_name = sys.argv[1]
table_name = os.path.splitext(file_name)[0]
row_number = 0
with open(file_name, newline='\n') as csv_file:
	reader = csv.reader(csv_file, delimiter='|', quotechar='"')
	for row in reader:
		if row_number == 0:
			header = row
		else:
			values = ["'" + column.replace('\n', ' ').replace('\r', '') + "'" for column in row]
			sql = 'INSERT INTO %s(%s) VALUES (%s);' % (table_name, ', '.join(header), ', '.join(values))
			print(sql)
		row_number += 1
