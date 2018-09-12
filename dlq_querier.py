import re
import sys

def doQuery(pattern, filename):
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
            print(output)
    f.close()
    return '\n'.join(result)

if __name__ == '__main__':
    pattern = str(sys.argv[1])
    filename = sys.argv[2]
    doQuery(pattern, filename)