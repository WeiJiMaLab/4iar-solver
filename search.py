import time

from checkbook import *
from graph import *


def init_groups(black_pieces, white_pieces, group_book):
    # Initialize board
    board = np.zeros((4, 9))
    all_x, all_y = batch_index_to_coordinate(list(range(36)))
    black_x, black_y = batch_index_to_coordinate(black_pieces)
    white_x, white_y = batch_index_to_coordinate(white_pieces)
    board[black_x, black_y] = 1
    board[white_x, white_y] = 2
    print(board)

    # Initialize group state
    state_vec = []
    for pos in group_book["all_four_in_a_row"]:
        x = all_x[pos]
        y = all_y[pos]
        state = board[x, y]
        num_black = np.sum(state == 1)
        num_white = np.sum(state == 2)
        if num_black == 0:
            if num_white == 0:
                state_vec.append(StateIndex["empty"])
            else:
                state_vec.append(StateIndex[f"white-{num_white}"])
        elif num_white == 0:
            state_vec.append(StateIndex[f"black-{num_black}"])
        else:
            state_vec.append(StateIndex["none"])
    state_vec = np.array(state_vec)

    # Build the group-based graph
    empty = []
    for i in range(36):
        if i not in black_pieces and i not in white_pieces:
            empty.append(i)

    graph = Graph(group_book)

    return state_vec, empty, graph


def get_candidates(turn_color, empty, state_vec, graph, remain_steps, is_player):
    opponent_color = "white" if turn_color == "black" else "black"
    offense_3iar_id = StateIndex[f"{turn_color}-3"]
    defense_3iar_id = StateIndex[f"{opponent_color}-3"]

    # player 3-in-a-row -> 4-in-a-row
    off_vtxes = []
    for vid in np.where(state_vec == offense_3iar_id)[0]:
        vertex = graph.vertexes[vid]
        off_vtxes += vertex.get_pieces()
    candidates = list(set(off_vtxes) & set(empty))
    if len(candidates) > 0:
        return [[c, "Force Win"] for c in candidates]

    # stop opponent 3-in-a-row -> 4-in-a-row
    def_vtxes = []
    for vid in np.where(state_vec == defense_3iar_id)[0]:
        vertex = graph.vertexes[vid]
        def_vtxes += vertex.get_pieces()
    candidates = list(set(def_vtxes) & set(empty))
    if len(candidates) > 0:
        return [[c, "Defense"] for c in candidates]

    # other situations, search the empty cells in order
    # the order is optimal under most situations (but not all the situations)
    if is_player:
        if remain_steps > 6:
            order = [f"{turn_color}-2", f"{turn_color}-1", "empty", f"{opponent_color}-1", f"{opponent_color}-2"]
        elif remain_steps == 5 or remain_steps == 6:
            order = [f"{turn_color}-2", f"{turn_color}-1", f"{opponent_color}-1", f"{opponent_color}-2"]
        elif remain_steps == 3 or remain_steps == 4:
            order = [f"{turn_color}-2", f"{turn_color}-1"]
        elif remain_steps == 2:
            order = [f"{turn_color}-2"]
        else:
            order = []
    else:
        order = [f"{opponent_color}-2", f"{turn_color}-2", f"{turn_color}-1", f"{opponent_color}-1", "empty"]

    for cat in order:
        cat_id = StateIndex[cat]
        vids = np.where(state_vec == cat_id)[0]
        for vid in vids:
            for p in graph.vertexes[vid].get_empty(empty):
                if p not in candidates:
                    candidates.append(p)
    return [[p, 'full search'] for p in candidates]


def update_groups(piece, color, state_vec, group_book):
    all_groups = np.array(group_book["all_four_in_a_row"])
    group_involve_piece = np.where(all_groups == piece)
    all_gids = group_involve_piece[0]
    state_vec[all_gids] = StateTransMatrix[int(color != "black")][state_vec[all_gids]]


def step(turn_color, empty, state_vec, graph, group_book, path, depth, max_depth, is_player):
    num_node = 0
    if depth >= max_depth:
        return [], [], num_node

    opponent_color = "white" if turn_color == "black" else "black"
    turn_candidates = get_candidates(turn_color, empty, state_vec, graph, max_depth - depth - (not is_player), is_player)
    all_forced_win_paths = []
    forced_win_cand = []
    for piece, cat in turn_candidates:
        if depth == max_depth - 1 and not cat.startswith("Force Win"):
            continue
        cp_empty = []
        for p in empty:
            if p != piece:
                cp_empty.append(p)
        cp_state_vec = np.copy(state_vec)
        update_groups(piece, turn_color, cp_state_vec, group_book)
        cp_path = deepcopy(path)
        cp_path.append(f"{turn_color}-{piece}-{cat}")
        num_node += 1
        if is_player:
            if cat == "Force Win":
                forced_win_cand.append([piece, cat])
                all_forced_win_paths.append(cp_path)
                num_node += 1
            else:
                next_fw_cand, next_all_fw_paths, n = step(opponent_color, cp_empty, cp_state_vec, graph,
                                                          group_book, cp_path, depth + 1, max_depth,
                                                          is_player=False)
                num_node += n
                if len(next_fw_cand) > 0:
                    forced_win_cand.append([piece, cat])
                    all_forced_win_paths += next_all_fw_paths
        else:
            if cat == "Force Win":
                num_node += 1
                break
            else:
                next_fw_cand, next_all_fw_paths, n = step(opponent_color, cp_empty, cp_state_vec, graph,
                                                          group_book, cp_path, depth + 1, max_depth,
                                                          is_player=True)
                num_node += n
                if len(next_fw_cand) > 0:
                    forced_win_cand.append([piece, cat])
                    all_forced_win_paths += next_all_fw_paths
                else:
                    return [], [], num_node

    return forced_win_cand, all_forced_win_paths, num_node


def search(black_pieces, white_pieces, pattern_book, max_depth, display=False):
    start = time.time()
    player_color = "black" if len(black_pieces) == len(white_pieces) else "white"
    cat_vec, empty, graph = init_groups(black_pieces, white_pieces, pattern_book)
    forced_win_cand, all_forced_win_paths, num_node = step(player_color, empty, cat_vec, graph, pattern_book, [], 1, max_depth, is_player=True)
    end = time.time()
    if display:
        print(num_node)
        print(forced_win_cand)
        for path in all_forced_win_paths:
            print(path)
    return forced_win_cand, all_forced_win_paths, num_node, end - start


if __name__ == '__main__':
    pattern_book = load_pattern_book()
    black = [3, 13, 15, 17, 20, 26, 29, 30, 10, 8]
    white = [1, 2, 4, 7, 12, 28, 31, 34, 0, 35]
    player_color = "black" if len(black) == len(white) else "white"
    max_depth = 5 * 2
    start = time.time()
    search(black, white, pattern_book, max_depth, display=True)
    end = time.time()
    print(end - start)