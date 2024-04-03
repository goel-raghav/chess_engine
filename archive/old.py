def minmax(board: Board, depth, color, alpha, beta):
    if depth == 0:
        return evaluate(board, color)
    
    if color:
        val = -math.inf
        m = None
        moves = board.legal_moves
        # moves = sorted(moves, key=lambda move: move_key(move, board))
        for move in moves:
            board.push(move)
            e, _ = minmax(board, depth-1, not color, alpha, beta)
            if e > val:
                m = move
                val = e
            board.pop()
            if val > beta:
                shift_killer_move(move)
                break
            alpha = max(val, alpha)
        return val, m
    
    else:
        val = math.inf
        moves = board.legal_moves
        # moves = sorted(moves, key=lambda move: move_key(move, board))
        for move in moves:
            board.push(move)
            e, _ = minmax(board, depth-1, not color, alpha, beta)
            if e < val:
                m = move
                val = e
            board.pop()
            if val < alpha:
                shift_killer_move(move)
                break
            beta = min(val, beta)
        return val, m