import re
import sys
import subprocess
import copy

def doQuery(pattern, filename):
    #print("doQuery is called")
    pattern2 = pattern
    if pattern2[0:2] != '.*':
        pattern2 = '.*' + pattern2
    if pattern2[-2:] != '.*':
        pattern2 = pattern2 + '.*'
    try:
        re_obj = re.compile(pattern2)
    except:
        print("Invalid query pattern: %s" %pattern)
        return
    f = open(filename, 'r')
    result = []
    for idx, line in enumerate(f.readlines()):
        line = line.strip()
        m = re_obj.match(line)
        if m:
            output = str(idx) + ': ' + line
            result.append(output)
    f.close()
    return '\n'.join(result)

def doQuery2(pattern, filename):
    # print("doQuery2 is called")
    pattern2 = pattern
    if pattern2[0:2] != '.*':
        pattern2 = '.*' + pattern2
    if pattern2[-2:] != '.*':
        pattern2 = pattern2 + '.*'
    try:
        re_obj = re.compile(pattern2)
    except:
        print("Invalid query pattern: %s" %pattern)
        return
    f = open(filename, 'r')
    for idx, line in enumerate(f.readlines()):
        line = line.strip()
        m = re_obj.match(line)
        if m:
            output = str(idx) + ': ' + line + '\n'
            yield output
    f.close()


def callGrepOnVM(grepCall):
	try:
		output = subprocess.check_output(grepCall).strip()
		afterGrepCount = copy.deepcopy(grepCall)
		afterGrepCount.insert(1, '-c')
		countOutput = subprocess.check_output(afterGrepCount).strip()
		output = output.split("\n")
		output.append(countOutput)
		for i in range(0, len(output)):
			yield output[i]
	except subprocess.CalledProcessError as e:
		if e.returncode  == 1:
			output = "Return non-zero exit status 1, which means the file has no matches found with pattern and options"
			yield output
		elif e.returncode == 2:
			output = "No such file or directory error"
			yield output



if __name__ == '__main__':
    pattern = sys.argv[1]
    filename = sys.argv[2]
    for output in doQuery2(pattern, filename):
        print(output)
