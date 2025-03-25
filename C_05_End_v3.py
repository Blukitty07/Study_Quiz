from tkinter import *


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


# read and separate

# return separations


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

        self.test_button = Button(self.start_frame, font=("Arial", "12"), text="test", command=open_file)
        self.test_button.grid(row=1)

    def check_rounds(self, mode):
        """
        Checks users have entered 1 or more rounds
        """

        score = 7

        Leaderboard(score)

        # Hide root window
        root.withdraw()


class Leaderboard:
    """
    Interface for playing the study quiz
    """

    def __init__(self, score):
        self.play_box = Toplevel()

        self.end_frame = Frame(self.play_box)
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
            first_score = Label(self.leaderboard_frame, text="You're the first to win!", bg="#ffa6d4", font=body_font)
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
            [self.hints_stats_frame, "Hints", "#c0bdff", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#bdeaff", "", 10, 0, 1],
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

    def check_name(self, score):
        name_entry = self.winners_name.get()

        if len(name_entry) == 3:
            print("all good")

            if name_entry.isalpha():
                print("all good")
                self.error_message.grid(row=2)
                self.error_message.config(text="The leaderboard will now be updated", fg="#25db30")
                self.winner_frame.grid_forget()
                self.update_leaderboard(score)

                # function to add it to the file?

            else:
                print("nahh")
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
        score = 17

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
            print(leader_board_entries)

        # separates the list into the names and points
        names, points = zip(*leader_board_entries)
        print(names)
        print(points)

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
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Studies Quiz")
    StartGame()
    root.mainloop()
