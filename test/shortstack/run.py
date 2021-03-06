#!/usr/bin/env python3

import ast
import os
import subprocess
import sys

from cc_pathlib import Path

import waystack

from waystack.waypoint import Waypoint, W, reset_W

def qeval(s) :
	try :
		return ast.literal_eval(s)
	except ( SyntaxError, ValueError ) :
		return s

def test(line_lst, output=sys.stdout) :
	line_lst = (cwd / "input.tsv").load()

	reset_W()

	u = waystack.ShortStack()
	u.debug = output

	for line in line_lst :
		print("\n---  " + ' '.join(line) + "\n", file=output)

		line = [qeval(cell) for cell in line]

		cmd, * param = line
		if cmd == "push" :
			ret = u.push(W(* param))
		elif cmd == "delete" :
			ret = u.delete(* param)
		elif cmd == "trim" :
			ret = u.trim(* param)
		elif cmd == "insert" :
			prev_id = param.pop(0)
			ret = u.insert(prev_id, W(* param))

		print("RETURN:", ret, file=output)

		print(u, file=output)

if __name__ == '__main__' :
	for arg in sys.argv[1:] :

		cwd = Path(arg)

		input_tsv = cwd / "input.tsv"
		output_log = cwd / "output.log"
		output_ref = cwd / "output.ref"

		if not input_tsv.is_file() :
			continue

		with output_log.open('wt') as fid :
			line_lst = input_tsv.load()
			test(line_lst, fid)

		if not output_ref.is_file() :
			output_ref.write_text(output_log.read_text())

		ret = subprocess.run(["diff", "-u", "--color", "output.log", "output.ref"], cwd=cwd)
		flag = '\x1b[32mOK\x1b[0m' if ret.returncode == 0 else '\x1b[31mKO\x1b[0m'
		print(f"{arg} -- {flag}")

