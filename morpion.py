import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
import os


class Morpion:
    def __init__(self, window):
        self.window = window
        self.window.title("Jeu de Morpion")
        self.window['bg'] = 'black'

        self.board = np.zeros((3, 3), dtype=int)
        self.currentPlayer = 1  # 1 pour X et -1 pour O
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.moves = []

        frame = tk.Frame(self.window)
        frame.pack()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(frame, text='', font='normal 20 bold', height=2, width=5,
                                               command=lambda i=i, j=j: self.click(i, j), bg='black',
                                               activebackground='#9C2394')
                self.buttons[i][j].grid(row=i, column=j)

        self.label = tk.Label(self.window, text="Joueur X commence", font='normal 15', bg='black', fg='#EC66E3',
                              activebackground='#9C2394', activeforeground='#D4A5D1')
        self.label.pack()

        self.resetButton = tk.Button(self.window, text='Rejouer', command=self.resetBoard, bg='black', fg='#EC66E3',
                                     activebackground='#9C2394', activeforeground='#D4A5D1')
        self.resetButton.pack()

        self.statsButton = tk.Button(self.window, text='Afficher les statistiques', bg='black', fg='#EC66E3',
                                     activebackground='#9C2394', activeforeground='#D4A5D1')
        self.statsButton.pack()

    def click(self, i, j):
        if self.board[i, j] == 0:
            move = f"{chr(97 + i)}{j + 1}"
            self.moves.append(move)

            if self.currentPlayer == 1:
                self.buttons[i][j].config(text='X', state='disabled')
                self.board[i, j] = 1
            else:
                self.buttons[i][j].config(text='O', state='disabled')
                self.board[i, j] = -1

            if self.checkWinner():
                winner = 'X' if self.currentPlayer == 1 else 'O'
                self.moves.append(winner)
                self.saveGame()
                self.endGame(f"Le joueur {winner} a gagné !")
            elif np.all(self.board != 0):
                self.moves.append("Draw")
                self.saveGame()
                self.endGame("Match nul")
            else:
                self.currentPlayer *= -1
                self.label.config(text=f"Tour de {'X' if self.currentPlayer == 1 else 'O'}")
                if self.currentPlayer == -1:
                    self.window.after(500, self.aiTurn)

    def aiTurn(self):
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    self.board[i, j] = -1
                    if self.checkWinner():
                        self.buttons[i][j].config(text='O', state='disabled')
                        self.endGame("Le joueur O a gagné !")
                        return
                    self.board[i, j] = 1
                    if self.checkWinner():
                        self.board[i, j] = -1
                        self.buttons[i][j].config(text='O', state='disabled')
                        self.currentPlayer = 1
                        self.label.config(text="Tour de X")
                        return
                    self.board[i, j] = 0

        emptySpots = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    emptySpots.append((i, j))
        clic = np.random.choice(len(emptySpots))
        i, j = emptySpots[clic]
        self.click(i, j)

    def checkWinner(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.currentPlayer) or np.all(self.board[:, i] == self.currentPlayer):
                return True
        if self.board[0, 0] == self.currentPlayer and self.board[1, 1] == self.currentPlayer and self.board[
            2, 2] == self.currentPlayer:
            return True
        if self.board[0, 2] == self.currentPlayer and self.board[1, 1] == self.currentPlayer and self.board[
            2, 0] == self.currentPlayer:
            return True
        return False

    def saveGame(self):
        filename = 'morpion_games.csv'
        file_exists = os.path.isfile(filename)
        data = [self.moves]

        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', header=not file_exists, index=False)
        self.moves = []

    def endGame(self, result):
        messagebox.showinfo("Fin du jeu", result)
        self.resetBoard()

    def resetBoard(self):
        self.board = np.zeros((3, 3), dtype=int)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
        self.currentPlayer = 1
        self.label.config(text="Joueur X commence")
        self.moves = []


if __name__ == "__main__":
    window = tk.Tk()
    morpion = Morpion(window)
    window.mainloop()
