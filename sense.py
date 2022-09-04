#!/usr/bin/env python3

from sense_hat import SenseHat
import sys, getopt

def print_usage(output = sys.stdout):
	print("Usage: sense.py -s <temperature|humidity|pressure> [-v]", file = output)

def read_sensor(metric):
	sensors = SenseHat()
	value = ""

	if metric == "temperature":
		value = sensors.get_temperature()
	elif metric == "humidity":
		value = sensors.get_humidity()
	elif metric == "pressure":
		value = sensors.get_pressure()
	else:
		print("Unsupported sensor metric", file = sys.stderr)
		sys.exit(2)

	return value

def main(argv):
	metric = ""
	verbose = False

	try:
		opts, args = getopt.getopt(argv, "hs:v")
	except getopt.GetoptError:
		print_usage(output = sys.stderr)
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print_usage()
			sys.exit()
		if opt == "-v":
			verbose = True
		elif opt == "-s":
			metric = arg

	if metric == "":
		print_usage(output = sys.stderr)
		sys.exit(2)

	value = read_sensor(metric)

	units = {
		"temperature": "C",
		"humidity": "%",
		"pressure": "mbar"
	}

	if verbose:
		print("%s: %s %s" % (metric.capitalize(), value, units[metric]))
	else:
		print("%s" % value)

if __name__ == "__main__":
	main(sys.argv[1:])
