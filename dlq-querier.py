import re
import sys

class querier:
    def __init__(self, pattern):
        self.pattern = pattern
        self.re_obj = re.compile(pattern)
    
    def query(self, filename):
        f = open(filename, 'r')
        for idx, line in enumerate(f.readlines()):
            m = self.re_obj.match(line)
            if m:
                print(str(idx) + ': ' + line)
        f.close()

if __name__ == '__main__':
    pattern = sys.argv[1]
    filename = sys.argv[2]
    q = querier(pattern)
    q.query(filename)