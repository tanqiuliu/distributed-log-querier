import socket
import sys
import os
import random
import subprocess
import string
import random
from multiprocessing import Process

nonRELetters = 'defghijklmnopqrstuvwxyz'
correctCharList = nonRELetters + string.digits

def get_vm_file_path(filename):
	return os.path.join('/home/mp1/', filename)

def generate_string(size, charList):
	return ''.join(random.choice(charList) for _ in range(size)) + '\r\n'

def generate_short_random_log():
	f= open("mp1unittest.txt", "w+")
	f.write("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz\r\n")
	for i in range(20):
		f.write(generate_string(52, correctCharList))
	f.write("abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabca\r\n")
	for i in range(100):
		f.write(generate_string(52, correctCharList))
	f.write("abcccccccccccccccccccccccccccccccccccccccccccccccccc\r\n")
	for i in range(200):
		f.write(generate_string(52, correctCharList))
	f.write("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabccccccccccccc\r\n")
	for i in range (1000):
		f.write(generate_string(52, correctCharList))
	f.write("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabc\r\n")
	for i in range (200):
		f.write(generate_string(52, correctCharList))
	f.close()

def generate_long_random_log():
	f= open("mp1reportlogtest.txt", "w+")
	f.write("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz\r\n")
	for i in range(20000):
		f.write(generate_string(52, correctCharList))
	f.write("abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabca\r\n")
	for i in range(10000):
		f.write(generate_string(52, correctCharList))
	f.write("abcccccccccccccccccccccccccccccccccccccccccccccccccc\r\n")
	for i in range(200000):
		f.write(generate_string(52, correctCharList))
	f.write("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabccccccccccccc\r\n")
	for i in range (800000):
		f.write(generate_string(52, correctCharList))
	f.write("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabc\r\n")
	for i in range (200000):
		f.write(generate_string(52, correctCharList))
	f.close()

def generate_random_logs_on_vms():
	for i in range(1, 11):
		generate_short_random_log()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		subprocess.call(['scp', dir_path + '/mp1unittest.txt', 'dchen51@fa18-cs425-g45-%02d.cs.illinois.edu:~/'.format(i)])

def run_server_on_vm(vmNum):
	subprocess.call(['ssh', 'dchen51@fa18-cs425-g45-{}.cs.illinois.edu'.format(vmNum), 'python /home/mp1/distributed-log-querier/dlq_server.py'])

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

if __name__ == '__main__':
	vmNums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
	runInParallel(run_server_on_vm('01'), run_server_on_vm('02'), 
				  run_server_on_vm('03'), run_server_on_vm('04'), 
				  run_server_on_vm('05'), run_server_on_vm('06'), 
			 	  run_server_on_vm('07'), run_server_on_vm('08'), 
				  run_server_on_vm('09'), run_server_on_vm('10'))
		
