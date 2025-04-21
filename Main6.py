import customtkinter as ctk
from tkinter import messagebox, simpledialog
import random
from words import word_list 



def get_word():
    return random.choice(word_list).upper()

class HangmanGame:
    def __init__(self, root, mode, rounds):

        self.root = root
        self.set_default_window()

        
        self.default_width = 1280
        self.default_height = 800
        self.aspect_ratio = 16 / 10

        self.setup_responsive_callbacks()
        self.mode = mode  
        self.rounds = rounds * (2 if mode == "pvp" else 1)  
        self.rounds_counter = int(self.rounds / 2 if mode == "pvp" else self.rounds)
        self.current_round = 0
        self.current_round_count = 1
        self.scores = [0, 0]  

        self.players = ["Player 1", "Player 2"] if self.mode == "pvp" else ["Player", "Bot"]
        self.current_role = 0  
        self.current_guesser = 1 if self.mode == "pvp" else 0 

        if not self.setup_game():  
            self.back_to_menu()
            return

        self.word_completion = " ".join("_" * len(self.word))
        self.tries = 6
        self.guessed_letters = []
        self.guessed_words = []

        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        self.label_round = ctk.CTkLabel(self.root, text=f"Round {self.current_round_count} of {self.rounds_counter}",
                                        text_color="#083D77", font=("Arial", 18))
        self.label_round.place(relx=0.5, rely=0.1, anchor="center") 

        self.label_player = ctk.CTkLabel(self.root, text=f"{self.players[self.current_guesser]}'s turn to guess",
                                         text_color="#083D77", font=("Arial", 18))
        self.label_player.place(relx=0.5, rely=0.2, anchor="center")

        self.label_word = ctk.CTkLabel(self.root, text=self.word_completion,
                                       text_color="#083D77", font=("Arial", 24))
        self.label_word.place(relx=0.5, rely=0.3, anchor="center")

        self.entry_guess = ctk.CTkEntry(self.root, placeholder_text="Guess the word", font=("Arial", 18))
        self.entry_guess.place(relx=0.5, rely=0.4, anchor="center")

        self.button_submit = self.create_button(self.root, "Submit Guess", self.process_guess)
        self.button_submit.place(relx=0.5, rely=0.5, anchor="center")

        self.label_tries = ctk.CTkLabel(self.root, text=self.display_hangman(),
                                        font=("Courier", 18), justify="left")
        self.label_tries.place(relx=0.7, rely=0.33, anchor="center")

        self.used_alphabets = ctk.CTkLabel(self.root, text="used alphabets: ",
                                           text_color="#083D77", font=("Arial", 18), justify="left")
        self.used_alphabets.place(relx=0.22, rely=0.3, anchor="w")

        if self.mode == "bot":
            self.button_restart = self.create_button(self.root, "Restart Game", self.restart_game)
            self.button_restart.place(relx=0.5, rely=0.6, anchor="center")

        self.back_button = self.create_button(self.root, "Back to Menu", self.back_to_menu)
        self.back_button.place(relx=0.5, rely=0.7, anchor="center")

    def create_button(self, parent, text, command):
        button = ctk.CTkButton(parent, text=text, font=('Arial', 16), command=command)
        button.bind("<Enter>", lambda e: button.configure(bg="lightgrey"))
        button.bind("<Leave>", lambda e: button.configure(bg="SystemButtonFace"))
        return button

    def display_hangman(self):
        stages = [
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
               -      
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / 
               -      
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |      
               -      
            """,
            """
               --------
               |      |
               |      O
               |     \\|
               |      |
               |     
               -      
            """,
            """
               --------
               |      |
               |      O
               |      |
               |      |
               |     
               -      
            """,
            """
               --------
               |      |
               |      O
               |    
               |      
               |     
               -      
            """,
            """
               --------
               |      
               |      
               |    
               |      
               |     
               -      
            """
        ]
        return stages[self.tries]

    def process_guess(self):
        guess = self.entry_guess.get().upper()

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                messagebox.showinfo("Hangman", f"You already guessed the letter {guess}")
            elif guess not in self.word:
                messagebox.showinfo("Hangman", f"{guess} is not in the word.")
                self.tries -= 1
                self.guessed_letters.append(guess)
                self.update_used_guesses()
            else:
                messagebox.showinfo("Hangman", f"Good job! {guess} is in the word!")
                self.guessed_letters.append(guess)
                word_as_list = list(self.word_completion.replace(" ", ""))
                indices = [i for i, letter in enumerate(self.word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                self.word_completion = " ".join(word_as_list)

        elif len(guess) == len(self.word) and guess.isalpha():
            if guess in self.guessed_words:
                messagebox.showinfo("Hangman", f"You already guessed the word {guess}")
            elif guess != self.word:
                messagebox.showinfo("Hangman", f"{guess} is not the correct word.")
                self.tries -= 1
                self.guessed_words.append(guess)
            else:
                self.word_completion = " ".join(self.word)
                self.end_game(True)
        else:
            messagebox.showwarning("Hangman", f"Not a valid guess. Please enter a word with {len(self.word)} letters.")

        self.update_gui()

    def update_gui(self):
        self.label_word.configure(text=self.word_completion)
        self.label_tries.configure(text=self.display_hangman())
        self.entry_guess.delete(0, 'end')
        self.update_used_guesses()

        if "_" not in self.word_completion.replace(" ", ""):
            self.end_game(True)
        elif self.tries == 0:
            self.end_game(False)

    def update_used_guesses(self):
       
        used_guesses_text = "used Guesses:\n" + ", ".join(self.guessed_letters)
        self.used_alphabets.configure(text=used_guesses_text)

    def end_game(self, won):
        if won:
            messagebox.showinfo("Hangman", f"Congrats, {self.players[self.current_guesser]}! You guessed the word!")
            self.scores[self.current_guesser] += 1
        else:
            messagebox.showinfo("Hangman", f"Sorry, {self.players[self.current_guesser]}! The word was {self.word}")

        self.current_round += 1

        if self.current_round % 2 == 0 and (self.current_round / 2) < self.rounds_counter and self.mode == "pvp":
            self.current_round_count += 1
        elif self.mode == "bot" and self.current_round < self.rounds_counter:
            self.current_round_count += 1
        self.label_round.configure(text=f"Round {self.current_round_count} of {self.rounds_counter}")

        if self.current_round < self.rounds:
            self.restart_game()
        else:
            self.show_final_scores()


    def restart_game(self):
        self.root.bell(False)
        if self.mode == "bot" or (self.current_round == self.rounds and self.rounds == 7):
            self.word = get_word()
        elif self.mode == "pvp":
            self.switch_roles()
            self.word = self.get_pvp_word()
            if self.word is None: 
                self.back_to_menu()
                return
        self.update_used_guesses()
        self.word_completion = " ".join("_" * len(self.word))
        self.tries = 6
        self.guessed_letters = []
        self.guessed_words = []
        self.update_gui()

    def switch_roles(self):
        self.current_role, self.current_guesser = self.current_guesser, self.current_role
        self.label_player.configure(text=f"{self.players[self.current_guesser]}'s turn to guess")

    def show_final_scores(self):
        score_message = f"Final Scores:\n{self.players[0]}: {self.scores[0]}\n{self.players[1]}: {self.scores[1]}"
        messagebox.showinfo("Game Over", score_message)
        self.back_to_menu()

    def setup_game(self):
        if self.mode == "pvp":
            self.players[0] = simpledialog.askstring("Player Name", "Enter name for Player 1:")
            if self.players[0] is None:
                return False
            self.players[1] = simpledialog.askstring("Player Name", "Enter name for Player 2:")
            if self.players[1] is None:
                return False
            self.word = self.get_pvp_word()
        elif self.mode == "bot":
            self.word = get_word()
        return self.word is not None

    def get_pvp_word(self):
        while True:
            word = simpledialog.askstring(f"{self.players[self.current_role]}'s Turn", "Enter a word for the guesser:")
            if word is None:
                return None
            if word.isalpha():
                return word.upper()
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid word.")

    def back_to_menu(self):
        self.root.destroy()
        choose_mode()

    def set_default_window(self):
        self.root.geometry("1280x800")  
        self.root.title("Hangman Game")
        self.root.configure(fg_color="#00E2AD")
        self.root.minsize(640, 400)  

    def setup_responsive_callbacks(self):
       
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
       
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height
            expected_height = new_width // 16 * 10

            if new_height != expected_height:
                self.root.geometry(f"{new_width}x{expected_height}")

           
            font_scale = new_width / 1280 
            self.scale_fonts(font_scale)

    def scale_fonts(self, scale):
      
        self.label_round.configure(font=("Arial", int(18 * scale)))
        self.label_player.configure(font=("Arial", int(18 * scale)))
        self.label_word.configure(font=("Arial", int(24 * scale)))
        self.entry_guess.configure(font=("Arial", int(18 * scale)))
        self.label_tries.configure(font=("Courier", int(18 * scale)))
        self.used_alphabets.configure(font=("Arial", int(18 * scale)))

    def update_widget_sizes(self, width, height):
      
        scale_x = width / self.default_width
        scale_y = height / self.default_height
        font_scale = min(scale_x, scale_y)

        self.label_round.configure(font=("Arial", int(18 * font_scale)))
        self.label_player.configure(font=("Arial", int(18 * font_scale)))
        self.label_word.configure(font=("Arial", int(24 * font_scale)))
        self.entry_guess.configure(font=("Arial", int(18 * font_scale)))
        self.label_tries.configure(font=("Courier", int(18 * font_scale)))
        self.used_alphabets.configure(font=("Arial", int(18 * font_scale)))
       

      
        self.label_tries.place(relx=0.44, rely=0.55, anchor="center")
        self.used_alphabets.place(relx=0.05, rely=0.3)

def choose_limit(mode):
    def set_rounds(rounds):
        limit_window.after_cancel("all")
        limit_window.destroy()  
        root = ctk.CTk()
        game = HangmanGame(root, mode, rounds)
        root.mainloop()  

    limit_window = ctk.CTk()
    limit_window.geometry("1280x800")
    limit_window.title("Choose Game Limit")
    limit_window.configure(fg_color="#00E2AD")

    ctk.CTkLabel(limit_window, text="Select Game Limit:",text_color="#083D77", font=("Arial", 24)).pack(pady=50)

    ctk.CTkButton(limit_window, text="The Coin (1 Round)", font=("Arial", 18), command=lambda: set_rounds(1)).pack(pady=20)
    ctk.CTkButton(limit_window, text="The Triangle (3 Rounds)", font=("Arial", 18), command=lambda: set_rounds(3)).pack(pady=20)
    ctk.CTkButton(limit_window, text="The Dice (6 Rounds)", font=("Arial", 18), command=lambda: set_rounds(6)).pack(pady=20)
    ctk.CTkButton(limit_window, text="Russian Roulette (7 Rounds)", font=("Arial", 18), command=lambda: set_rounds(7)).pack(pady=20)

    ctk.CTkButton(limit_window, text="Cancel", font=("Arial", 18), command=lambda: [limit_window.destroy(), choose_mode()]).pack(pady=20)

    limit_window.mainloop()

def choose_mode():
    mode_window = mode_window = ctk.CTk()
    mode_window.geometry("1280x800")
    mode_window.title("Choose Game Mode")
    mode_window.configure(fg_color="#00E2AD")

    def start_game(mode):
        mode_window.after_cancel("all")
        mode_window.destroy()
        choose_limit(mode)

    ctk.CTkLabel(mode_window, text="Select Game Mode:",text_color="#083D77", font=("Arial", 24)).pack(pady=50)
    ctk.CTkButton(mode_window, text="Play vs Bot", font=("Arial", 18), command=lambda: start_game("bot")).pack(pady=20)
    ctk.CTkButton(mode_window, text="Player vs Player", font=("Arial", 18), command=lambda: start_game("pvp")).pack(pady=20)
    mode_window.after_cancel("all")
    ctk.CTkButton(mode_window, text="Exit", font=("Arial", 18), command=mode_window.destroy).pack(pady=20)

    mode_window.mainloop()

choose_mode()
