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

def generate_short_frequent_random_log():
	f= open("mp1unittest.txt", "w+")
	for i in range (1000):
		f.write(generate_string(52, correctCharList))
	f.write("1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabc\r\n")
	for i in range (1000):
		f.write(generate_string(52, correctCharList))
	f.close()

#Generates a short txt/log file, somewhere under 3MB where the 
def generate_short_infrequent_random_log():
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
		generate_short_infrequent_random_log()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		subprocess.call(['scp', dir_path + '/mp1unittest.txt', 'dchen51@fa18-cs425-g45-%02d.cs.illinois.edu:~/'.format(i)])

#Runs the server on the vm number given
def run_server_on_vm(vmNum):
	subprocess.call(['ssh', 'dchen51@fa18-cs425-g45-{}.cs.illinois.edu'.format(vmNum), 'python /home/mp1/distributed-log-querier/dlq_server.py'])


#The server part of the client-server unit test that must be run first in order to get the servers started
def run_multiple_servers():
	for i in vmNums:
		run_server_on_vm(i)

#Unit test that puts log files on all machines with known and random lines then checks that the grep function works with the keyword on those known lines
def check_grep_output_on_servers():
	lineCount = []
	for i in vmNums:
		lineCount.append(subprocess.check_output(['ssh', 'dchen51@fa18-cs425-g45-{}.cs.illinois.edu'.format(i), 'grep -c -e abc /home/dchen51/mp1unittest.txt']).strip().decode('utf-8'))
	assert(lineCount == ['5', '5', '5', '5', '5', '5', '5', '5', '5', '5'])
	print('Passed putting files on all VMS and grepping them')
		

#The client part of the client-server unit test that must be run with in conjunction with the run_multiple_servers checking one server at a time because of the password input. Checks for the specific keyword -e abc -e bca -e zazz
def check_client_pattern_on_servers(pattern):
	nodeCount = []
	lineCount = []
	grepStart = 'grep -c ' + pattern + ' /home/mp1/vm'
	print("===========================================================================================")
	print("Running unit test on the pattern: " + pattern + " : on all vm logs")
	print("===========================================================================================")
	for i, vmNum in enumerate(vmNums):
		try:
			lineCount.append(int((subprocess.check_output(['ssh', 'dchen51@fa18-cs425-g45-{}.cs.illinois.edu'.format(vmNum), grepStart + str(i+1) + '.log'])).strip().decode('utf-8')))
		except:
			lineCount.append(0)
	outputCount = connect_to_server(pattern.split(" "), unittestmode=1)
	for node in outputCount:
		nodeCount.append(node['count'])
	print("The line count from local greps on each vm was:")
	print(lineCount)
	assert(nodeCount == lineCount)
	print("Client-Server Unit test passed")

def check_client_pattern_on_servers_with_file(pattern):
	nodeCount = []
	lineCount = []
	grepStart = 'grep -c ' + pattern + ' /home/mp1/vm'
	print("===========================================================================================")
	print("Running unit test on the pattern: " + pattern + " : on all vm logs")
	print("===========================================================================================")
	for i, vmNum in enumerate(vmNums):
		try:
			lineCount.append(int((subprocess.check_output(['ssh', 'dchen51@fa18-cs425-g45-{}.cs.illinois.edu'.format(vmNum), grepStart + str(i+1) + '.log'])).strip().decode('utf-8')))
		except:
			lineCount.append(0)
	outputCount = connect_to_server(pattern.split(" "), unittestmode=1)
	for node in outputCount:
		nodeCount.append(node['count'])
	print("The line count from local greps on each vm was:")
	print(lineCount)
	if(nodeCount == lineCount):
		return True
	else:
		return False

if __name__ == '__main__':
	which_test = input("1 very frequent pattern, 2 frequent pattern, 3 rare pattern, 4 for more regular expressions, 5 for a pattern with no matches, 6 to use a file full of valid grep commands : ")
	if which_test == '1':
		check_client_pattern_on_servers('2')
	elif which_test == '2':
		check_client_pattern_on_servers('300')
	elif which_test == '3':
		check_client_pattern_on_servers('-e abc -e bca -e zazz')
	elif which_test == '4':
		check_client_pattern_on_servers('-e ..00..')
	elif which_test == '5':
		check_client_pattern_on_servers('!')
	elif which_test == '6':
		f = open('unittestpatterns.log','r')
		content = f.readlines()
		content = [line.strip() for line in content] 
		failedLines = []
		count = 0
		totalCount = 0
		for i, pattern in enumerate(content):
			totalCount += 1
			if check_client_pattern_on_servers_with_file(pattern):
				count +=1
				print("Unit test with the pattern : " + pattern + " : has passed\n")
			else:
				failedLines.append(i + 1)
				print("Unit test with the pattern : " + pattern + " : has failed\n")
		for i in failedLines:
			print("The test has failed on line : " + i)
		print("Unit test has passed " + str(count) +  " tests out of " + str(totalCount))

		
		
