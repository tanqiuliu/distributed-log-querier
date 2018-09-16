import socket
import sys
import os
import random
import subprocess
import string
import random
from dlq_client import *

nonRELetters = 'defghijklmnopqrstuvwxyz'
correctCharList = nonRELetters + string.digits
vmNums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

def get_vm_file_path(filename):
	return os.path.join('/home/mp1/', filename)

#Generates a random strng of size:size among the chararacter List given
def generate_string(size, charList):
	return ''.join(random.choice(charList) for _ in range(size)) + '\r\n'

#Generates a short txt/log file, somewhere under 3MB
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

#Generates a long txt/log file, somewhere above 60MB
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


#Creates a random short txt/log file and copies it over to the beginning directory of every VM
def generate_random_logs_on_vms():
	for i in range(1, 11):
		generate_short_random_log()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		subprocess.call(['scp', dir_path + '/mp1unittest.txt', 'dchen51@fa18-cs425-g45-%02d.cs.illinois.edu:~/'.format(i)])

#Runs the server on the vm number given
def run_server_on_vm(vmNum):
	subprocess.call(['ssh', 'dchen51@fa18-cs425-g45-{}.cs.illinois.edu'.format(vmNum), 'python /home/mp1/distributed-log-querier/dlq_server.py'])


#Runs the server on vms 1-10
def run_multiple_servers():
	for i in vmNums:
		run_server_on_vm(i)

def check_grep_output_on_servers():
	lineCount = []
	for i in vmNums:
		lineCount.append(subprocess.check_output(['ssh', 'dchen51@fa18-cs425-g45-{}.cs.illinois.edu'.format(i), 'grep -c -e abc /home/dchen51/mp1unittest.txt']).strip().decode('utf-8'))
	assert(lineCount == ['5', '5', '5', '5', '5', '5', '5', '5', '5', '5'])
	print('Passed putting files on all VMS and grepping them')	

def check_client_py_on_servers():
	nodeCount = []
	for i in range(0, 10):
		outputCount = subprocess.check_output(['python3.6 dlq_client.py -e abc -e bca -e zazz'])[i]['count'])
		nodeCount.append(outputCount)
		wait = input("Please press enter once you set up the next server")
	print nodeCount

if __name__ == '__main__':
	check_grep_output_on_servers()
		
