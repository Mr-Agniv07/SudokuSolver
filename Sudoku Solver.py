from genericpath import exists
from typing import Tuple, List
# No other imports allowed

# PART OF THE DRIVER CODE

def input_sudoku() -> List[List[int]]:
	"""Function to take input a sudoku from stdin and return
	it as a list of lists.
	Each row of sudoku is one line.
	"""
	sudoku= list()
	for _ in range(9):
		row = list(map(int, input().rstrip(" ").split(" ")))
		sudoku.append(row)
	return sudoku

def print_sudoku(sudoku:List[List[int]]) -> None:
	"""Helper function to print sudoku to stdout
	Each row of sudoku in one line."""
	
	for i in range(9):
		for j in range(9):
			print(sudoku[i][j], end = " ")
		print()

def get_block_num(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
    row,col=pos[0],pos[1]
    if int(row)<=3:
        if int(col)<=3:
            return 1
        if int(col)>3 and int(col)<=6:
            return 2
        if int(col)<=9 and int(row)>6:
            return 3
    if int(row)>3 and int(row)<=6:
        if int(col)<=3:
            return 4
        if int(col)>3 and int(col)<=6:
            return 5
        if int(col)<=9 and int(row)>6:
            return 6
    if int(row)>6 and int(row)<=9:
        if int(col)<=3:
            return 7
        if int(col)>3 and int(col)<=6:
            return 8
        if int(col)<=9 and int(row)>6:
            return 9
    return

def get_position_inside_block(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	"""This function takes parameter position
	and returns the index of the position inside the corresponding block.
	"""
	row,col=pos[0],pos[1]
	if col%3==0:
		if row%3==0:
			return 9
		if (row+1)%3==0:
			return 6
		if (row-1)%3==0:
			return 3
	if (col+1)%3==0:
		if row%3==0:
			return 8
		if (row+1)%3==0:
			return 5
		if (row-1)%3==0:
			return 2
	if (col-1)%3==0:
		if row%3==0:
			return 7
		if (row+1)%3==0:
			return 4
		if (row-1)%3==0:
			return 1	


def get_block(sudoku:List[List[int]], x: int) -> List[int]:
	"""This function takes an integer argument x and then
	returns the x^th block of the Sudoku. Note that block indexing is
	from 1 to 9 and not 0-8
	"""
	# we have x
	L=[]
	M=[]
	for i in sudoku:
		M.append(i)
	if x==1:
		for i in range(3):
			for j in range(3):
				L.append(M[i][j])
		return L
	if x==2:
		for i in range(3):
			for j in range(3,6):
				L.append(M[i][j])
		return L
	if x==3:
		for i in range(3):
			for j in range(6,9):
				L.append(M[i][j])
		return L
	if x==4:
		for i in range(3,6):
			for j in range(3):
				L.append(M[i][j])
		return L
	if x==5:
		for i in range(3,6):
			for j in range(3,6):
				L.append(M[i][j])
		return L
	if x==6:
		for i in range(3,6):
			for j in range(6,9):
				L.append(M[i][j])
		return L
	if x==7:
		for i in range(6,9):
			for j in range(3):
				L.append(M[i][j])
		return L
	if x==8:
		for i in range(6,9):
			for j in range(3,6):
				L.append(M[i][j])
		return L
	if x==9:
		for i in range(6,9):
			for j in range(6,9):
				L.append(M[i][j])
		return L			
	
	

def get_row(sudoku:List[List[int]], i: int)-> List[int]:
	"""This function takes an integer argument i and then returns
	the ith row. Row indexing have been shown above.
	"""
	return sudoku[i-1] 

def get_column(sudoku:List[List[int]], x: int)-> List[int]:
	"""This function takes an integer argument i and then
	returns the ith column. Column indexing have been shown above.
	"""
	M=[]
	for i in sudoku:
		M.append(i[x-1])
			
	return M

def find_first_unassigned_position(sudoku : List[List[int]]) -> Tuple[int, int]:
	"""This function returns the first empty position in the Sudoku. 
	If there are more than 1 position which is empty then position with lesser
	row number should be returned. If two empty positions have same row number then the position
	with less column number is to be returned. If the sudoku is completely filled then return `(-1, -1)`.
	"""
	M=[]
	N=[]
	for i in sudoku:
		for j in i:
			if j==0:
				k=i.index(j)
				l=sudoku.index(i)
				M.append(k)
				N.append(l)
				break
	if len(M)!=0 and len(N)!=0:
		t=(N[0]+1,M[0]+1)
		return t
	else:
		return (-1,-1)


def valid_list(lst: List[int])-> bool:
	"""This function takes a lists as an input and returns true if the given list is valid. 
	The list will be a single block , single row or single column only. 
	A valid list is defined as a list in which all non empty elements doesn't have a repeating element.
	"""
	for a in lst:
		cc=0
		for b in range(len(lst)):
			if lst[b]==a:
				if a!=0:
					cc+=1
		if cc>1:
			return False
	
	return True



def valid_sudoku(sudoku:List[List[int]])-> bool:
	"""This function returns True if the whole Sudoku is valid.
	"""
	for i in sudoku:
		if valid_list(i)==False:
			return False
	COL=[]
	ele=[]
	for i in range(len(sudoku)):
		for j in sudoku:
			ele.append(j[i])
			if len(ele)==9:
				COL.append(ele)
				ele=[]
	for k in COL:
		if valid_list(k)==False:
			return False
	return True


def get_candidates(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[int]:
	"""This function takes position as argument and returns a list of all the possible values that 
	can be assigned at that position so that the sudoku remains valid at that instant.
	"""
	row=pos[0]
	col=pos[1]
	ui=get_block_num(sudoku,(pos[0],pos[1]))
	w=get_block(sudoku,ui)
	L=[]
	COL=[]
	K=[]
	ele=[]
	for o in range (0,10):
		K.append(o)
	for i in range(len(sudoku)):
		for j in sudoku:
			ele.append(j[i])
			if len(ele)==9:
				COL.append(ele)
				ele=[]
	for j in K:
		if j!=0:		
			if (j not in sudoku[row-1]) and (j not in COL[col-1]) and (j not in w):
				L.append(j)
			if L.count(0)>0:
				L.remove(0)
			
	L.sort()
	return L

				
	

def make_move(sudoku:List[List[int]], pos:Tuple[int, int], num:int) -> List[List[int]]:
	"""This function fill `num` at position `pos` in the sudoku and then returns
	the modified sudoku.
	"""
	sudoku[pos[0]-1][pos[1]-1]=num

	return sudoku

def undo_move(sudoku:List[List[int]], pos:Tuple[int, int]):
	"""This function fills `0` at position `pos` in the sudoku and then returns
	the modified sudoku. In other words, it undoes any move that you 
	did on position `pos` in the sudoku.
	"""
	sudoku[pos[0]-1][pos[1]-1]=0
	
	return sudoku

def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:
	""" This is the main Sudoku solver. This function solves the given incomplete Sudoku and returns 
	true as well as the solved sudoku if the Sudoku can be solved i.e. after filling all the empty positions the Sudoku remains valid.
	It return them in a tuple i.e. `(True, solved_sudoku)`.
	However, if the sudoku cannot be solved, it returns False and the same sudoku that given to solve i.e. `(False, original_sudoku)`
	"""
	while find_first_unassigned_position(sudoku)!=(-1,-1):
		print(find_first_unassigned_position(sudoku))
		k=find_first_unassigned_position(sudoku)
		L=get_candidates(sudoku,(k[0],k[1]))
		for i in L:
			make_move(sudoku,(k[0],k[1]),i)
			break
	if (valid_sudoku==True) and (find_first_unassigned_position(sudoku)==(-1,-1)):
		return (True,sudoku)
	return (False,sudoku)



# Following is the driver code
# you can edit the following code to check your performance.
if __name__ == "__main__":

	# Input the sudoku from stdin
	sudoku = input_sudoku()
	# Try to solve the sudoku
	possible, sudoku = sudoku_solver(sudoku)

	# Check if it could be solved
	if possible:
		print("Found a valid solution for the given sudoku :)")
		print_sudoku(sudoku)

	else:
		print("The given sudoku cannot be solved :(")
		print_sudoku(sudoku)