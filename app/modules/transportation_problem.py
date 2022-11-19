import sys
from icecream import ic

class transportationProblem:

	def __init__(self, supply, demand, cost_matrix):

		self.supply = supply
		self.demand = demand        
		self.cost_matrix = cost_matrix
		self.ans = []
		self.total_cost = 0

	def getLowest(self, arr):

		temp_min = 0
		for i in range(len(arr)):
			if arr[i] < arr[temp_min]:
				temp_min = i

		return arr[temp_min]

	def getSecondLowest(self, arr, l):

		min_ele = arr.index(l)

		temp_min = 0  
		if min_ele == 0:
			temp_min = 1

		for i in range(len(arr)):
			if arr[i] < arr[temp_min] and i!=min_ele:
				temp_min = i

		return arr[temp_min]

	def transpose(self, arr):
			
		temp = [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]
		return temp

	def isBalanced(self): # To check if the transportation problem is balanced

		self.balanced = False
		if sum(self.demand) == sum(self.supply):
			self.balanced = True

	def vam(self): # To find intial feasible solution using VAM (Vogel's Approximation Method)
		
		cost_matrix = [[self.cost_matrix[i][j] for j in range(len(self.cost_matrix[0]))] for i in range(len(self.cost_matrix))]
		
		supply = [i for i in self.supply]
		demand = [i for i in self.demand]

		sd_left = len(supply) + len(demand)

		while sd_left>1:

			row_diff = []
			col_diff = []

			for j in cost_matrix:

				min_ele = self.getLowest(j)
				sec_min_ele = self.getSecondLowest(j, min_ele)
				
				row_diff.append( sec_min_ele - min_ele )
				
			t_cost_matrix = self.transpose(cost_matrix)

			for j in t_cost_matrix:

				min_ele = self.getLowest(j)
				sec_min_ele = self.getSecondLowest(j, min_ele)

				col_diff.append( sec_min_ele - min_ele )
				
			max_row_diff = max(row_diff)
			max_col_diff = max(col_diff)

			# ic(row_diff, col_diff)

			if max_row_diff > max_col_diff:

				# ic("Case 1")

				row_index = row_diff.index(max_row_diff)
				# ic(row_index)
				row = cost_matrix[row_index]
				# ic(row)
				row_min = min(row)
				row_min_index = row.index(row_min)
				# ic(row_min, row_min_index)

				if supply[row_index] > demand[row_min_index]:
					# ic()
					self.ans.append([ demand[row_min_index] , row_min , (row_index, row_min_index)])
							
					supply[row_index] -= demand[row_min_index]
					demand[row_min_index] = 0

					for i in cost_matrix:
						i[row_min_index] = sys.maxsize
					
					sd_left -= 1

				elif supply[row_index] < demand[row_min_index]:
					# ic()
					self.ans.append([ supply[row_index] , row_min , (row_index, row_min_index)])

					demand[row_min_index] -= supply[row_index]
					supply[row_index] = 0

					cost_matrix[row_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 1

				else:
					# ic()
					self.ans.append([ supply[row_index] , row_min , (row_index, row_min_index)])

					demand[row_min_index] = 0
					supply[row_index] = 0

					for i in cost_matrix:
						i[row_min_index] = sys.maxsize

					cost_matrix[row_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 2

				# ic(cost_matrix)

			else:
					
				col_index = col_diff.index(max_col_diff)
				col = t_cost_matrix[col_index]
				col_min = min(col)
				col_min_index = col.index(col_min)

				if supply[col_min_index] > demand[col_index]:

					self.ans.append([ demand[col_index] , col_min , (col_min_index, col_index)])

					supply[col_min_index] -= demand[col_index]
					demand[col_index] = 0

					for i in cost_matrix:
						i[col_index] = sys.maxsize

					sd_left -= 1

				elif supply[col_min_index] < demand[col_index]:

					self.ans.append([ supply[col_min_index] , col_min , (col_min_index, col_index)])

					demand[col_index] -= supply[col_min_index]
					supply[col_min_index] = 0

					cost_matrix[col_min_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 1

				else:

					self.ans.append([ supply[col_min_index] , col_min , (col_min_index, col_index)])

					demand[col_index] = 0
					supply[col_min_index] = 0

					for i in cost_matrix:
						i[col_index] = sys.maxsize

					cost_matrix[col_min_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 1

			# ic(self.ans)
		return self.ans

	def getTotalCost(self):

		for i in self.ans:
			self.total_cost += i[0] * i[1]

		return self.total_cost
