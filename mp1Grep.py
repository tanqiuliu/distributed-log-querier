import socket
import copy
import sys
import subprocess

if __name__ == "__main__":
	afterGrep = sys.argv[1:]
	afterGrep.insert(0, 'grep')

	try:
		output = subprocess.check_output(afterGrep).strip()
		afterGrepCount = copy.deepcopy(afterGrep)
		afterGrepCount.insert(1, '-c')
		countOutput = subprocess.check_output(afterGrepCount).strip()
	except subprocess.CalledProcessError as e:
		if e.returncode  == 1:
			output = "Return non-zero exit status 1, which means the file has no matches found with pattern and options"
		elif e.returncode == 2:
			output = "No such file or directory error"

	print output
	print countOutput