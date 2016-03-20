#!/usr/bin/env python

from Tkinter import *
from game import Game
import argparse
import os
import subprocess
from datetime import datetime

class Dictionary:

	directions = {True: 'GER -> ENG', False: 'ENG -> GER'}

	def __init__(self, master, dict_f):
		self._game = Game(dict_f)

		frame = Frame(master)
		frame.pack()
		frame.grid(padx = 50, pady = 50)
		line_spacing = 50
		horizontal_spacing = 30

		Label(frame, text = "Win").grid(row = 0, column = 0, 
										padx = (0,horizontal_spacing))
		self._win = Label(frame)
		self._win.grid(row = 1, column = 0, 
						padx = (0,horizontal_spacing), 
						pady = (0, line_spacing))

		Label(frame, text = "Total").grid(row = 0, column = 1, 
											padx = (0,horizontal_spacing))
		self._total = Label(frame)
		self._total.grid(row = 1, column = 1, 
						padx = (0,horizontal_spacing), 
						pady = (0, line_spacing))

		Label(frame, text = "Percentage").grid(row = 0, column = 2)
		self._perc = Label(frame)
		self._perc.grid(row = 1, column = 2, 
						padx = (0,horizontal_spacing), 
						pady = (0,line_spacing))

		self._q_lab = Label(frame)
		self._q_lab.grid(row=2, columnspan = 4)
	
		self._a_entry = Entry(frame)
		self._a_entry.grid(row=3, columnspan = 4,
						pady = (0, line_spacing) )
		self._a_entry.focus()
		self._a_entry.bind('<Return>', self._answer)

		self._user_answer = Label(frame)
		self._user_answer.grid(row=4, columnspan = 4)
		self._real_answer = Label(frame)
		self._real_answer.grid(row=5, columnspan = 4)

		self._direction_lab = Label(frame)
		self._direction_lab.grid(row = 6, column = 4)	

		self._dir_button = Button(frame, anchor="ne", text = "Change direction")
		self._dir_button.grid(row=7, column = 4)
		self._dir_button.bind("<Button-1>", self.change_direction)

		self._update_fields(draw_correct = False)

	def _update_fields(self, draw_correct = True):
		self._direction_lab.config(text = Dictionary.directions[self._game._direction])
		self._q_lab.config(text = self._game._q)
		if self._game._score < 1.0:
			self._user_answer.config(text = self._game._prev_i, fg = 'red')
			self._real_answer.config(text = self._game._prev_a, fg = 'green')
		else:
			if draw_correct:
				self._user_answer.config(text = "Correct!", fg = 'green')
				self._real_answer.config(text = "")

		win = int(self._game._win)
		total = int(self._game._total)
		self._win.config(text = win)
		self._total.config(text = total)
		if total != 0:
			self._perc.config(text = "%d%%" % int(100 * (self._game._win/self._game._total)) )

	def change_direction(self, event):
		self._game.change_direction()
		self._game.next_question()
		self._update_fields(draw_correct = False)

	def _answer(self, event):
		self._game.set_answer(self._a_entry.get())
		self._a_entry.delete(0, 'end')
		self._update_fields()

def write_updated():
	f = open("updated", 'w')
	f.write(datetime.now().strftime("%d/%m/%Y"))
	f.close()

def read_updated():
	f = open("updated", 'r')
	content = f.readlines()
	d = datetime.strptime(content[0].strip(), "%d/%m/%Y")
	return d

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--parent", required = True)
	parser.add_argument("-d", "--dictionary", default = "words.csv")
	args = parser.parse_args()

	os.chdir(args.parent)
	if os.path.isfile("updated"):
		d = read_updated()
		diff = datetime.now() - d
		if diff.days >= 1:
			print "Updating git"
			subprocess.call(['git','pull'])
			write_updated()
	else:
		write_updated()

	root = Tk()
	root.geometry('500x500')
	dictionary = Dictionary(root, args.dictionary)

	root.mainloop()
	root.destroy() # optional; see description below
