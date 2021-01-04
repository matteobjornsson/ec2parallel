import random, time, sys
import ssl, smtplib, os, json
from io import StringIO
import numpy as np
from numpy import savetxt
from itertools import chain, combinations
import multiprocessing, time

final_size = 100
cycles = 10

def check_sum(S, counts, target):
	for i1 in range(counts[1]+1):
		for i2 in range(counts[2]+1):
			for i3 in range(counts[3]+1):
				for i4 in range(counts[4]+1):
					for i5 in range(counts[5]+1):
						for i6 in range(counts[6]+1):
							for i7 in range(counts[7]+1):
								for i8 in range(counts[8]+1):
									for i9 in range(counts[9]+1):
										# print([i1, i2, i3, i4, i5, i6, i7, i8, i9])
										sum = i1*1 + i2*2 + i3*3 + i4*4 + i5*5 + i6*6+ i7*7 + i8*8 + i9*9
										if sum == target:
#											print(
#												"1 + "*i1 +
#												"2 + "*i2 +
#												"3 + "*i3 + 
#												"4 + "*i4 + 
#												"5 + "*i5 + 
#												"6 + "*i6 + 
#												"7 + "*i7 + 
#												"8 + "*i8 + 
#												"9 + "*i9 +
#												"= " + str(target)
#												) 
											return True
	return False

def subsets(array):
	if not array:
		return
	else:
		length = len(array)
		for max_int in range(0x1 << length):
			subset = []
			for i in range(length):
				if max_int & (0x1 << i):
					subset.append(array[i])
			yield subset

def check_subsets(array, target):
	for i in subsets(array):
		if sum(i) == target:
#			print(i)
			return True
#	print("no return")
	return False

def SSUM(size, final_size, cycles):
	S = [random.randint(1,9) for i in range(size)]
	target = random.randint(1,size)

	counts = [0 for i in range(10)]
	for i in range(10):
		counts[i] = S.count(i)

	start1 = time.time()
	check = check_sum(S,counts, target)
	elapsed1 = time.time() - start1


	start2 = time.time()
	check2 = check_subsets(S, target)
	elapsed2 = time.time() - start2
	data.append([size, elapsed1, elapsed2])
	print(len(data), "of", final_size*cycles)

def send_email(receiver_email: str, msg: str):
    context = ssl.create_default_context()
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mountain.project.python@gmail.com"  # Enter your address
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, 'nopasswordforyou')
        server.sendmail(sender_email, receiver_email, msg.encode('utf-8'))


manager = multiprocessing.Manager()
data = manager.list()
start = time.time()
pool = multiprocessing.Pool()
for j in range(1, final_size+1):
    for i in range(cycles):
        pool.apply_async(SSUM, args=(j,final_size, cycles))
pool.close()
pool.join()

final_data = np.array(data)
#
#temp = []
#for i in range(len(final_data)):
#	temp.append(','.join([str(x) for x in final_data[i]]))
#msg = '\n'.join(temp)
#
np.savetxt('data.csv', data, delimiter=',')

#send_email('matteobjornsson@gmail.com', msg)

#print("Fast way: ", elapsed1)
#print("Slow Way: ", check2, ":", elapsed2)
#
#print(S)
#if check:
#	print("sum found")
#else:
#	print("no sum")
