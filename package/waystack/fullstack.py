#!/usr/bin/env python3

import sys

import waystack.levenstein

from waystack.waypoint import W

class FullStack() :

	debug = sys.stdout

	def pp(self, * pos) :
		print(* pos, file=self.debug)

	def __init__(self, start=0) :
		self.stack = list()
		self.start = start

	def __getitem__(self, index) :
		return self.stack[self.start + index]

	def __str__(self) :
		stack = list()
		for i, w in enumerate(self.stack) :
			stack.append(('>>' if i == self.start else '  ') + f'{i:2d} : {w}')
		return '\n'.join(stack)

	def cmd_delete(self, pos) :
		self.pp(f" >> FullStack.cmd_delete({pos})")
		self.stack.pop(pos)

	def cmd_insert(self, pos, wpt) :
		self.pp(f" >> FullStack.cmd_insert({pos}, {wpt})")
		self.stack.insert(pos, wpt)

	def cmd_push(self, wpt) :
		self.pp(f" >> FullStack.cmd_push({wpt})")
		self.stack.append(wpt)

	def cmd_swap(self, pos_a, pos_b) :
		self.pp(f" >> FullStack.cmd_swap({pos_a}, {pos_b})")
		self.stack[pos_a], self.stack[pos_b] = self.stack[pos_b], self.stack[pos_a]

	def execute(self, cmd, * param):
		param = list(param)

		if cmd == 'push' :
			self.cmd_push( W(* param) )
		
		elif cmd == "swap":
			old_id = param.pop(0)
			new_id = param.pop(0)
			self.cmd_swap(old_id, new_id)

		elif cmd == 'insert':
			cur_id = param.pop(0)
			self.cmd_insert(cur_id, W(* param))

		elif cmd == 'delete':
			cur_id = param.pop(0)
			self.cmd_delete(cur_id)

	def commit(self, other) :

		self.pp(self)
		self.pp(other)

		other.cmd_begin()

		short_lst = [w.id for w in other]
		full_lst = [w.id for w in self.stack[self.start:self.start + other.size]]

		self.pp(short_lst)
		self.pp(full_lst)

		diff_lst = waystack.levenstein.diff(short_lst, full_lst)
		self.pp(diff_lst, '\n')

		n = 0
		del_lst = list()
		for block in diff_lst :
			for item in block.line :
				if block.action in '-/' :
					self.pp("DEL: ", n, short_lst[n])
					del_lst.append(short_lst[n])
				if block.action in '=-/' :
					n += 1

		if del_lst :
			ret_del = other.cmd_del(* reversed(del_lst))
			assert(len(del_lst) == ret_del)
			self.pp(other)
		else :
			ret_begin = other.cmd_begin()
			print("begin:", ret_begin)

		n = 0
		for block in diff_lst :
			for item in block.line :
				if block.action in '+*' :
					self.pp("ADD: ", n, self[n])
					ret_add = other.cmd_add(n, self[n])
					print("add:", ret_add)
					self.pp(other)
				if block.action in '=+*' :
					n += 1

		short_lst = [w.id for w in other]

		self.pp(short_lst)
		self.pp(full_lst)

		return
