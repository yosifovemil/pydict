#!/usr/bin/env python

import csv

class CSVReader:

	def __init__(self, f_name):
		reader = self.unicode_csv_reader(open(f_name))
		header = reader.next()
		self._content = []
		for line in reader:
			entry = dict()
			for key,val in zip(header, line):
				entry[key] = val

			self._content.append(entry)

	def get_content(self):
		return self._content	

	
	def unicode_csv_reader(self, utf8_data, dialect=csv.excel, **kwargs):
		csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
		for row in csv_reader:
			yield [unicode(cell, 'utf-8') for cell in row]

