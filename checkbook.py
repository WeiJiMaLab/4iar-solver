from collections import defaultdict
import json
from copy import deepcopy

from utils import *


def prepare_legal_patterns():
    patterns = {}
    two_in_a_row = defaultdict(set)
    three_in_a_row = defaultdict(set)
    four_in_a_row = defaultdict(list)
    reversed_three_in_a_row = defaultdict(set)
    reversed_four_in_a_row = defaultdict(list)

    prob_four_in_a_row = []
    for y in range(9):
        for x in range(4):
            prob_four_in_a_row.append([(x, y), (x, y + 1), (x, y + 2), (x, y + 3)])
        prob_four_in_a_row.append([(k, y) for k in range(4)])
        prob_four_in_a_row.append([(k, y + k) for k in range(4)])
        prob_four_in_a_row.append([(k, y + 3 - k) for k in range(4)])

    all_three_in_a_row = []
    all_four_in_a_row = []
    all_groups = defaultdict(list)
    for pos in prob_four_in_a_row:
        if all([is_legal(p) for p in pos]):
            idxes = [coordinate_to_index(*p) for p in pos]
            for (i, j) in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
                two_in_a_row[idxes[i]].add(idxes[j])
                two_in_a_row[idxes[j]].add(idxes[i])
            for (i, j, k) in [(0, 1, 2), (0, 2, 3), (0, 1, 3), (1, 2, 3)]:
                all_three_in_a_row.append((idxes[i], idxes[j], idxes[k]))
                three_in_a_row[idxes[i]].add((idxes[j], idxes[k]))
                three_in_a_row[idxes[j]].add((idxes[i], idxes[k]))
                three_in_a_row[idxes[k]].add((idxes[i], idxes[j]))
                reversed_three_in_a_row[f'{idxes[j]}-{idxes[k]}'].add(idxes[i])
                reversed_three_in_a_row[f'{idxes[i]}-{idxes[k]}'].add(idxes[j])
                reversed_three_in_a_row[f'{idxes[i]}-{idxes[j]}'].add(idxes[k])

            all_four_in_a_row.append(idxes)
            all_groups[idxes[0]].append(idxes)
            all_groups[idxes[1]].append(idxes)
            all_groups[idxes[2]].append(idxes)
            all_groups[idxes[3]].append(idxes)
            four_in_a_row[idxes[0]].append([idxes[1], idxes[2], idxes[3]])
            four_in_a_row[idxes[1]].append([idxes[0], idxes[2], idxes[3]])
            four_in_a_row[idxes[2]].append([idxes[0], idxes[1], idxes[3]])
            four_in_a_row[idxes[3]].append([idxes[0], idxes[1], idxes[2]])
            reversed_four_in_a_row[f'{idxes[1]}-{idxes[2]}-{idxes[3]}'].append(idxes[0])
            reversed_four_in_a_row[f'{idxes[0]}-{idxes[2]}-{idxes[3]}'].append(idxes[1])
            reversed_four_in_a_row[f'{idxes[0]}-{idxes[1]}-{idxes[3]}'].append(idxes[2])
            reversed_four_in_a_row[f'{idxes[0]}-{idxes[1]}-{idxes[2]}'].append(idxes[3])

    patterns['all_three_in_a_row'] = all_three_in_a_row
    patterns['all_four_in_a_row'] = all_four_in_a_row
    patterns['all_groups'] = all_groups
    patterns['two_in_a_row'] = {k: list(v) for k, v in two_in_a_row.items()}
    patterns['three_in_a_row'] = {k: [list(i) for i in v] for k, v in three_in_a_row.items()}
    patterns['four_in_a_row'] = four_in_a_row
    patterns['reversed_three_in_a_row'] = {k: list(v) for k, v in reversed_three_in_a_row.items()}
    patterns['reversed_four_in_a_row'] = reversed_four_in_a_row
    json.dump(patterns, open('patterns.json', 'w'), indent=4)


def load_pattern_book():
    book = json.load(open('patterns.json', 'r'))

    all_groups = {}
    for k, v in book['all_groups'].items():
        all_groups[int(k)] = v

    two_in_a_row = {}
    for k, v in book['two_in_a_row'].items():
        two_in_a_row[int(k)] = v

    three_in_a_row = {}
    for k, v in book['three_in_a_row'].items():
        three_in_a_row[int(k)] = v

    four_in_a_row = {}
    for k, v in book['four_in_a_row'].items():
        four_in_a_row[int(k)] = v

    reversed_three_in_a_row = {}
    for k, v in book['reversed_three_in_a_row'].items():
        reversed_three_in_a_row[tuple([int(s) for s in k.split('-')])] = v

    reversed_four_in_a_row = {}
    for k, v in book['reversed_four_in_a_row'].items():
        reversed_four_in_a_row[tuple([int(s) for s in k.split('-')])] = v

    book['all_groups'] = all_groups
    book['two_in_a_row'] = two_in_a_row
    book['three_in_a_row'] = three_in_a_row
    book['four_in_a_row'] = four_in_a_row
    book['reversed_three_in_a_row'] = reversed_three_in_a_row
    book['reversed_four_in_a_row'] = reversed_four_in_a_row

    return book


if __name__ == '__main__':
    # prepare_legal_patterns()
    pattern_book = load_pattern_book()
    print(1)