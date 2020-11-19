#!/usr/bin/env python3

from waystack.waypoint import W

class FullStack() :
	def __init__(self) :
		self.stack = list()
		self.start = 0

	def __str__(self) :
		stack = list()
		for i, w in enumerate(self.stack) :
			stack.append(f'{i:2d} : {w}')
		return '\n'.join(stack)

	def cmd_delete(self, pos) :
		print(f" >> FullStack.cmd_delete({pos})")
		self.stack.pop(pos)

	def cmd_insert(self, pos, wpt) :
		print(f" >> FullStack.cmd_insert({pos}, {wpt})")
		self.stack.insert(pos, wpt)

	def cmd_push(self, wpt) :
		print(f" >> FullStack.cmd_push({wpt})")
		self.stack.append(wpt)

	def cmd_swap(self, pos_a, pos_b) :
		print(f" >> FullStack.cmd_swap({pos_a}, {pos_b})")
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

		print(str(self))

		w_final = other.stack[other.final][1]
		i_final = None if w_final is None else w_final.id

		short_set = set(w.id for w in other)
		full_set = set(w.id for w in self.stack[self.start:self.start + 4])

		print("SHORT:", ', '.join(short_set))
		print("FULL", ', '.join(full_set))

		to_be_deleted = short_set - full_set
		to_be_added = full_set - short_set

		print('DEL:', ', '.join(to_be_deleted))
		print('ADD:', ', '.join(to_be_added))

		other.delete(* sorted(short_set - full_set))

		mode = "PUSH" if i_final is None else "INSERT"
		for i, w in enumerate( self.stack[self.start:self.start + 4] ) :
			print(w.id, i_final, mode, w.id in to_be_added)
			if w.id == i_final :
				mode = "PUSH"
			if w.id in to_be_added :
				if mode == "INSERT" :
					other.insert(i, w)
				else :
					other.push(w)

		print(other)
