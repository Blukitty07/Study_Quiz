from tkinter import *


def open_file():
    file_name = "previous_top_scores.txt"
    statement = "No current scores"
    try:
        with open(file_name, "r") as file:
            result = file.read().split()
            names = result[::2]
            points = result[1::2]

            return names, points

    except FileNotFoundError:
        open(file_name, "w")
        return statement


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

        score = 17

        End(score)

        # Hide root window
        root.withdraw()


class End:
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

        # input name
        # detect points compare to current score. if current score is higher than the lowest score ask for input
        lowest_point = leader_point_list[-1]
        low_point = int(lowest_point)

        # frame for the name entry
        self.winner_frame = Frame(self.end_frame)
        self.winner_frame.grid(row=3)

        # define the lists of names and points to be carried over in functions
        self.leader_name_list = leader_name_list
        self.leader_point_list = leader_point_list

        if score > low_point:
            print("wowie")
            self.winners_name = Entry(self.winner_frame, font=("Arial", "20", "bold"), width=8)
            self.winners_name.grid(row=0, column=0, pady=10)

            self.winner_submit_button = Button(self.winner_frame, text="Submit", font=("Arial", "14", "bold"),
                                               command=lambda: [self.check_name(score)], bg="#ceabdb", width=9)
            self.winner_submit_button.grid(row=0, column=1)

        else:
            print("nahh")

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

        # make sure that only the == 3 is being accepted
        # sort points and names in order
        # clear text file and write everything back on
        # could do all this writing on another function [say write to file]

    def update_leaderboard(self, score):
        # set up lists to be the updated versions of the current
        current_winners = self.leader_name_list
        current_points = self.leader_point_list
        new_name = self.winners_name.get()
        score = 17

        # sort name list to be proper
        current_winners.append(new_name)
        print(current_winners)

        # sort name list to be proper
        current_points.append(score)
        print(current_points)
        current_points_new = [int(x) for x in current_points]
        current_points_new.sort()
        print(current_points_new)
        lowest_number = current_points_new[0]
        print(lowest_number)
        if lowest_number in current_points:
            place = current_points[lowest_number]
            print(place)

        # currently it sorts the list in order of highest to lowest,
        # but need to figure out which name is attached to point

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
