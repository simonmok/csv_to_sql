import os
import csv
import sys

delimiter = ','
quotechar = '"'

file_name_1, file_name_2 = sys.argv[1], sys.argv[2]
primary_keys = [int(i) for i in sys.argv[3:]]
table_name = os.path.splitext(file_name_1)[0]
row_number = 0
record_1 = dict()
header = None
primary_key_names = list()

with open(file_name_1, newline='\n') as csv_file:
	reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)
	for row in reader:
		if row_number == 0:
			header = row
			primary_key_names = [header[i] for i in primary_keys]
		else:
			record_1[tuple(row[i] for i in primary_keys)] = row
		row_number += 1


row_number = 0
record_2 = dict()
with open(file_name_2, newline='\n') as csv_file:
	reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)
	for row in reader:
		if row_number == 0:
			assert header == row, "Header row should be the same"
		else:
			record_2[tuple(row[i] for i in primary_keys)] = row
		row_number += 1

key_1, key_2 = set(record_1), set(record_2)

print('-- INSERT script')
for key in key_2 - key_1:
	values = ["'" + column + "'" for column in record_2[key]]
	sql = 'INSERT INTO %s(%s) VALUES (%s);' % (table_name, ', '.join(header), ', '.join(values))
	print(sql)

print()
print('-- DELETE script')
for key in key_1 - key_2:
	condition = ' AND '.join(['%s = %s' % (column, value) for column, value in zip(primary_key_names, key)])
	sql = 'DELETE FROM %s WHERE %s;' % (table_name, condition)
	print(sql)

print()
print('-- UPDATE script')
for key in key_1.intersection(key_2):
	values_1 = record_1[key]
	values_2 = record_2[key]
	if (values_1 != values_2):
		values = ["%s = '%s'" % (column, value_2) for column, value_1, value_2 in zip(header, values_1, values_2) if value_1 != value_2]
		condition = ' AND '.join(['%s = %s' % (column, value) for column, value in zip(primary_key_names, key)])
		sql = 'UPDATE %s SET %s WHERE %s;' % (table_name, ', '.join(values), condition)
		print(sql)
