from tkinter import *
from PIL import Image, ImageTk
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


# gets the names and study types for round
def get_study_names():
    """
    Choose four studies from larger list ensuring that they're all different
    :return: list of studies
    """

    all_study_list = get_studies()

    study_names = []
    study_types = []

    # loop until we have four studies that are all different fields of study
    while len(study_names) < 3:
        potential_study = random.choice(all_study_list)

        # get the study type and check it's not a duplicate
        if potential_study[1] not in study_types:
            actual_rad_study = potential_study[1].replace("Study of ", "")
            study_types.append(actual_rad_study)

            # append the study name to the list for the round
            study_names.append(potential_study[0])

    return study_names, study_types


# opens file and create lists for leaderboard
def open_file():
    file_name = "previous_top_scores.txt"
    try:
        with open(file_name, "r") as file:
            result = file.read().split()
            names = result[::2]
            points = result[1::2]

            return names, points

    except FileNotFoundError:
        with open(file_name, "w") as file:
            file.close()
            names = ""
            points = ""
            return names, points


def round_question(mode):
    """
    Choose a question from larger list
    :return: question
    """

    all_study_list = get_studies()
    question = ""
    answer = ""

    potential_question = random.choice(all_study_list)

    # get the study type and check it's not a duplicate
    if mode == "first":
        actual_rad_study = potential_question[1].replace("Study of ", "")
        question = actual_rad_study
        answer = potential_question[0]

    else:
        # append the study name to the list for the round
        question = potential_question[0]
        actual_rad_answer = potential_question[1].replace("Study of ", "")
        answer = actual_rad_answer

    return question, answer


class StartGame:
    """
    Initial starting screen
    """

    def __init__(self):
        """
        gets no. rounds from users input
        """

        # set up the start frame
        self.start_frame = Frame(pady=10, padx=10)
        self.start_frame.grid()

        # Load the image
        image = Image.open('study.jpg')

        # Resize the image in the given (width, height)
        img = image.resize((320, 223))

        # Converse the image in TkImage
        my_img = ImageTk.PhotoImage(img)

        # Display the image with label
        display_image = Label(self.start_frame, image=my_img, background="#000000")
        display_image.image = my_img  # anchoring the image to prevent garbage collection
        display_image.grid(row=0)

        # Set up strings
        mode_string = ("Put the amount of rounds you wish to play into the box. "
                       "\n" "Then select one of the Modes \n"
                       "Mode 1: What is the Study of? \n" "Mode 2: This is what study?")

        # list of labels to be made(text | font | font colour)
        # currently only one text, but prepared for potential future
        start_game_labels_list = [
            [mode_string, ("Arial", "13"), None]
        ]

        # create the labels and add them to a reference list
        start_game_labels_ref = []

        for count, item in enumerate(start_game_labels_list):
            make_the_label = Label(self.start_frame, text=item[0],
                                   font=item[1], fg=item[2], padx=10, pady=5)
            make_the_label.grid(row=1)

            start_game_labels_ref.append(make_the_label)

        self.mode_label = start_game_labels_ref[0]

        # make entry box for amount of rounds
        self.amount_of_rounds = Entry(self.start_frame, font=("Arial", "14", "bold"), width=30)
        self.amount_of_rounds.grid(row=2, padx=10, pady=10)

        # made the frame for the buttons
        self.mode_button_frame = Frame(self.start_frame, padx=10)
        self.mode_button_frame.grid(row=3)

        # prepare to see which button is clicked
        first_mode_click = "first"
        second_mode_click = "second"
        # make the buttons
        self.first_mode_button = Button(self.mode_button_frame, font=("Arial", "16", "bold"),
                                        bg="#73fffd", text="Mode 1", width=10, height=2,
                                        command=lambda: [self.check_rounds(first_mode_click)])
        self.first_mode_button.grid(row=0, column=0, padx=5, pady=5)

        self.second_mode_button = Button(self.mode_button_frame, font=("Arial", "16", "bold"), fg="#FFFFFF",
                                         bg="#1d0eab", text="Mode 2", width=10, height=2,
                                         command=lambda: [self.check_rounds(second_mode_click)])
        self.second_mode_button.grid(row=0, column=1, pady=5, padx=5)

        self.leaderboard_button = Button(self.start_frame, font=("Arial", "16", "bold"), fg="#000000", bg="#ceabdb",
                                         text="Leaderboard", width=10, height=2, command=self.to_end)
        self.leaderboard_button.grid(row=4)

    def check_rounds(self, mode):
        """
        checks that 1 or more rounds have been entered
        """

        # get the amount of rounds
        rounds_wanted = self.amount_of_rounds.get()

        # Reset label and entry box (for when users come back to home screen)
        self.mode_label.config(
            text=("Put the amount of rounds you wish to play into the box. \n"
                  "Then select one of the Modes \n"
                  "Mode 1: What is the Study of? \n"
                  "Mode 2: This is what study?"),
            fg="#000000", font=("Arial", "12", "bold"))
        self.amount_of_rounds.config(bg="#FFFFFF")

        # set up strings
        error = "Please enter a whole number more than 0"
        error_check = "Nope"

        # appropriate amount of rounds checker
        try:
            rounds_wanted = int(rounds_wanted)
            # correct amount of rounds
            if rounds_wanted >= 1:
                Play(rounds_wanted, mode)
                # Hide root window (ie: hide round choice window)
                root.withdraw()

            # incorrect amount of rounds
            else:
                error_check = "yes"
        # wrong values
        except ValueError:
            error_check = "yes"

        # display the error if necessary
        if error_check == "yes":
            self.mode_label.config(text=error, fg="#c20000", font=("Arial", "10", "bold"))
            self.amount_of_rounds.config(bg="#F4CCCC")
            self.amount_of_rounds.delete(0, END)

    def to_end(self):
        """
        Gets score and brings player to leaderboard
        """
        score = 0
        mode_type = "start"
        Leaderboard(score, mode_type)


class Play:
    """
    Interface for playing the study quiz
    """

    def __init__(self, how_many, mode):

        # stuff for the questions
        self.warning_label = ""
        self.input_place = 0
        self.round_questions = []

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

        # If users press cross at top, closes hint and releases hint button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # List for label details (text | font | background | row)
        play_labels_list = [
            [f"Question 0 of {how_many}", ("Arial", "16", "bold"), None, 0],
            [f"Score: 0", ("Arial", "12"), "#D5E8D4", 1],
            [f"{mode} mode. example Question", ("Arial", "13"), "#FFF2CC", 2]
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

        self.warning_time = False

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
        self.hints_stats_frame.grid(row=8)

        # set up score
        self.score = 0

        # list for buttons (frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.game_frame, "Next Round", "#86a5c4", lambda: [self.new_round(mode)], 21, 7, None],
            [self.hints_stats_frame, "Instructions", "#c0bdff", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#bdeaff", self.to_stats, 10, 0, 1],
            [self.game_frame, "Main Menu", "#cc81a5", self.close_play, 21, 9, None]
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

        # set up warning label
        self.warning_label = Label(self.game_frame, text="You have answered all questions, they are now repeating",
                                   font=("Arial", "13"), bg="#F8CECC")
        self.warning_label.grid(row=6)

        rounds_wanted = self.rounds_wanted.get()

        # get round studies and their names
        study_names, study_types = get_study_names()

        questions_so_far = self.round_questions

        question, answer = round_question(mode)

        if len(questions_so_far) == 273:
            questions_so_far.clear()
            self.warning_time = True
        else:
            self.warning_label.destroy()
            self.warning_time = False

        while question in questions_so_far:
            question = round_question(mode)

        questions_so_far.append(question)

        if self.warning_time:
            self.warning_time = False

        # prepare to input the answer into a specific place
        number_list = [0, 1, 2, 3]
        self.input_place = random.choice(number_list)

        # Update heading, and score to beat labels. "Hide" results label
        self.round_label.config(text=f"Question {rounds_played} of {rounds_wanted}")

        # enable answer buttons and make questions / answers for this round
        if mode == "first":
            study_names.insert(self.input_place, answer)
            round_questions = study_names
            self.question_label.config(text=f"What is the Study of {question}?")

        else:
            study_types.insert(self.input_place, answer)
            round_questions = study_types
            self.question_label.config(text=f"{question} is the Study of what?")

        # set up backgrounds for the buttons
        background_ref_list = [
            "#d2ffc9", "#e6ebb2", "#9dd19d", "#c6d998"
        ]

        for count, item in enumerate(self.answer_button_ref):
            item.config(text=round_questions[count], bg=background_ref_list[count], wraplength=140, state=NORMAL)

        # disabled until answer is chosen
        self.next_button.config(state=DISABLED)

    def get_score(self, user_choice):
        """
        Retrieves which button was pushed (index 0-3), retrieves
        score and then compares it with median,updates results and adds
        results to stats list
        """

        if user_choice == self.input_place:
            self.score += 1  # add 1 to score
            self.score_label.config(text=f"Score: {self.score}")
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
            self.next_button.config(text="Leaderboard", bg="#ceabdb", command=self.to_end)
            self.end_game_button.config(text="Play Again", bg="#7abf81", command=self.close_play)

        for item in self.answer_button_ref:
            item.config(state=DISABLED, bg="#d6d6d6")

        # change colour to reflect correct answer
        number = int(self.input_place)
        self.answer_button_ref[number].config(bg="#42d442")

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

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round stats
        """

        # IMPORTANT: retrieve number of rounds
        # won as a number (rather than the self container)
        rounds_won = self.score
        rounds_wanted = self.rounds_wanted.get()
        rounds_played = self.rounds_played.get()
        stats_bundle = [rounds_won, rounds_played, rounds_wanted]

        Stats(self, stats_bundle)

    def to_end(self):
        """
        Gets score and brings player to leaderboard
        """
        score = self.score
        mode_type = ""
        Leaderboard(score, mode_type)


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
                                        text="Instructions",
                                        font=("Arial", "16", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "This is a quiz about the various types of studies in the world. \n" \
                    "Depending on what Mode you picked the questions will either ask:\n" \
                    "Mode 1: What is the Study of ___ \n" \
                    "OR \n" \
                    "Mode 2: ___ is the study of what? \n" \
                    "In either case you need to select the correct answer out of 4 possible choices. \n" \
                    "If you select the correct one then 1 point will be added to your score!"

        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, wraplength=350,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hint_frame,
                                     font=("Arial", "15", "bold"),
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


class Stats:

    def __init__(self, partner, all_stats_info):

        # Extract information from master list
        user_score = all_stats_info[0]
        rounds_played = all_stats_info[1]
        rounds_wanted = all_stats_info[2]

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
            comment_colour = "#3eed3e"

        elif total_score == 0:
            comment_string = "Oh no! You haven't gotten any question right - Yet!"
            comment_colour = "#F8CECC"
            best_score_string = f"Best Score: n/a"
        else:
            comment_string = ""
            comment_colour = "#ccffcc"

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
                                     anchor="w", justify="left", bg="#ccffcc",
                                     pady=5, padx=30)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#458045",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

        self.stats_frame.config(bg="#ccffcc")

    # closes stats dialogue (used by button and x at top of corner)

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button)
        """
        # Put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


class Leaderboard:
    """
    Interface for playing the study quiz
    """

    def __init__(self, score, mode_type):
        self.end_box = Toplevel()

        self.end_frame = Frame(self.end_box)
        self.end_frame.grid(padx=10, pady=10)

        # body font for most labels
        body_font = ("Arial", "12")

        # open file and grab the names and points
        leader_name_list, leader_point_list = open_file()

        # make a box to display leaderboard in
        self.leaderboard_frame = Frame(self.end_frame, bg="#ffa6d4")
        self.leaderboard_frame.grid(row=1)

        # heading
        self.heading = Label(self.end_frame, text="Leaderboard", font=("Arial", "16", "underline", "bold"))
        self.heading.grid(row=0, pady=5)

        # names and points displayed
        leaderboard_list = []
        for count, item in enumerate(leader_name_list):
            self.make_label = Label(self.leaderboard_frame, text=f"{leader_name_list[count]} -- "
                                                                 f"{leader_point_list[count]} points", font=body_font,
                                    bg="#ffa6d4",
                                    wraplength=300, justify="left")
            self.make_label.grid(row=count)
            leaderboard_list.append(self.make_label)

        # detect points compare to current score. if current score is higher than the lowest score ask for input
        length_leaderboard = len(leaderboard_list)
        if length_leaderboard == 0:
            low_point = 0
            if mode_type == "start":
                no_score = Label(self.leaderboard_frame, text="There are no scores yet!", bg="#ffa6d4",
                                 font=body_font)
                no_score.grid(row=2)
            else:
                first_score = Label(self.leaderboard_frame, text="You're the first to win!", bg="#ffa6d4",
                                    font=body_font)
                first_score.grid(row=2)

        else:
            lowest_point = leader_point_list[-1]
            low_point = int(lowest_point)

        # frame for the name entry
        self.winner_frame = Frame(self.end_frame)
        self.winner_frame.grid(row=3)

        # define the lists of names and points to be carried over in functions
        self.leader_name_list = leader_name_list
        self.leader_point_list = leader_point_list

        if score > low_point:
            self.winners_name = Entry(self.winner_frame, font=("Arial", "20", "bold"), width=8)
            self.winners_name.grid(row=0, column=0, pady=10)

            self.winner_submit_button = Button(self.winner_frame, text="Submit", font=("Arial", "14", "bold"),
                                               command=lambda: [self.check_name(score)], bg="#ceabdb", width=9)
            self.winner_submit_button.grid(row=0, column=1)

        else:
            pass

        # after button to submit name and points is pushed resort points and write to list

        # heading to make the error area [forget afterwards]
        self.error_message = Label(self.end_frame, text="error_label", font=("Arial", "14", "bold"), fg="#c20000")
        self.error_message.place_forget()

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.end_frame)
        self.hints_stats_frame.grid(row=4)

        # list for buttons (frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.end_frame, "Play Again", "#cc81a5", self.back_to_start, 21, 7, None]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "15"),
                                         fg="#000000", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], pady=5, padx=5)

            control_ref_list.append(make_control_button)

        if mode_type == "start":
            play_again = control_ref_list[0]
            play_again.config(text="Main Menu")

    def check_name(self, score):
        name_entry = self.winners_name.get()

        if len(name_entry) == 3:

            if name_entry.isalpha():
                self.error_message.grid(row=2)
                self.error_message.config(text="The leaderboard will now be updated", fg="#25db30")
                self.winner_frame.grid_forget()
                self.update_leaderboard(score)

                # function to add it to the file?

            else:
                self.error_message.grid(row=2)
                self.error_message.config(text="Please enter do not enter numbers")
                # label to tell them no
                # don't accept input

        else:
            self.error_message.grid(row=2)
            self.error_message.config(text="Please enter exactly 3 letters\n"
                                           "for your name")

    def update_leaderboard(self, score):
        # set up lists to be the updated versions of the current
        current_winners = self.leader_name_list
        current_points = self.leader_point_list
        new_name = self.winners_name.get()
        score = score

        leader_board_entries = []
        # sort name list to be proper
        for item in range(len(current_winners)):
            leader_board_entries.append([current_winners[item], int(current_points[item])])

        # add new entry and sort in order of greater to smallest
        leader_board_entries.append([new_name, int(score)])
        leader_board_entries.sort(key=lambda x: x[1], reverse=True)

        # get the length of list
        length_of_list = len(leader_board_entries)

        # only leave the top 3 scores
        if length_of_list > 3:
            del leader_board_entries[-1]

        # separates the list into the names and points
        names, points = zip(*leader_board_entries)

        # open file
        writing = open("previous_top_scores.txt", "w")
        for count, item in enumerate(names):
            writing.write(item)
            writing.write("\n")
            writing.write(str(points[count]))
            writing.write("\n")

        # close file
        writing.close()

    def back_to_start(self):
        # reshow root (ie choose rounds) and end
        # current game / allow new game to start
        root.deiconify()
        self.end_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Studies Quiz")
    StartGame()
    root.mainloop()
