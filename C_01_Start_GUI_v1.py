from tkinter import *
from PIL import Image, ImageTk
from functools import partial


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
        mode_string = ("Choose what mode you'd like to play: \n"
                       "Mode 1 - Study of = This word \n"
                       "Mode 2 - This word = Study of")

        # list of labels to be made(text | font | font colour)
        # currently only one text, but prepared for potential future
        start_game_labels_list = [
            [mode_string, ("Arial", "14"), None]
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
            self.mode_button_frame = Frame(pady=25, padx=10)
            self.mode_button_frame.grid(row=3)

            # make the buttons
            self.first_mode_button = Button(self.mode_button_frame, font=("Arial", "16", "bold"),
                                            bg="#73fffd", text="Mode 1", width=10, height=2, command=self.check_rounds)
            self.first_mode_button.grid(row=0, column=0, padx=5, pady=5)

            self.second_mode_button = Button(self.mode_button_frame, font=("Arial", "16", "bold"), fg="#FFFFFF",
                                             bg="#1d0eab", text="Mode 2", width=10, height=2, command=self.check_rounds)
            self.second_mode_button.grid(row=0, column=1, pady=5, padx=5)

    def check_rounds(self):
        """
        checks that 1 or more rounds have been entered
        """

        # get the amount of rounds
        rounds_wanted = self.amount_of_rounds.get()

        # Reset label and entry box (for when users come back to home screen)
        self.mode_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.amount_of_rounds.config(bg="#FFFFFF")

        # set up strings
        error = "Please enter a whole number more than 0"
        error_check = "Nope"

        # appropriate amount of rounds checker
        try:
            rounds_wanted = int(rounds_wanted)
            # correct amount of rounds
            if rounds_wanted > 0:
                print(error_check)
                self.mode_label.config(text=f"You have chosen to play {rounds_wanted} rounds")
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


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Studies Quiz")
    StartGame()
    root.mainloop()
