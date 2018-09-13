import re
import sys

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


if __name__ == '__main__':
    pattern = sys.argv[1]
    filename = sys.argv[2]
    for output in doQuery2(pattern, filename):
        print(output)