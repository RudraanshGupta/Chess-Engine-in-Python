import streamlit as st
from ChessEngine import Gamestate
from ChessAI import findBestMove, findRandomMove
import chess
import time

# Unicode pieces mapping
UNICODE_PIECES = {
    'wp': '♙', 'wR': '♖', 'wN': '♘', 'wB': '♗', 'wQ': '♕', 'wK': '♔',
    'bp': '♟', 'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚',
    '--': ' '
}

# Initialize game state
if 'gs' not in st.session_state:
    st.session_state.gs = Gamestate()
    st.session_state.selected = None  # (row, col)
    st.session_state.move_made = False

st.title("♟️ Chess Engine on Streamlit")

# Render board as an 8x8 grid of buttons
for r in range(8):
    cols = st.columns(8)
    for c, col in enumerate(cols):
        piece = st.session_state.gs.board[r][c]
        label = UNICODE_PIECES[piece]
        # highlight selected
        if st.session_state.selected == (r, c):
            styles = "background-color:lightblue"
        else:
            styles = None
        if col.button(label, key=f"{r}_{c}", help=f"{r},{c}"):
            # handle click
            if st.session_state.selected is None:
                if piece != '--' and ((piece[0]=='w' and st.session_state.gs.whitetomove) or (piece[0]=='b' and not st.session_state.gs.whitetomove)):
                    st.session_state.selected = (r, c)
            else:
                start = st.session_state.selected
                end = (r, c)
                move = None
                # find matching move
                for m in st.session_state.gs.getValidMoves():
                    if m.startRow==start[0] and m.startCol==start[1] and m.endRow==end[0] and m.endCol==end[1]:
                        move = m
                        break
                if move:
                    st.session_state.gs.makeMoves(move)
                    st.session_state.move_made = True
                st.session_state.selected = None
            st.experimental_rerun()

# After human move, let AI play
if st.session_state.move_made:
    with st.spinner("AI thinking..."):
        time.sleep(0.5)
        valid = st.session_state.gs.getValidMoves()
        ai_move = findBestMove(st.session_state.gs, valid, None)
        if ai_move is None:
            ai_move = findRandomMove(valid)
        st.session_state.gs.makeMoves(ai_move)
        st.session_state.move_made = False
    st.experimental_rerun()

# Check endgame
if st.session_state.gs.checkMate or st.session_state.gs.staleMate:
    if st.session_state.gs.staleMate:
        st.warning("Stalemate! It's a draw.")
    else:
        winner = 'Black' if st.session_state.gs.whitetomove else 'White'
        st.success(f"Checkmate! {winner} wins.")
    if st.button("Restart"):
        st.session_state.gs = Gamestate()
        st.session_state.selected = None
        st.session_state.move_made = False
        st.experimental_rerun()