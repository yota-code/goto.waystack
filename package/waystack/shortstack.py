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

		def trim(self, w_nbr=1) :
			print(f" >> ShortStack.trim({w_nbr})", file=self.debug)

			""" remove w_nbr waypoints at the end of the w_nbr """

			for z in range(w_nbr) :
				i = self.final
				p, w, n = self.stack[i]
				self.stack[i] = [None, None, None]
				self._free_slot.append(i)
				self.final = p

			self.insert_pos = self.initial

			return w_nbr


		@property
		def free_slot(self) :
			i = self._free_slot.pop(0)
			print(f" --> ShortStack.free_slot = {i}", file=self.debug)
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
			return '\n' + '\n'.join(stack) + f'\n  === [  {route}  ] ===' + '\n'

		def __iter__(self) :
			i = self.initial
			while i is not None :
				p, w, n = self.stack[i]
				if w is not None :
					yield w
				i = n


		def delete(self, * id_lst) :
			print(f" >> ShortStack.delete({', '.join(id_lst)})", file=self.debug)
			""" waypoints must be provided in reverse order, from final to initial """

			delete_cnt = 0

			id_lst = list(id_lst)

			# delete those at the end, easier, could have been trimmed
			for z in id_lst :
				if z == self.final :
					i = self.final
					p, w, n = self.stack[i]
					self.stack[i] = [None, None, None]
					self._free_slot.append()
					delete_cnt += 1
					self.final = p
				else :
					break

			# delete the others in-between, more difficult, done step by step in reverse order
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

			self.insert_pos = self.initial

			return delete_cnt
		
		def insert(self, prev_id, w) :
			print(f" >> ShortStack.insert({prev_id}, {w}) initial={self.initial} final={self.final}", file=self.debug)

			i = self.insert_pos
			while i != None :
				prev_p, prev_w, prev_n = self.stack[i]
				if prev_n == prev_id :
					try :
						j = self.free_slot
					except IndexError :
						return None
					self.stack[j] = [i, w, prev_n]
					self.stack[i][2] = j
					self.insert_pos = i
					return j
				else :
					i = prev_n
		
		def push(self, w) :
			print(f" >> ShortStack.push({w})", file=self.debug)

			try :
				i = self.free_slot
			except IndexError :
				return None

			if self.final == self.initial and self.stack[self.final][1] is None :
				# empty stack
				self.stack[i] = [None, w, None]
			else :
				self.stack[self.final][2] = i
				self.stack[i] = [self.final, w, None]
			self.final = i

			self.insert_pos = self.initial

			return i



			

if __name__ == '__main__' :
	u = ShortStack()
	print(u)
	u.push(W(3, 4))
	print(u)
	u.push(W(1, 2))
	print(u)
	u.push(W(5, 6))
	print(u)
	u.delete('B')
	print(u)
	u.push(W(7, 8))
	print(u)
	u.push(W(3, 8))
	print(u)
	u.insert('C', W(1, 8))
	print(u)
