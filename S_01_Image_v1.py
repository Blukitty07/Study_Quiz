from tkinter import *
from PIL import ImageTk, Image

root = Tk()

# Load the image
image = Image.open('school-work-851328_640.jpg')

# Resize the image in the given (width, height)
img = image.resize((320, 223))

# Converse the image in TkImage
my_img = ImageTk.PhotoImage(img)

# Display the image with label
label = Label(root, image=my_img)
label.pack()

label.pack(expand=1, fill=BOTH)


mainloop()
