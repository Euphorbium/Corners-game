from copy import deepcopy

import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        # print(maxEval)
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move

def alphabeta(board, depth, alpha, beta, max_player, game):
    print(f'alphabeta called: {depth} {alpha} {beta}')
    if depth == 0 or board.winner() != None:
        print(f'{alpha} {beta}')
        return board.evaluate(), board

    if max_player:
        maxEval = float('-inf')
        for move in get_all_moves(board, WHITE, game):
            evaluation = alphabeta(move, depth-1, alpha, beta, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval >= beta:
                print(f'best move found {alpha}')
                break
            alpha = max(alpha, maxEval)
        return maxEval, move
    else:
        minEval = float('inf')
        for move in get_all_moves(board, RED, game):
            evaluation = alphabeta(move, depth-1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval <= alpha:
                break
            beta = min(beta, minEval)
        return minEval, move


def simulate_move(piece, move, board):
    board.move(piece, move[0], move[1])


    return board


def get_all_moves(board, color, game):
    moves = set()

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board)
            moves.add(new_board)
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

