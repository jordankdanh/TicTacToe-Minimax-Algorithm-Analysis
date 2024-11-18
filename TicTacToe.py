import tkinter as tk
from tkinter import messagebox
import math


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  # Human player
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.use_alpha_beta = False
        self.create_start_menu()
        self.window.mainloop()

    def create_start_menu(self):
        """Creates the start menu where the player selects the AI mode."""
        menu_frame = tk.Frame(self.window)
        menu_frame.pack(pady=20)

        label = tk.Label(menu_frame, text="Choose AI Mode", font=("Arial", 16))
        label.pack(pady=10)

        minimax_button = tk.Button(
            menu_frame, text="Minimax", font=("Arial", 14),
            command=lambda: self.start_game(False)
        )
        minimax_button.pack(pady=5)

        alpha_beta_button = tk.Button(
            menu_frame, text="Alpha-Beta Pruning", font=("Arial", 14),
            command=lambda: self.start_game(True)
        )
        alpha_beta_button.pack(pady=5)

    def start_game(self, use_alpha_beta):
        """Starts the game with the selected AI mode."""
        self.use_alpha_beta = use_alpha_beta
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_ui()

    def create_ui(self):
        """Creates the game UI."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.window, text="", font=("Arial", 24), width=5, height=2,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, row, col):
        if self.board[row][col] == "" and self.current_player == "X":
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X")
            if self.check_winner():
                messagebox.showinfo("Game Over", "You Win!")
                self.reset_game()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_game()
            else:
                self.current_player = "O"
                self.ai_move()

    def ai_move(self):
        best_score = -math.inf
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False, -math.inf, math.inf) if self.use_alpha_beta else self.minimax(False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            row, col = best_move
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")
            if self.check_winner():
                messagebox.showinfo("Game Over", "AI Wins!")
                self.reset_game()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_game()
            else:
                self.current_player = "X"

    def minimax(self, is_maximizing, alpha=None, beta=None):
        winner = self.check_winner()
        if winner == "X":
            return -1
        elif winner == "O":
            return 1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(False, alpha, beta) if alpha is not None else self.minimax(False)
                        self.board[i][j] = ""
                        best_score = max(best_score, score)
                        if alpha is not None:
                            alpha = max(alpha, best_score)
                            if beta is not None and beta <= alpha:
                                break
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(True, alpha, beta) if alpha is not None else self.minimax(True)
                        self.board[i][j] = ""
                        best_score = min(best_score, score)
                        if beta is not None:
                            beta = min(beta, best_score)
                            if beta <= alpha:
                                break
            return best_score

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        return None

    def is_draw(self):
        for row in self.board:
            if "" in row:
                return False
        return True

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.current_player = "X"


if __name__ == "__main__":
    TicTacToe()
