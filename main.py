from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title("Untitled - PyTextEdit")
root.iconbitmap("Icon.ico")
root.geometry("800x500")
# root.geometry("1200x660")

# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create A Scroll Bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create Text Box
my_text = Text(my_frame, width=97, height=25,
               font=("Consolas", 16),
               undo=True,
               yscrollcommand=text_scroll.set)

my_text.pack()

# Configure Scrollbar
text_scroll.config(command=my_text.yview)

# Create a Menu Bar
my_menu = Menu(root)
root.config(menu=my_menu)

# File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

# Add Status Bar at bottom
status_bar = Label(root, text="Ready    ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)


root.mainloop()
