import time
import math
import json


class TicTacToeAIvsAI:
    def __init__(self, algorithm1="minimax", algorithm2="minimax", games=10):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.algorithm1 = algorithm1
        self.algorithm2 = algorithm2
        self.games_to_play = games
        self.total_nodes = 0
        self.total_time = 0
        self.games_played = 0
        self.total_pruned_branches = 0
        self.total_game_tree_size = 0
        self.results = {"X": 0, "O": 0, "Draw": 0}

    def reset_board(self):
        """Reset the board to start a new game."""
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def play_game(self):
        """Simulates one game of AI vs AI."""
        self.reset_board()
        current_player = "X"
        game_tree_size = 0
        branches_pruned = 0

        while True:
            nodes_visited, pruned = self.ai_move(current_player)
            self.total_nodes += nodes_visited
            game_tree_size += nodes_visited
            branches_pruned += pruned

            if self.check_winner():
                self.results[current_player] += 1
                break
            if self.is_draw():
                self.results["Draw"] += 1
                break

            current_player = "O" if current_player == "X" else "X"

        self.total_game_tree_size += game_tree_size
        self.total_pruned_branches += branches_pruned

    def ai_move(self, player):
        """AI makes a move based on the selected algorithm for each player."""
        if player == "X":
            algorithm = self.algorithm1
        else:
            algorithm = self.algorithm2

        best_score = -math.inf if player == "X" else math.inf
        best_move = None
        nodes_visited = 0
        pruned = 0

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = player
                    if algorithm == "alphabeta":
                        score, visited, pruned_branches = self.minimax_alpha_beta(player == "O", -math.inf, math.inf)
                    else:
                        score, visited, _ = self.minimax(player == "O")
                        pruned_branches = 0
                    self.board[i][j] = ""
                    nodes_visited += visited
                    pruned += pruned_branches

                    if (player == "X" and score > best_score) or (player == "O" and score < best_score):
                        best_score = score
                        best_move = (i, j)

        if best_move:
            row, col = best_move
            self.board[row][col] = player
        return nodes_visited, pruned

    def minimax(self, is_maximizing):
        """Regular Minimax algorithm."""
        winner = self.check_winner()
        if winner == "X":
            return 1, 1, 0
        elif winner == "O":
            return -1, 1, 0
        elif self.is_draw():
            return 0, 1, 0

        nodes_visited = 0
        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score, visited, _ = self.minimax(False)
                        self.board[i][j] = ""
                        best_score = max(best_score, score)
                        nodes_visited += visited
            return best_score, nodes_visited + 1, 0
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score, visited, _ = self.minimax(True)
                        self.board[i][j] = ""
                        best_score = min(best_score, score)
                        nodes_visited += visited
            return best_score, nodes_visited + 1, 0

    def minimax_alpha_beta(self, is_maximizing, alpha, beta):
        """Minimax algorithm with Alpha-Beta Pruning."""
        winner = self.check_winner()
        if winner == "X":
            return 1, 1, 0
        elif winner == "O":
            return -1, 1, 0
        elif self.is_draw():
            return 0, 1, 0

        nodes_visited = 0
        pruned = 0
        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score, visited, pruned_branches = self.minimax_alpha_beta(False, alpha, beta)
                        self.board[i][j] = ""
                        best_score = max(best_score, score)
                        alpha = max(alpha, best_score)
                        nodes_visited += visited
                        pruned += pruned_branches
                        if beta <= alpha:
                            pruned += 1
                            break
            return best_score, nodes_visited + 1, pruned
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score, visited, pruned_branches = self.minimax_alpha_beta(True, alpha, beta)
                        self.board[i][j] = ""
                        best_score = min(best_score, score)
                        beta = min(beta, best_score)
                        nodes_visited += visited
                        pruned += pruned_branches
                        if beta <= alpha:
                            pruned += 1
                            break
            return best_score, nodes_visited + 1, pruned

    def check_winner(self):
        """Check for a winner in the game."""
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
        """Check if the game is a draw."""
        for row in self.board:
            if "" in row:
                return False
        return True

    def run_simulation(self):
        """Simulates multiple games and calculates statistics."""
        start_time = time.time()
        for _ in range(self.games_to_play):
            self.play_game()
        end_time = time.time()

        average_nodes = self.total_nodes / (self.games_to_play * 9)
        average_game_tree_size = self.total_game_tree_size / self.games_to_play
        average_pruned = self.total_pruned_branches / self.games_to_play
        overall_game_time = end_time - start_time
        algorithm1 = "Alpha-Beta Pruning" if self.algorithm1 == "alphabeta" else "Minimax"
        algorithm2 = "Alpha-Beta Pruning" if self.algorithm2 == "alphabeta" else "Minimax"
        data = {
            "Algorithm 1": algorithm1,
            "Algorithm 2": algorithm2,
            "Average Nodes Visited per Move": average_nodes,
            "Average Time Taken per Move (ms)": (overall_game_time / (self.games_to_play * 9)) * 1000,
            "Overall Game Time (seconds)": overall_game_time,
            "Average Game Tree Size": average_game_tree_size,
            "Average Branches Pruned": average_pruned,
            "Game Outcomes": self.results,
        }

        with open(f"{algorithm1} vs {algorithm2} Simulation Data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Results saved to {algorithm1} vs {algorithm2} Simulation Data.json")


if __name__ == "__main__":
    print("Simulating Minimax vs Minimax...")
    game_minimax_vs_minimax = TicTacToeAIvsAI(algorithm1="minimax", algorithm2="minimax", games=10)
    game_minimax_vs_minimax.run_simulation()

    print("Simulating Alpha-Beta Pruning vs Alpha-Beta Pruning...")
    game_alpha_beta_vs_alpha_beta = TicTacToeAIvsAI(algorithm1="alphabeta", algorithm2="alphabeta", games=10)
    game_alpha_beta_vs_alpha_beta.run_simulation()

    print("Simulating Minimax vs Alpha-Beta Pruning...")
    game_minimax_vs_alpha_beta = TicTacToeAIvsAI(algorithm1="minimax", algorithm2="alphabeta", games=10)
    game_minimax_vs_alpha_beta.run_simulation()
