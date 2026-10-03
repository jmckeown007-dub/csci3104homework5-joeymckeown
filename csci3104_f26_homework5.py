'''Homework 5. Copy and paste your code from the earlier MSP algs and 
then implement Kadane's algorithm. Functions for timing your code have 
been provided.

Usage: python csci3104_f26_homework5.py <filename>
Example: python csci3104_f26_homework5.py csci3104_f26_max_subarray_data_hw5/num_array_100.txt
'''

import timeit
import math
import matplotlib.pyplot as plt
from pathlib import Path
from tabulate import tabulate

def max_subarray_enumeration(A):
	'''
	Computes the value of a maximum subarray of the input array by enumeration.

	Args:
		A (list): An array of n >=1 integers.

	Returns:
		The sum of the elements in a maximum subarray of A.
	'''
	# TODO: paste your solution from HW1 in this function
	n = len(A)
	best_sum = 0
	
	for i in range(n): # left endpoint
		for j in range(i, n): # right endpoint
			curr_sum = 0
			for k in range(i, j+1): # calculates every possible subarray with third loop which is what makes this O(n^3)
				curr_sum += A[k]
			if curr_sum > best_sum:
				best_sum = curr_sum
	
	return best_sum 



def max_subarray_iteration(A):
	'''
	Computes the value of a maximum subarray of the input array by iteration.

	Args:
		A (list): An array of n >= 1 integers.

	Returns:
		The sum of the elements in a maximum subarray of A.
	'''
	# TODO: paste your solution from HW1 in this function
	n = len(A)
	best_sum = 0
	
	for i in range(n): # left endpoint
		curr_sum = 0
		for j in range(i, n): # right endpoint
			curr_sum += A[j] # as the subarray grows from left to right from i, this will 
			if curr_sum > best_sum: # ensure that the best/max subarray is found with any given left endpoint
				best_sum = curr_sum
	
	return best_sum


def find_max_crossing_subarray(A, low, mid, high):
	'''
	Finds the maximum sum subarray crossing the midpoint and returns its sum.

	Args:
		A (list): An array of n >= 1 integers.
		low (int): The lowest index of A that should be searched.
		mid (int): The middle index of the array, included in the crossing.
		high (int): The greatest index of A that should be searched.

	Returns:
		The sum of elements in the maximum crossing subarray of A.
	'''
	# TODO: paste your solution from HW2 in this function
	left_best_sum = -math.inf # set sums to negative infinity so that any sum is larger
	right_best_sum = -math.inf
	
	i = mid # this will be the left index of the subarray
	j = mid + 1 # this will be the right index of the subarray
	
	curr_sum = 0
	
	for x in range(mid, low - 1, -1):
		curr_sum += A[x]
		if curr_sum > left_best_sum:
			left_best_sum = curr_sum
			i = x
	
	
	curr_sum = 0
	
	for y in range(mid + 1, high + 1):
		curr_sum += A[y]
		if curr_sum > right_best_sum:
			right_best_sum = curr_sum
			j = y
	
	s = left_best_sum + right_best_sum
	
	return i,j,s


def max_subarray_DC(A, low=0, high=None):
	'''
	Computes the value of a maximum subarray of the input array by 
	divide-and-conquer.

	The parameter low is given a default value of 0, and high a default 
	value of None. If high has a value of None, it is assigned a value equal 
	to the length of A. This makes it possible to make the first call to this 
	function from time_alg, since calling max_subarray_DC(A) is now equivalent 
	to max_subarray_DC(A, 0, len(A)).

	Args:
		A (list): An array of n >= 1 integers.
		low (int, optional): The lowest index of A that should be searched. 
			Defaults to 0.
		high (int, optional): The highest indec of A that should be searched. 
			Defaults to None.

	Returns:
		The sum of the elements in a maximum subarray of A.
	'''
	if high is None:
		high = len(A) - 1
	# TODO: paste your solution from HW2 in this function
	if low == high:
		return low, high, A[low]
	
	mid = (low + high) // 2
	
	left_low, left_high, left_sum = max_subarray_DC(A, low, mid)
	right_low, right_high, right_sum = max_subarray_DC(A, mid + 1, high)
	cross_low, cross_high, cross_sum = find_max_crossing_subarray(A, low, mid, high)

	
	if left_sum >= right_sum and left_sum >= cross_sum:
		return left_low, left_high, left_sum
	elif right_sum >= left_sum and right_sum >= cross_sum:
		return right_low, right_high, right_sum
	else:
		return cross_low, cross_high, cross_sum


def max_subarray_kadane(A):
	'''
	Computes the value of a maximum subarray of the input array using 
	Kadane's algorithm.

	Args:
		A (list): An array of n >= 1 integers.

	Returns:
		The sum of the elements in a maximum subarray of A.
	'''
	# TODO: your new code here
	curr_sum = 0
	max_sum = -math.inf
	for n in A:
		curr_sum += n
		if curr_sum < 0:
			curr_sum = 0
		max_sum = max(max_sum, curr_sum)


	return max_sum


def time_alg(alg, A):
	'''
	Runs an algorithm for the maximum subarray problem on a test array 
	and times how long it takes.

	Args:
		alg (callable): An algorithm for the maximum subarray problem.
		A (list): An array of n >= 1 integers

	Returns:
		A pair consisting of the value of alg(A) and the time needed 
			to execute alg(A) in seconds. 
	'''
	start_time = timeit.default_timer() #get the start time in seconds
	max_subarray_val = alg(A)
	end_time = timeit.default_timer() #get the end time in seconds
	return max_subarray_val, end_time - start_time


def scatter_plot(x, y1, y2):

	fig, ax = plt.subplots(1,2, layout="tight")

	fig.suptitle("Algorithms' Runtimes")

	ax[0].scatter(x, y1[0], color='r', label='Iteration') 
	ax[0].scatter(x, y1[1], color='b', label='Divide and Conquer')
	ax[0].scatter(x, y1[2], color='g', label="Kadane's")
	ax[0].set_title("Iteration, Divide and Conquer, and Kadane")
	ax[0].set_xlabel("Array Size")
	ax[0].set_ylabel("Runtime in Milliseconds")
	ax[0].legend()

	ax[1].scatter(x,y2) 
	ax[1].set_title("Enumeration")
	ax[1].set_xlabel("Array Size")
	ax[1].set_ylabel("Runtime in Milliseconds")

	plt.tight_layout()
	plt.savefig('algorithm_runtimes.png', bbox_inches="tight")

	plt.show()


def main():
	alg_list = [max_subarray_enumeration, max_subarray_iteration, 
			max_subarray_DC, max_subarray_kadane]

	headers = ['','Enumeration', 'Iteration', 'Divide and Conquer', 'Kadane']
	rows = []

	enumeration_times = []
	iteration_times = []
	divide_and_conquer_times = []
	kadane_times = []
	
	"""New implementation for reading every text file at once rather than using sys.argv[1]"""
	array_size = []

	p = Path(r"csci3104_f26_max_subarray_data_hw5") # this has to be in same directory as this program (csci3104_f26_homework5.py) or else it won't be able to find it

	for f in sorted(p.glob('*.txt'), key=lambda f:int(f.stem.rsplit('_')[2])):
		if f.is_file() and f.suffix.lower() == '.txt':
			with open(f, 'r', encoding='utf-8') as filename:

				A = [int(num) for num in filename.readline().strip().split(' ')]
				num_count = f.stem.split('_')[2]

				row = [f'Size {num_count} Array']
				array_size.append(int(num_count))

				print(f"Algorithm results for array with {num_count} elements:\n")
				print(f"============================================\n\n")

				for alg in alg_list:

				
						algorithm_result = time_alg(alg,A)
						row.append(algorithm_result[1] * 1000)

						if alg == max_subarray_enumeration:
							print(f"\tEnumeration Best Sum: {algorithm_result[0]}\n")
							print(f"\tEnumeration Running Time: {algorithm_result[1]}\n")
							print(f"\t============================================\n\n")
							enumeration_times.append(algorithm_result[1] * 1000)
				
						elif alg == max_subarray_iteration:
							print(f"\tIteration Best Sum: {algorithm_result[0]}\n")
							print(f"\tIteration Running Time: {algorithm_result[1]}\n")
							print(f"\t============================================\n\n")
							iteration_times.append(algorithm_result[1] * 1000)
				
						elif alg == max_subarray_DC:
							print(f"\tDivide and Conquer Best Sum: {algorithm_result[0][2]}\n")
							print(f"\tDivide and Conquer Running Time: {algorithm_result[1]}\n")
							print(f"\t============================================\n\n")
							divide_and_conquer_times.append(algorithm_result[1] * 1000)
				
						elif alg == max_subarray_kadane:
							print(f"\tKadane's Best Sum: {algorithm_result[0]}\n")
							print(f"\tKadane's Running Time: {algorithm_result[1]}\n")
							print(f"\t============================================\n\n")
							print(f"\t============================================\n\n")
							kadane_times.append(algorithm_result[1] * 1000)
				
						#print(time_alg(alg, A))
				
				rows.append(row)
		else:
			print(f"{f.name} is not a valid text file")


	print("\nTable of Algorithm Runtimes (in milliseconds): \n")
	print(tabulate(rows, headers = headers, tablefmt='fancy_grid'))

	scatter_one_values = [iteration_times, divide_and_conquer_times, kadane_times]
	scatter_two_values = enumeration_times

	scatter_plot(array_size, scatter_one_values, scatter_two_values)
	"""
	filename = sys.argv[1]
	with open(filename, 'r') as f:
		A = [int(num) for num in f.readline().strip().split(' ')]
	"""

	




if __name__ == '__main__':
	main()