import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENTIONS = 8
SQ_SIZE = HEIGHT // DIMENTIONS
MAX_FPS = 15
IMAGES = {}

def loadimages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = p.image.load("my_chess/images/" + piece + ".png")
