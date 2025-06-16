import tkinter as tk
from tkinter import messagebox
import random


class GameModeSelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Выбор режима игры")
        self.root.geometry("300x150")

        self.label = tk.Label(root, text="Выберите режим игры:", font=('Helvetica', 15))
        self.label.pack(pady=10)

        self.friend_btn = tk.Button(root, text="Играть с другом", command=self.start_friend_mode, width=20)
        self.friend_btn.pack(pady=5)

        self.bot_btn = tk.Button(root, text="Играть с ботом", command=self.start_bot_mode, width=20)
        self.bot_btn.pack(pady=5)

    def start_friend_mode(self):
        self.root.destroy()
        game_root = tk.Tk()
        TicTacToe(game_root, "friend", "X")
        game_root.mainloop()

    def start_bot_mode(self):
        self.root.destroy()
        first_move_root = tk.Tk()
        FirstMoveSelection(first_move_root)


class FirstMoveSelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Выбор первого хода")
        self.root.geometry("300x150")

        self.label = tk.Label(root, text="Кто ходит первым?", font=('Helvetica', 15))
        self.label.pack(pady=10)

        self.player_btn = tk.Button(root, text="Я (Х)", command=lambda: self.start_game("X"), width=20)
        self.player_btn.pack(pady=5)

        self.bot_btn = tk.Button(root, text="Бот (O)", command=lambda: self.start_game("O"), width=20)
        self.bot_btn.pack(pady=5)

    def start_game(self, first_player):
        self.root.destroy()
        game_root = tk.Tk()
        TicTacToe(game_root, "bot", first_player)
        game_root.mainloop()


class TicTacToe:
    def __init__(self, root, game_mode, first_player):
        self.root = root
        self.root.title("Крестики-нолики")
        self.game_mode = game_mode
        self.current_player = first_player
        self.board = [" " for i in range(9)]

        self.top_frame = tk.Frame(root)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="we")

        self.mode_label = tk.Label(self.top_frame,
                                   text=f"Режим: {'2 игрока' if game_mode == 'friend' else 'Игра с ботом'}",
                                   font=('Arial', 10))
        self.mode_label.pack(side="left", padx=5)

        self.change_mode_btn = tk.Button(self.top_frame, text="Сменить режим", command=self.change_mode,
                                         font=('Arial', 10))
        self.change_mode_btn.pack(side="right", padx=5)

        self.player_label = tk.Label(root, text=f"Первым ходит: {'Вы (X)' if first_player == 'X' else 'Бот (O)'}",
                                     font=('Arial', 10))
        self.player_label.grid(row=1, column=0, columnspan=3, sticky="w")

        self.buttons = []
        for i in range(9):
            button = tk.Button(root, text=" ", font=('Arial', 20), width=5, height=2,
                               command=lambda idx=i: self.make_move(idx))
            button.grid(row=i // 3 + 2, column=i % 3)
            self.buttons.append(button)

        self.reset_button = tk.Button(root, text="Новая игра", command=self.reset_game)
        self.reset_button.grid(row=5, column=0, columnspan=3, sticky="we")

        if self.game_mode == "bot" and self.current_player == "O":
            self.root.after(500, self.bot_move)

    def change_mode(self):
        self.root.destroy()
        selection_root = tk.Tk()
        GameModeSelection(selection_root)
        selection_root.mainloop()

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            self.buttons[position].config(text=self.current_player)

            if self.check_winner():
                winner = self.get_winner_name()
                messagebox.showinfo("Победа!", winner)
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
                self.reset_game()
            else:
                self.switch_player()
                if self.game_mode == "bot" and self.current_player == "O":
                    self.root.after(500, self.bot_move)

    def get_winner_name(self):
        if self.game_mode == "friend":
            return f"Игрок {self.current_player} победил!"
        else:
            return "Вы победили!" if self.current_player == "X" else "Бот победил!"

    def bot_move(self):
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                if self.check_winner():
                    self.buttons[i].config(text="O")
                    messagebox.showinfo("Победа!", "Бот победил!")
                    self.reset_game()
                    return
                self.board[i] = " "

        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = "O"
                    self.buttons[i].config(text="O")
                    self.switch_player()
                    return
                self.board[i] = " "

        if self.board[4] == " ":
            self.make_move(4)
            return

        empty_positions = [i for i, val in enumerate(self.board) if val == " "]
        if empty_positions:
            move = random.choice(empty_positions)
            self.make_move(move)

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " "):
                return True
        return False

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.current_player = "X" if self.game_mode == "friend" else "X"
        if self.game_mode == "bot" and self.current_player == "O":
            self.root.after(500, self.bot_move)


if __name__ == "__main__":
    selection_root = tk.Tk()
    GameModeSelection(selection_root)
    selection_root.mainloop()
