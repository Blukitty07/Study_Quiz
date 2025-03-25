from tkinter import *
from functools import partial  # To prevent unwanted windows


class StartGame:
    """
    Initial Game Interface (asks users how many
    rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(pady=10, padx=10)
        self.start_frame.grid()

        # create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        rounds_wanted = 5
        self.to_play()

    def to_play(self):
        """
        Invokes game GUI and takes acoss number of rounds to be played
        """
        Play()
        # Hide root window (ie: hide rounds choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the Studies Quiz Game
    """

    def __init__(self):
        self.rounds_won = IntVar()
        self.rounds_wanted = IntVar()
        self.rounds_played = IntVar()

        # Lists for stats component
        # all correct
        # self.rounds_played.set(7)
        # self.rounds_wanted.set(8)
        # self.rounds_won.set(7)

        # all wrong
        self.rounds_played.set(6)
        self.rounds_wanted.set(15)
        self.rounds_won.set(0)
        self.questions = ["What is b", "What is ee", "What is yy", "What is babbory", "What is regkd"]
        self.answers = []

        # Random Score Test Data
        # self.rounds_played.set(6)
        # self.rounds_wanted.set(10)
        # self.rounds_won.set(4)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Studies Quiz", font=("Arial", "16", "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round stats
        """

        # IMPORTANT: retrieve number of rounds
        # won as a number (rather than the self container)
        rounds_won = self.rounds_won.get()
        rounds_wanted = self.rounds_wanted.get()
        rounds_played = self.rounds_played.get()
        questions = self.questions
        answers = self.answers
        stats_bundle = [rounds_won, rounds_played, rounds_wanted, questions, answers]

        Stats(self, stats_bundle)


class Stats:

    def __init__(self, partner, all_stats_info):

        # Extract information from master list
        user_score = all_stats_info[0]
        rounds_played = all_stats_info[1]
        rounds_wanted = all_stats_info[2]
        questions = all_stats_info[3]
        answers = all_stats_info[4]

        # setup dialog box
        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes stats and releases stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300)
        self.stats_frame.grid()

        # Math to populate Stats Dialogue
        success_rate = user_score / rounds_played * 100
        total_score = user_score
        max_possible = rounds_wanted

        # high score do later

        # Strings for stats Labels

        success_string = (f"Success Rate: {user_score} / {rounds_played}"
                          f" ({success_rate:.1f}%)")
        score_string = f"Current Score: {total_score}"
        # best score do later

        # custom comment text and formatting
        if total_score == rounds_played:
            comment_string = "Wow! You got every question right!"
            comment_colour = "#ccffcc"

        elif total_score == 0:
            comment_string = "Oh no! You haven't gotten any question right - Yet!"
            comment_colour = "#F8CECC"
            best_score_string = f"Best Score: n/a"
        else:
            comment_string = ""
            comment_colour = "#bdeaff"

        question_answered_string = f"Questions Answered: {rounds_played} of {rounds_wanted}"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label list (text | font | 'Sticky')
        all_stats_string = [
            ["Statistics", heading_font, ""],
            [question_answered_string, normal_font, "W"],
            [success_string, normal_font, "W"],
            [score_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_string):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", bg="#bdeaff",
                                     pady=5, padx=30)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

        # 5 most recent answers and if they were correct or not
        new_q_list = list(questions)

        # question display box frame
        self.history_frame = Frame(self.stats_frame, width=200, padx=20, pady=20)
        self.history_frame.grid(row=8)

        # display questions inside frame
        for count, item in enumerate(new_q_list):
            self.past_questions = Label(self.history_frame, text=item[count], font=("Arial", "14"))
            self.past_questions.grid(row=count)

        # dismiss button
        self.dismiss_button = Button(self.stats_frame, font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#5a93ad",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=9, padx=10, pady=10)

        self.stats_frame.config(bg="#bdeaff")

    # closes stats dialogue (used by button and x at top of corner)

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button)
        """
        # Put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Studies Quiz")
    StartGame()
    root.mainloop()
