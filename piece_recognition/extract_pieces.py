
#FEN "k1q1r1b1/1n1p4/8/8/8/1N1P4/K1Q1R1B1/8 w - - 0 1"

import cv2
import pyautogui as pg

BOARD_SIZE = 400
DARK_SQUARE_THRESHOLD = 150
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 138
BOARD_LEFT_COORD = 5

piece_names = {
    '0': 'black_king',
    '1': 'black_queen',
    '2': 'black_rook',
    '3': 'black_bishop',
    '4': 'black_knight',
    '5': 'black_pawn',
    '6': 'white_knight',
    '7': 'white_pawn',
    '8': 'white_king',
    '9': 'white_queen',
    '10': 'white_rook',
    '11': 'white_bishop'
}

y = BOARD_TOP_COORD
x = BOARD_LEFT_COORD

pg.screenshot('screenshot.png')

screenshot = cv2.imread('screenshot.png')

screenshot_grayscale = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

piece_code = 0

for row in range(8):
    
    for col in range(8):
        
        if row in [0, 1, 5, 6]:
            
            if screenshot_grayscale[y][x] > DARK_SQUARE_THRESHOLD:
               
                if row == 1 and col < 4: continue
                if row == 5 and col < 4: continue
                
                
                piece_image = screenshot[y:y + CELL_SIZE, x: x + CELL_SIZE]
                
               
                cv2.imshow('scr', piece_image)
                cv2.waitKey(0)
                
               
                cv2.imwrite('./pieces/' + piece_names[str(piece_code)] + '.png', piece_image)
                
               
                piece_code += 1
        
        x += CELL_SIZE
    
        x = BOARD_LEFT_COORD
    y += CELL_SIZE

cv2.destroyAllWindows()

