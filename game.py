#!/usr/bin/env python

from csvreader import CSVReader
import argparse
import random

class Game:

	def __init__(self, dict_f):
		self.load_dictionary(dict_f)

		#default values 
		self._direction = True
		self._score = 999
		self._win = 0.0
		self._total = 0.0

		self.next_question()

	def load_dictionary(self, dict_f):
		self._words = CSVReader(dict_f).get_content()

	def change_direction(self):
		self._direction = not self._direction

	def next_question(self):
		entry = random.choice(self._words)
		if self._direction:
			self._q = entry['German']
			self._a = entry['English']
		else:
			self._q = entry['English']

			if entry['Gender'] != "":
				self._q = "%s [%s]" % (self._q, entry['Gender'])
			if entry['Preposition'] != "":
				self._q = "%s %s" % (entry['Preposition'], self._q)

			self._a = entry['German']

	def set_answer(self, answer):
		self._score = self.check_answer(answer)
		self._win += self._score
		self._total += 1
		
		self._prev_i = answer
		self._prev_a = self._a
		self.next_question()

	def check_answer(self, answer):
		answ_w = answer.split(" ")
		match_w = self._a.split(" ")

		if len(match_w) == len(answ_w):
			count = 0.0
			for word, match in zip(answ_w, match_w):
				if word == match:
					count += 1.0

		else:
			count = 0.0
			for word in answ_w:
				if word in match_w:
					count += 1.0

		score = count / len(match_w)

		return(score)
