import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd


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
                self.buttons[i][j] = tk.Button(frame, text='', font='normal 20 bold', height=2, width=5, command=lambda i=i, j=j: self.click(i, j), bg='black', activebackground ='#9C2394')
                self.buttons[i][j].grid(row=i, column=j)
        
        self.label = tk.Label(self.window, text="Joueur X commence", font='normal 15', bg='black', fg='#EC66E3', activebackground ='#9C2394', activeforeground ='#D4A5D1')
        self.label.pack()
        
        self.resetButton = tk.Button(self.window, text='Rejouer', command=self.resetBoard, bg='black', fg='#EC66E3', activebackground ='#9C2394', activeforeground ='#D4A5D1')
        self.resetButton.pack()
        
        self.statsButton = tk.Button(self.window, text='Afficher les statistiques', command=self.showStats, bg='black', fg='#EC66E3', activebackground ='#9C2394', activeforeground ='#D4A5D1')
        self.statsButton.pack()

    def click(self, i, j):
        if self.board[i, j] == 0:
            if self.currentPlayer == 1:
                self.buttons[i][j].config(text='X', state='disabled')
                self.board[i, j] = 1
                self.moves.append(('X', i, j))
            else:
                self.buttons[i][j].config(text='O', state='disabled')
                self.board[i, j] = -1
                self.moves.append(('O', i, j))
            
            if self.checkWinner(self.currentPlayer):
                winner = 'X' if self.currentPlayer == 1 else 'O'
                self.endGame(f"Le joueur " + winner + " a gagné !", winner)
            elif np.all(self.board != 0):
                self.endGame("Match nul", 'N')
            else:
                self.currentPlayer *= -1
                self.label.config(text=f"Tour de {'X' if self.currentPlayer == 1 else 'O'}")
                if self.currentPlayer == -1 :
                    self.window.after(500, self.aiTurn)

    def aiTurn(self) :
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    self.board[i, j] = -1
                    if self.checkWinner(-1):
                        self.buttons[i][j].config(text='O', state='disabled')
                        self.moves.append(('O', i, j))
                        self.endGame("Le joueur O a gagné !", 'O')
                        return
                    self.board[i, j] = 0

        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    self.board[i, j] = 1
                    if self.checkWinner(1):
                        self.board[i, j] = -1
                        self.buttons[i][j].config(text='O', state='disabled')
                        self.moves.append(('O', i, j))
                        self.currentPlayer = 1
                        self.label.config(text="Tour de X")
                        return
                    self.board[i, j] = 0

        emptySpots = []
        for i in range(3) :
            for j in range(3) :
                if self.board[i, j] == 0 :
                    emptySpots.append((i, j))
        clic = np.random.choice(len(emptySpots))
        i, j = emptySpots[clic]
        self.click(i, j)

    def checkWinner(self, player):
        for i in range(3):
            if np.all(self.board[i, :] == player) or np.all(self.board[:, i] == player):
                return True
        if self.board[0, 0] == player and self.board[1, 1] == player and self.board[2, 2] == player:
            return True
        if self.board[0, 2] == player and self.board[1, 1] == player and self.board[2, 0] == player:
            return True
        return False

    def endGame(self, result, winner):
        messagebox.showinfo("Fin du jeu", result)
        self.saveStats(winner)
        self.resetBoard()

    def saveStats(self, winner):
        dfMoves = pd.DataFrame(self.moves, columns=['Player', 'Row', 'Column'])
        dfWinner = pd.DataFrame([{'Player': '', 'Row': '', 'Column': 'Winner', 'Winner': winner}])
        dfSeparator = pd.DataFrame([{'Player': '_____', 'Row': '_____', 'Column': '_____', 'Winner': '_____'}])
        
        moves = dfMoves.to_string(index=False, header=False)
        winner = dfWinner.to_string(index=False, header=False)
        separator = dfSeparator.to_string(index=False, header=False)
        
        with open('morpion_moves.csv', 'a') as f:
            f.write(moves + '\n')
            f.write(winner + '\n')
            f.write(separator + '\n')

    def loadStats(self):
        try:
            statsData = pd.read_csv('morpion_moves.csv')
        except FileNotFoundError:
            statsData = "Aucun fichier de statistiques trouvé"
        return statsData

    def showStats(self):
        statsData = self.loadStats()
        
        statsWindow = tk.Toplevel(self.window)
        statsWindow.title("Statistiques")
        statsWindow.configure(bg='black')

        statsText = tk.Text(statsWindow, font='normal 12', bg='black', fg='#EC66E3', wrap='word')
        statsText.insert(tk.END, statsData.to_string(index=False))
        statsText.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(statsWindow, command=statsText.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        statsText.config(yscrollcommand=scrollbar.set)

        close = tk.Button(statsWindow, text="Fermer", command=statsWindow.destroy, bg='black', fg='#EC66E3', activebackground ='#9C2394', activeforeground ='#D4A5D1')
        close.pack(pady=10)

        statsWindow.mainloop()

    def resetBoard(self):
        self.board = np.zeros((3, 3), dtype=int)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
        self.moves = []
        self.currentPlayer = 1
        self.label.config(text="Joueur X commence")


if __name__ == "__main__":
    window = tk.Tk()
    morpion = Morpion(window)
    window.mainloop()
