import os
import json

from search import search
from checkbook import load_pattern_book


Puzzle_Path = './shucheng_puzzles'
Max_Depth = 6 * 2


def read_puzzles_from_file():
    puzzles = {}
    buff = {}
    is_first = True
    with open(os.path.join(Puzzle_Path, 'puzzles')) as f:
        for line in f:
            line = line.strip()
            if line.startswith('case'):
                if is_first:
                    is_first = False
                else:
                    puzzles[pid] = buff
                    buff = {}
                pid = line[:-1].split(' ')[-1]
            elif line.startswith('black'):
                black_pieces = json.loads(line.split(' = ')[-1])
                buff['black_pieces'] = black_pieces
            elif line.startswith('white'):
                white_pieces = json.loads(line.split(' = ')[-1])
                buff['white_pieces'] = white_pieces
            elif line.startswith('solution'):
                solutions = json.loads(line.split(' = ')[-1])
                buff['solutions'] = solutions
        puzzles[pid] = buff
    return puzzles


def search_and_save(black_pieces, white_pieces, pattern_book, max_depth, pid, solutions):
    forced_win_cand, all_forced_win_paths, num_node, search_time = search(black_pieces, white_pieces, pattern_book, max_depth)
    results = {
        'solutions': [fwc[0] for fwc in forced_win_cand],
        'ground truth': solutions,
        'paths': all_forced_win_paths,
        'search_time': search_time,
        'num. search nodes': num_node
    }
    succ = set(results['solutions']) == set(results['ground truth'])
    json.dump(results, open(os.path.join(Puzzle_Path, f'{pid}.json'), 'w'), indent=4)
    print(f"Puzzle: {pid} finished! Time: {search_time}, Num. Nodes: {num_node}\n")
    return succ


if __name__ == '__main__':
    pattern_book = load_pattern_book()
    puzzles = read_puzzles_from_file()
    standard_inputs = [{
        'black_pieces': puzzles[pid]['black_pieces'],
        'white_pieces': puzzles[pid]['white_pieces'],
        'pattern_book': pattern_book,
        'max_depth': Max_Depth,
        'pid': pid,
        'solutions': puzzles[pid]['solutions']
    } for pid in puzzles]

    num_succ = 0
    for inputs in standard_inputs:
        num_succ += search_and_save(**inputs)
    print(f"Accuracy: {round(100 * num_succ / len(standard_inputs), 2)}%")




