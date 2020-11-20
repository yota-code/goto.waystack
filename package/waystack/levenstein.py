#!/usr/bin/env python3

# file released under the GPLv3
# copyleft <yota.news@gmail.com>

import io

class Block() :
	def __init__(self, line, action) :
		self.line = line
		self.action = action
		
	def __str__(self) :
		return "({0}{1}{0})".format(self.action, ' '.join(str(i) for i in self.line))
	
	def __repr__(self) :
		return "{0}{{{1}}}".format(self.action, '|'.join(repr(i) for i in self.line))

def longest_common_substring(src, dst) :
	
	# to avoid dependency on numpy, let's use a list() of list()
	c = [[0] * len(dst) for i in range(len(src))]

	z = 0
	src_m = None
	dst_m = None
	for i in range(len(src)) :
		for j in range(len(dst)) :
			#print(src[i], '?=', dst[j])
			#print('i=', i, 'j=,', j)
			if src[i] == dst[j] :
				if i == 0 or j == 0 :
					#print("one zero")
					c[i][j] = 1
				else :
					#print("no zero")
					c[i][j] = c[i-1][j-1] + 1
				if c[i][j] > z :
					#print("increment")
					z = c[i][j]
				if c[i][j] == z :
					src_m = (i-z+1, i+1)
					dst_m = (j-z+1, j+1)
			else :
				c[i][j] = 0

	return src_m, dst_m

def diff(src, dst, depth=0, pos="first") :
	
	if len(src) == 0 or len(dst) == 0 :
		# at leat one field is empty
		if len(src) != 0 :
			# no destination corresponding to the source, then (- src -)
			return [Block(src, '-'),]			
		elif len(dst) != 0 :
			# no source corresponding to the destination, then (+ dst +)
			return [Block(dst, '+'),]
		else :
			# both empty, then nothing 
			return list()
			
	src_m, dst_m = longest_common_substring(src, dst)
	if src_m == None and dst_m == None :
		return [Block(src, '/'), Block(dst, '*'),]
	else :
		middle = src[src_m[0]:src_m[1]]
		left = diff(src[:src_m[0]], dst[:dst_m[0]], depth+1, "left")
		right = diff(src[src_m[1]:], dst[dst_m[1]:], depth+1, "right")
		if middle :
			return left + [Block(middle, '='),] + right
		else :
			return left + right

def synthetic_unified_diff(src, dst) :
	result_lst = list()
	delta_lst = diff(src, dst)
	for block in delta_lst :
		for item in block.line :
			if block.action != '/' :
				result_lst.append(block.action)
	return result_lst


def synthetic_splitted_diff(src, dst) :
	src_lst, dst_lst = list(), list()
	delta_lst = diff(src, dst)
	for block in delta_lst :
		for item in block.line :
			if block.action in '=-/' :
				src_lst.append(block.action)
			if block.action in '=+*' :
				dst_lst.append(block.action)
	return src_lst, dst_lst

def indexed_diff(src, dst) :
	src_lst, dst_lst = list(), list()
	delta_lst = diff(src, dst)
	src_n, dst_n = 0, 0
	for block in delta_lst :
		for item in block.line :
			if block.action in '-/' :
				src_lst.append(src_n)
			if block.action in '+*' :
				dst_lst.append(dst_n)
			if block.action in '=-/' :
				src_n += 1
			if block.action in '=+*' :
				dst_n += 1
	return src_lst, dst_lst
		
def html_diff(src, dst, sep=None) :
	
	if sep is not None :
		src = src.strip(sep).split(sep)
		dst = dst.strip(sep).split(sep)
	else :
		sep = ''
		
	result = diff(src, dst)

	s = list()
	for Block in result :
		if Block.action == '=' :
			s.append(sep.join(Block.line))
		elif Block.action == '-' :
			s.append('<span class="diff_deleted">' + sep.join(Block.line) + '</span>')
		elif Block.action == '/' :
			s.append('<span class="diff_modified">' + sep.join(Block.line) + '</span>')
	d = list()
	for Block in result :
		if Block.action == '=' :
			d.append(sep.join(Block.line))
		elif Block.action == '+' :
			d.append('<span class="diff_created">' + sep.join(Block.line) + '</span>')
		elif Block.action == '*' :
			d.append('<span class="diff_modified">' + sep.join(Block.line) + '</span>')
		
	return sep.join(s), sep.join(d)
	
if __name__ == '__main__' :
	#a = "a b c d e f g h i j"
	#b = "a b d e q g h j i"
	a='a b c d'.split(' ')
	b='b c d e'.split(' ')


	a = [3247330401, 2197528548, 3205926072, 916527825]
	b = [3478510675, 360556937, 2197528548, 3205926072]

	a = "ABCDE"
	b = "ACBED"
	#a = "ABCDG"
	#b = "EFGHI"

	res = diff(a,b)
	print(res)
	print(res[0])


	#print(synthetic_unified_diff(a, b))
	# print(synthetic_splitted_diff(a, b))
	# print(indexed_diff(a, b))
	# print(html_diff(a, b))
	#print(longest_common_substring(a, b))
	# a = "Lorem ipsum amet consectetur adipiscing elit Ut id nisl quis lacus lobortis egestas id nec turpis"
	# b = "Lorem ipsum amet consectetur amet consectetur elit Ut id nisl ploum quis lacus lobortis egestas id nec turpis"

	# print(diff_two(a, b))
	# with open("diff.html", 'wt', encoding='utf8') as fid :
	# 	fid.write(html_two(a, b))
	
