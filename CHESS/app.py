import streamlit as st
import chess
import chess.svg
import pygame as p
import base64
from io import BytesIO
from ChessEngine import Gamestate
from ChessAI import findBestMove
import time

if "game_state" not in st.session_state:
    st.session_state.game_state = Gamestate()
    st.session_state.board = chess.Board()
    st.session_state.move_log = []

def render_board(board):
    """Renders the current chessboard as an SVG image and encodes it for Streamlit."""
    svg = chess.svg.board(board)
    return f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"/>'

st.title("♟️ Chess Game with AI ♟️")
st.markdown("Play against an AI chess engine built using Pygame and Streamlit.")

st.markdown(render_board(st.session_state.board), unsafe_allow_html=True)

user_move = st.text_input("Enter your move (e.g., e2e4):")

if st.button("Make Move"):
    try:
        move = chess.Move.from_uci(user_move)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_log.append(f"User: {user_move}")

            if not st.session_state.board.is_game_over():
                time.sleep(1)  # Simulating AI thinking time
                ai_move = findBestMove(st.session_state.game_state, st.session_state.game_state.getValidMoves(), None)
                if ai_move:
                    st.session_state.board.push(chess.Move.from_uci(ai_move))
                    st.session_state.move_log.append(f"AI: {ai_move}")

        else:
            st.error("Invalid move! Try again.")

    except Exception as e:
        st.error(f"Error: {str(e)}")

st.subheader("Move Log")
for move in st.session_state.move_log:
    st.write(move)

if st.session_state.board.is_checkmate():
    st.success("Checkmate! Game over.")
elif st.session_state.board.is_stalemate():
    st.warning("Stalemate! It's a draw.")
elif st.session_state.board.is_insufficient_material():
    st.warning("Draw due to insufficient material.")
