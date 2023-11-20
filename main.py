#!/bin/python3

import numpy as np

def gen_empty():
    return np.zeros((9, 9), dtype=int)

def is_valid(board, row, col, num):
    return (
        not np.any(board[row, :] == num) and
        not np.any(board[:, col] == num) and
        not np.any(board[(row // 3) * 3 : (row // 3 + 1) * 3, (col // 3) * 3 : (col // 3 + 1) * 3] == num)
    )

def solve(board):
    empty = np.where(board == 0)
    
    if len(empty[0]) == 0:
        return True

    row, col = empty[0][0], empty[1][0]
    numbers = np.random.permutation(9) + 1

    for num in numbers:
        if is_valid(board, row, col, num):
            board[row, col] = num

            if solve(board):
                return True

            board[row, col] = 0

    return False

def is_unique(board):
    copy_board = board.copy()
    empty = np.where(copy_board == 0)
    
    if len(empty[0]) == 0:
        return 1

    row, col = empty[0][0], empty[1][0]
    count = 0

    for num in range(1, 10):
        if is_valid(copy_board, row, col, num):
            copy_board[row, col] = num
            count += is_unique(copy_board)
            if count > 1:
                return False
            
            copy_board[row, col] = 0

    return count == 1

def gen_full():
    board = gen_empty()
    solve(board)
    return board

def gen_puzzle(n_cells_to_leave):
    solution = gen_full()
    puzzle = solution.copy()

    non_empty_cells = np.column_stack(np.where(puzzle != 0))
    np.random.shuffle(non_empty_cells)

    for _ in range(np.count_nonzero(puzzle != 0) - n_cells_to_leave):
        row, col = non_empty_cells[_]
        temp_value = puzzle[row, col]
        puzzle[row, col] = 0

        if not is_unique(puzzle):
            puzzle[row, col] = temp_value

    return puzzle, solution

if __name__ == "__main__":
    board = gen_puzzle(25)
    print("Generated Puzzle:")
    print(board[0])
    print("Solution:")
    print(board[1])