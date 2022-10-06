#!/usr/bin/env python3

from ruuvitag_sensor.ruuvitag import RuuviTag
import sys, getopt

def print_usage(output = sys.stdout):
	print("Usage: ruuvi.py -s <temperature|humidity|pressure> -m <mac_address> [-v]", file = output)


def read_sensor(metric, mac):
	sensor = RuuviTag(mac)
	sensor.update()
	state = sensor.state

	if metric != "temperature" and metric != "pressure" and metric != "humidity":
		print("Unsupported sensor metric", file = sys.stderr)
		sys.exit(2)

	return state[metric]


def main(argv):
	metric = ""
	mac = ""
	verbose = False

	try:
		opts, args = getopt.getopt(argv, "hs:m:v")
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
		elif opt == "-m":
			mac = arg

	if metric == "" or mac == "":
		print_usage(output = sys.stderr)
		sys.exit(2)

	value = read_sensor(metric, mac)

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
