#!/usr/bin/env python3

import collections

Waypoint = collections.namedtuple('Waypoint', ['id', 'lat', 'lon'])

_counter_id = ord('A')

def reset_W() :
	global _counter_id
	_counter_id = ord('A')

def W(* pos) :
	global _counter_id
	w = Waypoint(chr(_counter_id), * pos)
	_counter_id += 1
	return w