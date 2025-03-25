from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


# functions for classes and helping go here
def get_studies():
    """
    Retrieves studies from csv file
    :return: list of studies which where each list item has the
     study name, and what the study is about
    """
    # Retrieve studies for csv file and put them in a list
    file = open("study_of.csv", "r")
    all_studies = list(csv.reader(file, delimiter=","))
    file.close()

    # remove first row
    all_studies.pop(0)

    return all_studies


def get_study_names():
    """
    Choose four studies from larger list ensuring that they're all different
    :return: list of studies
    """

    all_study_list = get_studies()

    study_names = []
    study_types = []

    # loop until we have four studies that are all different fields of study
    while len(study_names) < 4:
        potential_study = random.choice(all_study_list)

        # get the study type and check it's not a duplicate
        if potential_study[1] not in study_types:
            actual_rad_study = potential_study[1].replace("Study of ", "")
            study_types.append(actual_rad_study)

            # append the study name to the list for the round
            study_names.append(potential_study[0])

    return study_names, study_types


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
        # prepare to see which button is clicked
        first_mode_click = "first"
        second_mode_click = "second"
        # make the buttons
        self.first_mode_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                        bg="#73fffd", text="Mode 1", width=10, height=2,
                                        command=lambda: [self.check_rounds(first_mode_click)])
        self.first_mode_button.grid(row=0, column=0, padx=5, pady=5)

        self.second_mode_button = Button(self.start_frame, font=("Arial", "16", "bold"), fg="#FFFFFF",
                                         bg="#1d0eab", text="Mode 2", width=10, height=2,
                                         command=lambda: [self.check_rounds(second_mode_click)])
        self.second_mode_button.grid(row=0, column=1, pady=5, padx=5)

    def check_rounds(self, mode):
        """
        Checks users have entered 1 or more rounds
        """

        Play(5, mode)

        # Hide root window
        root.withdraw()


class Play:
    """
    Interface for playing the study quiz
    """

    def __init__(self, how_many, mode):

        # rounds played - start with zero
        self.round_number_ref = ""
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # study lists and score list
        self.round_study_names_list = []
        self.round_study_types_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # List for label details (text | font | background | row)
        play_labels_list = [
            [f"Round 0 of {how_many}", ("Arial", "16", "bold"), None, 0],
            [f"Current Score: 0", ("Arial", "12"), "#D5E8D4", 1],
            [f"{mode} mode. example Question", ("Arial", "13"), "#FFF2CC", 2],
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve labels so they can be configured later
        self.round_label = play_labels_ref[0]
        self.score_label = play_labels_ref[1]
        self.question_label = play_labels_ref[2]

        # set up answer frame
        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=3)

        self.answer_button_ref = []
        self.button_list = []

        # set up backgrounds for the buttons
        background_ref_list = [
            "#d2ffc9", "#e6ebb2", "#9dd19d", "#c6d998"
        ]

        # create the four answer buttons in a 2x2 grid
        for item in range(0, 4):
            self.answer_button = Button(self.answer_frame, font=("Arial", "12"),
                                        text="answer option", width=16,
                                        bg=background_ref_list[item], command=partial(self.get_score, item))
            self.answer_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

            self.answer_button_ref.append(self.answer_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # set up score
        self.score = 0

        # list for buttons (frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.game_frame, "Next Round", "#86a5c4", lambda: [self.new_round(mode)], 21, 5, None],
            [self.hints_stats_frame, "Hints", "#c0bdff", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#bdeaff", "", 10, 0, 1],
            [self.game_frame, "Game Over", "#cc81a5", self.close_play, 21, 7, None]
        ]

        # create buttons and add to list
        controls_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "15"),
                                         fg="#000000", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], pady=5, padx=5)

            controls_ref_list.append(make_control_button)

        # retrieve next, stats and end button so that they can be configured
        self.next_button = controls_ref_list[0]
        self.hints_button = controls_ref_list[1]
        self.stats_button = controls_ref_list[2]
        self.end_game_button = controls_ref_list[3]

        # Once interface has been created, invoke new round
        # function for the first round
        self.new_round(mode)

    def new_round(self, mode):
        """
        Choose four studies, works out media for score to beat.
        Configures buttons with the choose number
        """

        # retrieve number of rounds played. add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round studies and their names
        study_names, study_types = get_study_names()

        # Update heading, and score to beat labels. "Hide" results label
        self.round_label.config(text=f"Round {rounds_played} of {rounds_wanted}")

        # also get the same name attached to the study and make it the correct answer [half of this in get_score]
        # set up number list to select a single option from the options for this round
        number_list = [0, 1, 2, 3]
        self.round_number_ref = random.choice(number_list)
        study_type = study_types[self.round_number_ref]
        study_name = study_names[self.round_number_ref]

        # enable answer buttons and make questions / answers for this round
        if mode == "first":
            questions = study_names
            self.question_label.config(text=f"What is the Study of {study_type}?")
        else:
            questions = study_types
            self.question_label.config(text=f"{study_name} is the Study of what?")

        for count, item in enumerate(self.answer_button_ref):
            item.config(text=questions[count], wraplength=140, state=NORMAL)

        # disabled until answer is chosen
        self.next_button.config(state=DISABLED)

    def get_score(self, user_choice):
        """
        Retrieves which button was pushed (index 0-3), retrieves
        score and then compares it with median,updates results and adds
        results to stats list
        """

        if user_choice == self.round_number_ref:
            self.score += 1  # add 1 to score
            self.score_label.config(text=f"Current Score: {self.score}")
        else:
            pass

        # enable stats & next buttons, disable answer buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        # if no more rounds reconfigure buttons [set up to proceed to end game GUI]
        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="No more Rounds")
            self.end_game_button.config(text="End Screen", bg="#de8e99", command=self.close_play)

        for item in self.answer_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie choose rounds) and end
        # current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hints(self):
        """
        Displays hints for playing game
        """
        DisplayHints(self)


class DisplayHints:

    def __init__(self, partner):
        # setup dialog box and background colour
        background = "#c0bdff"
        self.hint_box = Toplevel()

        # disable hint button
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes hint and releases hint button
        self.hint_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hints, partner))

        self.hint_frame = Frame(self.hint_box, width=300,
                                height=200)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame,
                                        text="Hints",
                                        font=("Arial", "14", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "This is a quiz about the various types of studies. \n" \
                    "Depending on the Mode that you picked the questions will either ask:\n" \
                    "What is the Study of ___ or ___ is the study of what? \n" \
                    "In either case you need to select the correct answer out of 4 possible choices. \n"\
                    "If you select the correct one then 1 point will be added to your score!"

        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, wraplength=350,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hint_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#7571d9",
                                     fg="#FFFFFF",
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.hint_frame, self.hint_heading_label, self.hint_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_hints(self, partner):
        """
        Closes hint dialogue box (and enables hint button)
        """
        # Put hint button back to normal
        partner.hints_button.config(state=NORMAL)
        self.hint_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Studies Quiz")
    StartGame()
    root.mainloop()
