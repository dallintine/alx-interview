#!/usr/bin/python3
import sys

def print_usage_and_exit(message, status=1):
    print(message)
    sys.exit(status)

# Validate command-line arguments
if len(sys.argv) != 2:
    print_usage_and_exit("Usage: nqueens N")

try:
    N = int(sys.argv[1])
except ValueError:
    print_usage_and_exit("N must be a number")

if N < 4:
    print_usage_and_exit("N must be at least 4")

# Function to check if a queen placement is safe
def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

# Backtracking function to solve the N-Queens problem
def solve_nqueens(board, row):
    if row == N:
        print([[i, board[i]] for i in range(N)])
        return
    for col in range(N):
        if is_safe(board, row, col):
            board[row] = col
            solve_nqueens(board, row + 1)
            board[row] = -1

# Initialize the board and start the solution process
board = [-1] * N
solve_nqueens(board, 0)

