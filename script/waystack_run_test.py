#!/usr/bin/env python3

import ast
import os
import sys

from cc_pathlib import Path

import waystack

def qeval(s) :
	try :
		return ast.literal_eval(s)
	except ( SyntaxError, ValueError ) :
		return s

def test(test_dir) :
	line_lst = (test_dir / "input.tsv").load()

	fms = waystack.FullStack()

	mon = waystack.ShortStack()
	upm = waystack.ShortStack()

	for line in line_lst :
		print("\n---  " + ' '.join(line) + "\n")
		if line[0] == '!!' :
			print("\n~~~ MON")
			mon_check = fms.commit(mon)
			print("\n~~~ UPM")
			upm_check = fms.commit(upm)
		elif line[0] == '->' :
			pass
		else :
			fms.execute(* [qeval(cell) for cell in line])

if __name__ == '__main__' :
	for arg in sys.argv[1:] :
		test(Path(arg))

