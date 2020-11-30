#!/usr/bin/env python3

import sys

from waystack.waypoint import W

class ShortStack() :

		debug = sys.stdout

		def pp(self, * pos) :
			print(* pos, file=self.debug)

		def __init__(self, size=6) : # size is the default size of te shortstack

			self.size = size
			self.stack = list()
			self._free_slot = list()

			self.initial = 0
			self.final = 0

			self.insert_pos = self.initial

			for i in range(size) :
				self.stack.append([None, None, None])
				self._free_slot.append(i)

		def step(self, w_nbr=1) :
			# return the index of the next waypoint pointed by self.initial
			# return None if there is no next waypoint
			for z in range(w_nbr) :
				i = self.initial
				p, w, n = self.stack[i]
				if w is None :
					break
				self.stack[i] = [None, None, None]
				self._free_slot.append(i)
				if n is not None :
					self.stack[n][0] = None
					self.initial = n
			return n

		@property
		def free_slot(self) :
			i = self._free_slot.pop(0)
			self.pp(f"--> ShortStack.free_slot = {i}")
			return i

		def __str__(self) :
			stack = list()
			for i, (p, w, n) in enumerate(self.stack) :
				stack.append(' '.join([
					'I' if i == self.initial else ' ',
					'F' if i == self.final else ' ',
					'..' if p is None else f"{p:2d}",
					'<-(',
					f"{i:2d}",
					')->',
					'..' if n is None else f"{n:2d}",
					':',
					str(w) 
				]))
			route = ' -> '.join(w.id for w in self if w is not None)
			return '\n' + '\n'.join(stack) + f'\n  === [  {route}  ] === free: {self._free_slot}' + '\n'

		def __iter__(self) :
			loop_set = set()
			i = self.initial
			while i is not None :
				p, w, n = self.stack[i]					
				if w is not None :
					yield w
				if i in loop_set :
					break
				loop_set.add(i)
				i = n

		def cmd_del(self, * id_lst) :
			self.pp(f" >> ShortStack.delete({', '.join(id_lst)})")
			""" waypoints must be provided in reverse order, from final to initial """

			delete_cnt = 0

			id_lst = list(id_lst)

			i = self.final
			while i is not None and id_lst :
				p, w, n = self.stack[i]
				if w.id == id_lst[0] :
					self._free_slot.append(i)
					delete_cnt += 1
					if p is not None :
						self.stack[p][2] = n
					else :
						self.initial = n
					if n is not None :
						self.stack[n][0] = p
					else :
						self.final = p
					self.stack[i] = [None, None, None]
					id_lst.pop(0)
				i = p

			self.cmd_begin()

			return delete_cnt

		def cmd_begin(self) :
			self.cursor_pos = 0
			self.cursor_ind = self.initial
			
			return self.cursor_ind

		def cmd_add(self, insert_pos, w) :
			self.pp(f">>> ShortStack.cmd_add({insert_pos}, {w}) {self.initial} -> {self.final}")

			if self.cursor_ind == self.final :
				# the cursor is as the last point, it's easier to just push
				return self._cmd_push(w)

			# self.pp(f"self.cursor_ind: {self.cursor_ind}")
			# self.pp(f"self.cursor_pos: {self.cursor_pos}")

			prev_p, prev_w, prev_n = None, None, self.initial
			while self.cursor_ind is not None :

				curs_p, curs_w, curs_n = self.stack[self.cursor_ind]
				# self.pp("CURS:", curs_p, curs_w, curs_n)
				if self.cursor_pos == insert_pos :

					prev_p, prev_w, prev_n = self.stack[curs_p]
					# self.pp("PREV:", prev_p, prev_w, prev_n)

					try :
						j = self.free_slot
					except IndexError :
						return None

					self.stack[j] = [curs_p, w, prev_n]
					self.stack[curs_p][2] = j
					self.stack[prev_n][0] = j

					self.cursor_ind = j
					return j

				else :
					self.cursor_pos += 1
					self.cursor_ind = curs_n

				# self.pp(f"self.cursor_ind: {self.cursor_ind}")
				# self.pp(f"self.cursor_pos: {self.cursor_pos}")

		
		def _cmd_push(self, w) :
			# add a waypoint at the end
			self.pp(f">>> ShortStack._cmd_push({w})")

			try :
				j = self.free_slot
			except IndexError :
				return None

			if self.stack[self.final][1] is None :
				# the stack is empty
				self.stack[j] = [None, w, None]
			else :
				self.stack[self.final][2] = j
				self.stack[j] = [self.final, w, None]

			self.final = j

			self.cursor_pos += 1
			self.cursor_ind = j

			return j



			

if __name__ == '__main__' :
	u = ShortStack()
	self.pp(u)
	u.push(W(3, 4))
	self.pp(u)
	u.push(W(1, 2))
	self.pp(u)
	u.push(W(5, 6))
	self.pp(u)
	u.delete('B')
	self.pp(u)
	u.push(W(7, 8))
	self.pp(u)
	u.push(W(3, 8))
	self.pp(u)
	u.insert('C', W(1, 8))
	self.pp(u)
