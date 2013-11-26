import os
import errno

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise

def write_file(filepath, list):
	f = open(filepath, 'w')
	for item in list:
		f.write(item + "\n")
	f.close()

def read_file(filepath):
	f = open(filepath, 'r')
	list = f.read().strip("\n").split("\n")
	f.close()
	
	return list