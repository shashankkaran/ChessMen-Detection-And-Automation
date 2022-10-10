

import sys
import cv2
import numpy as np
import pyautogui as pg
import chess
import chess.engine
import time

BOARD_SIZE = 400
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 140
BOARD_LEFT_COORD = 5
CONFIDENCE = 0.8
DETECTION_NOICE_THRESHOLD = 8
PIECES_PATH = './piece_recognition/pieces/'

WHITE = 0
BLACK = 1


side_to_move = 0


try:
    if sys.argv[1] == 'black': side_to_move = BLACK
except:
    print('usage: "chessbot.py white" or "chessbot.py black"')
    sys.exit(0)


square_to_coords = [];
get_square = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
];
  
piece_names = {
    'black_king': 'k',
    'black_queen': 'q',
    'black_rook': 'r',
    'black_bishop': 'b',
    'black_knight': 'n',
    'black_pawn': 'p',
    'white_knight': 'N',
    'white_pawn': 'P',
    'white_king': 'K',
    'white_queen': 'Q',
    'white_rook': 'R',
    'white_bishop': 'B'
}

def locate_piece(screenshot, piece_location):
   
    for index in range(len(piece_location)):
        piece = piece_location[index]
        
        cv2.rectangle(
            screenshot,
            (piece.left, piece.top),
            (piece.left + piece.width, piece.top + piece.height),
            (0, 0, 255),
            2
        )
    
   
    cv2.imshow('Screenshot', screenshot)
    cv2.waitKey(0)

def recognize_position():
    piece_locations = {
        'black_king': [],
        'black_queen': [],
        'black_rook': [],
        'black_bishop': [],
        'black_knight': [],
        'black_pawn': [],
        'white_knight': [],
        'white_pawn': [],
        'white_king': [],
        'white_queen': [],
        'white_rook': [],
        'white_bishop': []
    }

    screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)

    for piece in piece_names.keys():
        for location in pg.locateAllOnScreen(PIECES_PATH + piece + '.png', confidence=CONFIDENCE):
            noise = False
            
            for position in piece_locations[piece]:
                if abs(position.left - location.left) < DETECTION_NOICE_THRESHOLD and \
                   abs(position.top - location.top) < DETECTION_NOICE_THRESHOLD:
                    noise = True
                    break
            
            if noise: continue
            
            piece_locations[piece].append(location)
            print('detecting:', piece, location)
            
    return screenshot, piece_locations
def locations_to_fen(piece_locations):
    fen = ''
    
    x = BOARD_LEFT_COORD
    y = BOARD_TOP_COORD
    
    for row in range(8):
        empty = 0
            
        for col in range(8):
            square = row * 8 + col
            
            is_piece = ()
            
            for piece_type in piece_locations.keys():
                for piece in piece_locations[piece_type]:
                    if abs(piece.left - x) < DETECTION_NOICE_THRESHOLD and \
                       abs(piece.top - y) < DETECTION_NOICE_THRESHOLD:
                        if empty:
                            fen += str(empty)
                            empty = 0

                        fen += piece_names[piece_type]
                        is_piece = (square, piece_names[piece_type])
            
            if not len(is_piece):
                empty += 1
            
            x += CELL_SIZE
        
        if empty: fen += str(empty)
        if row < 7: fen += '/'
        
        x = BOARD_LEFT_COORD
        y += CELL_SIZE
    
    fen += ' ' + 'b' if side_to_move else ' w'
    
    fen += ' KQkq - 0 1'
    
    return fen
            
def search(fen):
    print('Searching best move for this position:')
    print(fen)
    board = chess.Board(fen=fen)
    print(board)

    engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\shash\Downloads\opencv-chess-bot-main\opencv-chess-bot-main\src\Stockfish\stockfish")
    
    # print(engine)

    # get best move
    best_move = str(engine.play(board, chess.engine.Limit(time=0.1)).move)
    # print("==>")
    # close engine
    engine.quit()

    # search for the best move
    return best_move


x = BOARD_LEFT_COORD
y = BOARD_TOP_COORD
for row in range(8):
    for col in range(8):
        square = row * 8 + col
        
        square_to_coords.append((int(x + CELL_SIZE / 2), int(y + CELL_SIZE / 2)))
        x += CELL_SIZE
    x = BOARD_LEFT_COORD
    y += CELL_SIZE

while True:
    try:
        screenshot, piece_locations = recognize_position()
        fen = locations_to_fen(piece_locations)
        best_move = search(fen)
        print('Best move:', best_move)
        from_sq = square_to_coords[get_square.index(best_move[0] + best_move[1])]
        to_sq = square_to_coords[get_square.index(best_move[2] + best_move[3])]
        pg.moveTo(from_sq)
        pg.click()
        pg.moveTo(to_sq)
        pg.click()
        time.sleep(3)
    
    except: sys.exit(0)











