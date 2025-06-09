from flask import Flask, render_template, abort
import chess
import chess.engine

app = Flask(__name__)

STOCKFISH_PATH = "./learning pygame/NeuroChess/stockfish1/stockfish-windows-x86-64-avx2.exe"  # Adjust this path if needed
MOVES_PATH = "./learning pygame/NeuroChess/storage/moves.txt"  # Path to your moves.txt
GAME_HISTORY_PATH = "./learning pygame/NeuroChess/storage/game_history.txt"

BEST = "#00AA1A"
PERFECT = "#57D115"
EXCELLENT = "#92E600"
GOOD = "#D7FD2B"
INACCURACY = "#FF7A15"
MISTAKE = "#E11F1F"
SERIOUS_MISTAKE = "#C21919"
BLUNDER = "#B80000"

def analyze_game(moves_list=None):
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    feedback_list = []

    # Use provided moves list or read from file
    if moves_list is None:
        with open(MOVES_PATH, "r") as f:
            move_lines = [line.strip() for line in f if line.strip()]
    else:
        move_lines = moves_list

    for idx, move_str in enumerate(move_lines):
        player = "White" if board.turn == chess.WHITE else "Black"

        try:
            move = chess.Move.from_uci(move_str)
            if move not in board.legal_moves:
                raise ValueError("Illegal move")
        except ValueError:
            feedback_list.append({
                "move_no": idx // 2 + 1,
                "player": player,
                "move": move_str,
                "delta": "—",
                "feedback": "Invalid or illegal move!",
                "color": "#6c757d"
            })
            continue

        # Get best move from engine
        best_result = engine.analyse(board, chess.engine.Limit(depth=15))
        best_move = best_result["pv"][0]
        score_before = best_result["score"].white().score(mate_score=10000) or 0

        # Push actual move
        board.push(move)

        # Evaluate after actual move
        actual_result = engine.analyse(board, chess.engine.Limit(time=0.1))
        score_after = actual_result["score"].white().score(mate_score=10000) or 0

        # Adjust delta depending on side to move
        delta = score_after - score_before
        if player == "Black":
            delta = -delta

        # Feedback classification (based on delta and best move)
        if move == best_move:
            fb = "Best move!"
            color = BEST
        elif abs(delta) < 10:
            fb = "Perfect!"
            color = PERFECT
        elif abs(delta) < 25:
            fb = "Excellent!"
            color = EXCELLENT
        elif abs(delta) < 50:
            fb = "Good"
            color = GOOD
        elif abs(delta) < 75:
            fb = "Inaccuracy"
            color = INACCURACY
        elif abs(delta) < 150:
            if abs(delta) < 100:
                fb = "Mistake"
                color = MISTAKE
            else:
                fb = "Serious Mistake"
                color = SERIOUS_MISTAKE
        else:
            fb = "Blunder!"
            color = BLUNDER

        # Mate detection remains
        if "mate" in str(best_result["score"]).lower() or "mate" in str(actual_result["score"]).lower():
            color = "#800080"
            fb = "Checkmate sequence" if abs(delta) > 0 else "Mate defended"

        feedback_list.append({
            "move_no": idx // 2 + 1,
            "player": player,
            "move": move_str,
            "delta": f"{delta:+}",
            "feedback": fb,
            "color": color
        })

    engine.quit()
    return feedback_list

def parse_game_history():
    """Parse game_history.txt into individual games"""
    games = []
    current_game = []

    with open(GAME_HISTORY_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Game"):
                if current_game:
                    games.append(current_game)
                    current_game = []
            elif line:
                current_game.append(line)
        if current_game:
            games.append(current_game)
    return games

@app.route("/")
def home():
    feedback = analyze_game()
    return render_template("index.html", feedback=feedback)

@app.route("/current_game")
def current_game():
    feedback = analyze_game()
    return render_template("index.html", feedback=feedback)

@app.route("/game_history")
def game_history():
    games = parse_game_history()
    return render_template("game_history.html", games=games)

@app.route("/view_game/<int:game_id>")
def view_game(game_id):
    games = parse_game_history()
    if game_id < 1 or game_id > len(games):
        abort(404)
    feedback = analyze_game(moves_list=games[game_id-1])
    return render_template("index.html", feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
