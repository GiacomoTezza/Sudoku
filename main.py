#!/bin/python3

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm
import argparse

progress_counter = 0

def gen_empty():
    return np.zeros((9, 9), dtype=int)

def is_valid(board, row, col, num):
    return (
        not np.any(board[row, :] == num) and
        not np.any(board[:, col] == num) and
        not np.any(board[(row // 3) * 3 : (row // 3 + 1) * 3, (col // 3) * 3 : (col // 3 + 1) * 3] == num)
    )

def solve(board):
    global progress_counter
    empty = np.where(board == 0)
    
    if len(empty[0]) == 0:
        return True

    row, col = empty[0][0], empty[1][0]
    numbers = np.random.permutation(9) + 1

    for num in numbers:
        if is_valid(board, row, col, num):
            board[row, col] = num
            progress_counter += 1
            if solve(board):
                return True

            board[row, col] = 0

    return False

def is_unique(board):
    global progress_counter
    copy_board = board.copy()
    empty = np.where(copy_board == 0)
    
    if len(empty[0]) == 0:
        return 1

    row, col = empty[0][0], empty[1][0]
    count = 0

    for num in range(1, 10):
        if is_valid(copy_board, row, col, num):
            copy_board[row, col] = num
            progress_counter += 1
            count += is_unique(copy_board)
            if count > 1:
                return False
            
            copy_board[row, col] = 0

    return count == 1

def gen_full():
    global progress_counter
    board = gen_empty()
    solve(board)
    progress_counter = 0
    return board

def gen_puzzle(n_cells_to_leave):
    global progress_counter
    solution = gen_full()
    puzzle = solution.copy()

    non_empty_cells = np.column_stack(np.where(puzzle != 0))
    np.random.shuffle(non_empty_cells)

    for _ in tqdm(range(np.count_nonzero(puzzle != 0) - n_cells_to_leave), desc="Generating Puzzle", unit="cell"):
        row, col = non_empty_cells[_]
        temp_value = puzzle[row, col]
        puzzle[row, col] = 0

        if not is_unique(puzzle):
            puzzle[row, col] = temp_value

    progress_counter = 0
    return puzzle, solution

def draw_puzzle(board, output_file):
    image_size = (720, 720)
    cell_size = (80, 80)

    img = Image.new("RGB", image_size, color="white")
    draw = ImageDraw.Draw(img)

    font_size = min(cell_size) // 1.5
    font = ImageFont.load_default()
    font = ImageFont.truetype("./tmp/Montserrat-Regular.ttf", font_size)

    # Draw thicker lines dividing the grid into 9 sectors
    for i in range(1, 9):
        thickness = 2 if i % 3 == 0 else 1  # Thicker lines for every 3rd line
        line_position = i * cell_size[0]
        draw.line([(line_position, 0), (line_position, image_size[1])], fill="black", width=thickness)
        draw.line([(0, line_position), (image_size[0], line_position)], fill="black", width=thickness)

    for i in range(9):
        for j in range(9):
            cell_value = board[i, j]
            cell_position = (j * cell_size[0], i * cell_size[1])
            draw.rectangle([cell_position, (cell_position[0] + cell_size[0], cell_position[1] + cell_size[1])], outline="black")
            if cell_value != 0:
                draw.text((cell_position[0] + cell_size[0] // 2, cell_position[1] + cell_size[1] // 2),
                          str(cell_value), font=font, fill="black", anchor="mm")

    img.save(output_file)

def main():
    parser = argparse.ArgumentParser(description="Sudoku Puzzle Generator")

    parser.add_argument("-n", "--num-cells", type=int, default=30, help="Number of cells to leave in the puzzle (min 17)")
    parser.add_argument("-o", "--output-file", type=str, default="sudoku_puzzle", help="Output image file name")
    args = parser.parse_args()

    if args.num_cells < 17 or args.num_cells > 81:
        parser.error("Number of cells to leave must be between 17 and 81")

    puzzle_board = gen_puzzle(args.num_cells)
    draw_puzzle(puzzle_board[0], args.output_file+".png")
    draw_puzzle(puzzle_board[0], args.output_file+"_solution.png")
    
    print(f"\nGenerated Sudoku saved to {args.output_file}")

if __name__ == "__main__":
    main()
