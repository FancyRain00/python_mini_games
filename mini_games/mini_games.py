"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Kehittynyt käyttöliittymä / Advanced GUI
Name:       Anas Monjib
Email:      amonjib@gmail.com
Student Id: ----

This is an app called Mini Games that contains a couple of games.
It is possible to add games later on. Right now it has two games:
Tic-Tac-Toe and Rock-Paper-Scissors.
When you start the game, you are welcomed with the menu window. you can
either choose 'Choose Game' or 'Quit' to stop the program.
If you choose the first option, you are greeted with the game options window,
where you can choose the game you want to play.
The games are straightforward and pretty self explanatory. Although to know
how the game works there is a 'Help' button explaining everything.
Whatever window you are on, if you press menu or 'X:button' to exit, you are
directed to the menu window where you can either choose a new game or exit.

disclaimer for TA: The code was mostly made by myself. The way to change
windows and how to change what 'X:button' does is what I looked up.
In my opinion this should be more than enough for the Advanced GUI.
I could've used Menu() or other factors of the Advanced GUI, but for a game,
Buttons seemed more suited for the job.
"""
from tkinter import *
import tkinter.messagebox
from random import randint


class MainPage:
    """
    The main window that has a logo, a choose game button and a quit button.
    """
    def __init__(self):
        self.__interface = Tk()
        self.__interface.title("Mini Games")
        self.__photo = PhotoImage(file='logo.gif')
        self.__logo = Label(self.__interface, image=self.__photo)
        self.__logo.pack()

        self.__gamebutton = Button(self.__interface, text="Choose Game",
                                   height=2, width=15,
                                   background="DeepSkyBlue2",
                                   foreground="Black",
                                   command=self.change_window)
        self.__gamebutton.pack()

        self.__quit = Button(self.__interface, text="Quit",
                             height=1, width=10, background="Red",
                             foreground="White", command=self.quit)
        self.__quit.pack()

        self.__interface.mainloop()

    def quit(self):
        self.__interface.destroy()

    # Method that changes the window from the main window to the menu window
    # where you can choose the game you want to play
    def change_window(self):
        self.__interface.destroy()
        # Even though the 'game_menu' isn't used, the name is still given as
        # shown in examples
        game_menu = GameMenu()


class GameMenu:
    """
    The menu window that has four buttons with two photos and two texts.
    One photo and one txt button lead to the same game.
    """
    def __init__(self):
        self.__interface = Tk()
        self.__interface.title("Mini Games")
        self.__tic_photo = PhotoImage(file='tic_tac_photo.gif')
        self.__rps_photo = PhotoImage(file='r_p_s.png')

        self.__tic_tac = Button(self.__interface, image=self.__tic_photo,
                                height=300, width=300,
                                background="gainsboro",
                                command=self.choose_tic)
        self.__tic_tac.grid(row=0, column=0)

        self.__tic_txt = Button(self.__interface, text="Tic-Tac-Toe",
                                background="White", height=2, width=15,
                                command=self.choose_tic)
        self.__tic_txt.grid(row=1, column=0, sticky=W + E + S + N)

        self.__rps = Button(self.__interface, image=self.__rps_photo,
                            height=300, width=300,
                            background="gainsboro",
                            command=self.choose_rps)
        self.__rps.grid(row=0, column=1)

        self.__rpc_txt = Button(self.__interface, text="Rock-Paper_scissors",
                                background="White", height=2, width=15,
                                command=self.choose_rps)
        self.__rpc_txt.grid(row=1, column=1, sticky=W + E + S + N)

        # Here we change what happens when the x button is pressed
        self.__interface.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__interface.mainloop()

    # When the game 'Tic Tac Toe' is chosen, this method is called to close
    # the window and open the chosen game window
    def choose_tic(self):
        self.__interface.destroy()
        tic_tac_game = TicTacToe()

    # Same here, only here the chosen game is 'Rock Paper Scissors'
    def choose_rps(self):
        self.__interface.destroy()
        rpc_game = RPS()

    # Here we change what happens when the x button is pressed
    def on_closing(self):
        self.__interface.destroy()
        game_menu = MainPage()


class TicTacToe:
    """
    The game is Tic Tac Toe. Score label is shown and 9 buttons for the game.
    You play against another player and not with the computer.
    Three buttons for resetting the game board, Help info about the game
    and Menu for going back to the main page.
    """
    def __init__(self):
        self.__interface = Tk()
        self.__turn = 0
        self.__size = 3
        self.__interface.title(f"Tic-Tac-Toe {self.__size}x{self.__size}")

        self.__x_wins = 0
        self.__x_place = []
        self.__o_wins = 0
        self.__o_place = []

        self.__x_result = Label(self.__interface,
                                text=f"X: {self.__x_wins} wins",
                                background="White",
                                font='Times 18 bold')
        self.__x_result.grid(row=0, column=0, columnspan=self.__size,
                             sticky=W + E + S + N)

        self.__o_result = Label(self.__interface,
                                text=f"O: {self.__o_wins} wins",
                                background="White",
                                font='Times 18 bold')
        self.__o_result.grid(row=1, column=0, columnspan=self.__size,
                             sticky=W + E + S + N)

        # The following loop will initialize the two lists __buttons
        # and __commands to be SIZE×SIZE matrices (lists within a list)
        # with all elements initialized as None.  These two lists
        # will contain bookkeeping information about locations of
        # the game's push buttons and command functions connected
        # to a button in a particular location on the board.
        self.__buttons = []
        self.__commands = []
        for num in range(self.__size):
            self.__buttons.append([None] * self.__size)
            self.__commands.append([None] * self.__size)

        # Lets generate size * size command-functions and
        # size * size  push buttons, store the information
        # about them in the lists __buttons and __commands.
        # The buttons will also be placed on the game board.
        for y in range(self.__size):
            for x in range(self.__size):
                # The command function to handle a button press on
                # game piece in coordinates (y, x).
                def button_press(button_y_coord=y, button_x_coord=x):
                    self.game_play(button_y_coord, button_x_coord)

                # The defined function needs to be stored for later use
                # in the move_slate method.
                self.__commands[y][x] = button_press

                # The new button in placed on coordinated (y, x) and
                # its command function is the one defined earlier
                # which gets as its parameter the location (y, x) of the
                # button when clicked.
                new_button = Button(self.__interface,
                                    text="",
                                    width=16,
                                    heigh=8,
                                    background="gainsboro",
                                    command=button_press)

                # The newly created button is also stored into
                # the bookkeeping matrix.
                self.__buttons[y][x] = new_button

                # The button's location in the beginning of the game
                # is at coordinates (y + 2, x).
                new_button.grid(row=y + 2, column=x, sticky=W + E + S + N)

        self.__reset_game = Button(self.__interface, text="New Game",
                                   font='Times 18 bold',
                                   command=self.new_game)
        self.__reset_game.grid(row=self.__size + 3, column=0,
                               columnspan=self.__size // 2, )

        self.__help = Button(self.__interface, text="Help",
                             font='Times 18 bold',
                             command=self.help)
        self.__help.grid(row=self.__size + 3, column=1,
                         columnspan=self.__size // 2,
                         sticky=W + E + S + N)

        self.__quit = Button(self.__interface, text="Menu",
                             font='Times 18 bold',
                             command=self.quit)
        self.__quit.grid(row=self.__size + 3, column=2,
                         columnspan=self.__size // 2, sticky=W + E + S + N)

        self.__interface.protocol("WM_DELETE_WINDOW", self.quit)
        self.__interface.mainloop()

    # Method Takes the pressed button, makes sure it wasn't pressed before
    # and if it wasn't, then we put the players character on it.
    # Afterwards we call method to check if there is a winner.
    def game_play(self, y, x):
        pressed_btn = self.__buttons[y][x]
        num = (x + 1) + (y * 3)
        if num in self.__x_place or num in self.__o_place or 10 > num < 1:
            return

        if self.__turn % 2 == 0:
            pressed_btn.configure(text="X", background="SteelBlue1",
                                  font='Times 24 bold', width=6,
                                  heigh=3, )
            self.__x_place.append(num)
        elif self.__turn % 2 == 1:
            pressed_btn.configure(text="O", background="SlateBlue2",
                                  font='Times 24 bold', width=6,
                                  heigh=3, )
            self.__o_place.append(num)

        self.__turn += 1

        self.check_win()

    # Method checks if there is a winner using the winning combos
    # and if there is a winner, a message is shown and a method is called
    # for a new game.
    def check_win(self):
        winning_rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8],
                        [3, 6, 9], [1, 5, 9], [3, 5, 7]]

        for win_row in winning_rows:
            if set(win_row).issubset(self.__x_place):
                self.__x_wins += 1
                self.__x_result.configure(text=f"X: {self.__x_wins} wins")
                tkinter.messagebox.showinfo("Tic-Tac-Toe", "Player X wins!")
                self.new_game()
            elif set(win_row).issubset(self.__o_place):
                self.__o_wins += 1
                self.__o_result.configure(text=f"O: {self.__o_wins} wins")
                tkinter.messagebox.showinfo("Tic-Tac-Toe", "Player O Wins!")
                self.new_game()

        # If there if no winner and the game board is full, it is a tie
        # and a message is shown and a new game begun.
        if len(self.__x_place) + len(self.__o_place) == 9:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "It is a Tie")
            self.new_game()

    # Method is called if help button if pressed. A message containing
    # the info is shown
    def help(self):
        help_txt = ("1. The game is played on a grid that's 3 squares by 3 "
                    "squares.\n\n"
                    "2. You are X, your friend "
                    "is O. Players take turns putting their marks in empty "
                    "squares.\n\n"
                    "3. The first player to get 3 of their marks in a row (up,"
                    " down, across, or diagonally) is the winner.\n\n"
                    "4. When all 9 squares are full, the game is over. If no "
                    "player has 3 marks in a row, the game ends in a tie. ")

        tkinter.messagebox.showinfo("RULES FOR TIC-TAC-TOE", help_txt)

    # If Quit is chosen the window is closed and the main window is opened
    def quit(self):
        self.__interface.destroy()
        main_menu = MainPage()

    # Method deletes all the nfo that needs to be deleted for the new game
    # to start.
    def new_game(self):
        self.__x_place = []
        self.__o_place = []
        self.__turn = 0
        # Takes all the buttons and cleans them for the new game.
        for y in range(self.__size):
            for x in range(self.__size):
                button = self.__buttons[y][x]
                button.configure(text="", background="gainsboro")


class RPS:
    """
    The game Roc Paper Scissors. Score label is shown and 3 buttons for
    the game. You play against the computer and not with another player.
    Three buttons for resetting the whole game, Help info about the game
    and Menu for going back to the main page.
    """
    def __init__(self):
        self.__interface = Tk()
        self.__interface.title("Rock-Paper-Scissors")

        self.__p_points = 0
        self.__player_points = Label(self.__interface,
                                     text=f"Player: {self.__p_points} wins",
                                     background="White",
                                     font='Times 18 bold')
        self.__player_points.grid(row=0, column=0, columnspan=3,
                                  sticky=W + E + S + N)

        self.__c_points = 0
        self.__computer_points = Label(self.__interface,
                                       text=f"Computer: {self.__p_points} wins",
                                       background="White",
                                       font='Times 18 bold')
        self.__computer_points.grid(row=1, column=0, columnspan=3,
                                    sticky=W + E + S + N)

        self.__rock_p = PhotoImage(file='rock_left.png')
        self.__paper_p = PhotoImage(file='hand_left.png')
        self.__scissors_p = PhotoImage(file='scissors_left.png')

        self.__rock = Button(self.__interface, image=self.__rock_p,
                             background="SteelBlue1",
                             height=300, width=300,
                             command=self.choose_rock)
        self.__rock.grid(row=2, column=0)
        self.__paper = Button(self.__interface, image=self.__paper_p,
                              height=300, width=300,
                              background="SteelBlue1",
                              command=self.choose_paper)
        self.__paper.grid(row=2, column=1)
        self.__scissors = Button(self.__interface, image=self.__scissors_p,
                                 height=300, width=300,
                                 background="SteelBlue1",
                                 command=self.choose_scissors)
        self.__scissors.grid(row=2, column=2)

        self.__reset_game = Button(self.__interface, text="Reset",
                                   font='Times 18 bold',
                                   command=self.reset)
        self.__reset_game.grid(row=3, column=0,
                               columnspan=1, sticky=W + E + S + N)

        self.__help = Button(self.__interface, text="Help",
                             font='Times 18 bold',
                             command=self.help)
        self.__help.grid(row=3, column=1,
                         columnspan=1,
                         sticky=W + E + S + N)

        self.__quit = Button(self.__interface, text="Menu",
                             font='Times 18 bold',
                             command=self.on_closing)
        self.__quit.grid(row=3, column=2,
                         columnspan=1, sticky=W + E + S + N)

        self.__interface.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__interface.mainloop()

    # Background of the pressed button 'Rock' is changed to red
    def choose_rock(self):
        self.__rock.configure(background="Red")
        self.winning_hand("Rock")

    # Background of the pressed button 'Paper' is changed to red
    def choose_paper(self):
        self.__paper.configure(background="Red")
        self.winning_hand("Paper")

    # Background of the pressed button 'Scissors' is changed to red
    def choose_scissors(self):
        self.__scissors.configure(background="Red")
        self.winning_hand("Scissors")

    # Method chooses a hand for the computer, then compares the two hands
    # to see which one won. After that shows a message and starts a new game.
    def winning_hand(self, hand):
        # Changes the hand chosen by player to a number and gives a random
        # number between(0, 2) to the computer.
        hands = ["Rock", "Paper", "Scissors"]
        player = hands.index(hand)
        computer = randint(0, 2)

        # The ways where the player wins and changing the score.
        if player > computer and [computer, player] != [0, 2]\
                or player == 0 and computer == 2:
            self.__p_points += 1
            self.__player_points.configure(
                text=f"Player: {self.__p_points} wins")
            # Message shown after one round if player wins
            tkinter.messagebox.showinfo(f"R-P-S", f"Computer chose "
                                                  f"{hands[computer]}.\n"
                                                  f"The Player wins!")
            # Starts a new game
            self.new_game()
        # The ways where the Computer wins and changing the score.
        elif computer > player or player == 2 and computer == 0:
            self.__c_points += 1
            self.__computer_points.configure(
                text=f"Computer: {self.__c_points} wins")
            # Message shown after one round if computer wins
            tkinter.messagebox.showinfo(f"R-P-S", f"Computer chose "
                                                  f"{hands[computer]}.\n"
                                                  f"The Computer wins!")
            self.new_game()
        else:
            # Message shown after one round if it's a tie.
            tkinter.messagebox.showinfo(f"R-P-S", f"Computer chose "
                                                  f"{hands[computer]}.\n"
                                                  f"It's a tie!")
            self.new_game()

    # Method deletes all the nfo that needs to be deleted for the new game
    # to start.
    def new_game(self):
        buttons = [self.__rock, self.__paper, self.__scissors]

        for button in buttons:
            button.configure(background="SteelBlue1")

    # Method deletes all the nfo that needs to be deleted for the new game
    # to start.
    def reset(self):
        self.__p_points = 0
        self.__c_points = 0

        self.__player_points.configure(text=f"Player: {self.__p_points} wins")
        self.__computer_points.configure(text=f"Computer: "
                                              f"{self.__c_points} wins")

    # Method is called if help button if pressed. A message containing
    # the info is shown
    def help(self):
        help_txt = ("The game is played where players deliver hand signals "
                    "that will represent the elements of the game;\n"
                    " rock, paper and scissors. You are playing against "
                    "the computer \n"
                    "The outcome of the game is determined by 3 simple rules:\n"
                    "\n1. Rock wins against scissors.\n"
                    "\n2. Scissors win against paper.\n"
                    "\n3. Paper wins against rock. ")

        tkinter.messagebox.showinfo("RULES FOR Rock-Paper-Scissors", help_txt)

    # Method makes sure when quitting the game, the main window is opened
    def on_closing(self):
        self.__interface.destroy()
        main_menu = MainPage()


def main():
    MainPage()


if __name__ == "__main__":
    main()
