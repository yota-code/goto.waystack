#!/usr/bin/env python3

import ast
import os
import subprocess
import sys

from cc_pathlib import Path

import waystack

def qeval(s) :
	try :
		return ast.literal_eval(s)
	except ( SyntaxError, ValueError ) :
		return s

def test(line_lst, output=sys.stdout) :

	if line_lst[0][0] == '##' :
		null, p_start, p_size = line_lst.pop(0)
		fms = waystack.FullStack(p_start)
		mon = waystack.ShortStack(p_size)
		# upm = waystack.ShortStack(p_size)
	else :
		fms = waystack.FullStack()
		mon = waystack.ShortStack()
		# upm = waystack.ShortStack()

	fms.debug = output
	mon.debug = output

	for line in line_lst :
		cmd, * param = [qeval(cell) for cell in line]
		print("\n---  " + ' '.join(line) + "\n", file=output)
		if cmd == '!!' :
			print("\n~~~ MON", file=output)
			mon_check = fms.commit(mon)
			# print("\n~~~ UPM", file=output)
			# upm_check = fms.commit(upm)
		elif cmd == '->' :
			pass
		elif cmd == '##' :
			# fast forward
			fms.start = param.pop(0)
		else :
			fms.execute(cmd, * param)

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

