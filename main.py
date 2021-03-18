# TODO - Change Font To Consolas Size 11

from tkinter import *
from tkinter import filedialog
from tkinter import font
from pathlib import Path

root = Tk()
root.title("Untitled - PyTextEdit")
root.iconbitmap("Icon.ico")
root.geometry("800x500")

global name_of_file
name_of_file = False

global selected
selected = ""


# Functions
def new_file():
    my_text.delete("1.0", END)
    root.title("Untitled - PyTextEdit")
    status_bar.config(text="Created New File    ")

    global name_of_file
    name_of_file = False


def open_file():
    my_text.delete("1.0", END)
    file = filedialog.askopenfilename(initialdir=Path.home(),
                                      title="Open File", filetypes=(
            ("Text Files", "*.txt"),
            ("All Files", "*")
        ))

    if file:
        global name_of_file
        name_of_file = file

    file_name = file.split("/")[-1]

    file = open(file, "r")
    content = file.read()
    my_text.insert(END, content)
    file.close()

    root.title(f"{file_name} - PyTextEdit")
    status_bar.config(text=f"Opened File {file_name}    ")


def save_file():
    global name_of_file
    if name_of_file:
        file_name = str(name_of_file).split("/")[-1]
        root.title(f"{file_name} - PyTextEdit")
        status_bar.config(text=f"Saved File {file_name}    ")

        file = open(name_of_file, "w")
        file.write(my_text.get(1.0, END))
        file.close()

    else:
        save_as_file()


def save_as_file():
    file = filedialog.asksaveasfilename(defaultextension="*",
                                        initialdir=Path.home(),
                                        title="Save File",
                                        filetypes=(
                                            ("Text Files", "*.txt"),
                                            ("All Files", "*")
                                        ))

    if file:
        global name_of_file
        name_of_file = file
        file_name = file.split("/")[-1]
        root.title(f"{file_name} - PyTextEdit")
        status_bar.config(text=f"Saved File {file_name}    ")

        file = open(file, "w")
        file.write(my_text.get(1.0, END))
        file.close()


def cut_text(e):
    global selected

    if e:
        selected = root.clipboard_get()

    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)


def copy_text(e):
    global selected

    # Check If We Used Keyboard Shortcuts
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.delete(my_text.selection_get())
            my_text.insert(position, selected)


def text_bold():
    bold_font = font.Font(my_text, my_text.cget('font'))
    bold_font.configure(weight="bold")

    my_text.tag_configure("bold", font=bold_font)

    current_tags = my_text.tag_names("sel.first")

    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")

    else:
        my_text.tag_add("bold", "sel.first", "sel.last ")

def text_italics():
    italics_font = font.Font(my_text, my_text.cget('font'))
    italics_font.configure(slant="italic")

    my_text.tag_configure("italics", font=italics_font)

    current_tags = my_text.tag_names("sel.first")

    if "italics" in current_tags:
        my_text.tag_remove("italics", "sel.first", "sel.last")

    else:
        my_text.tag_add("italics", "sel.first", "sel.last ")



# Create ToolBar Frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Create Main Frame
my_frame = Frame(root)
my_frame.pack()

# Create A Vertical Scroll Bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create A Horizontal Scroll Bar
horizontal_scrollbar = Scrollbar(my_frame, orient=HORIZONTAL)
horizontal_scrollbar.pack(side=BOTTOM, fill=X)

# Create Text Box
my_text = Text(my_frame,
               width=105, height=25,
               font=("Consolas", 16),
               undo=True,
               wrap="none",
               xscrollcommand=horizontal_scrollbar.set,
               yscrollcommand=text_scroll.set)

my_text.pack()

# Configure Scrollbar
text_scroll.config(command=my_text.yview)
horizontal_scrollbar.config(command=my_text.xview)

# Create a Menu Bar
my_menu = Menu(root)
root.config(menu=my_menu)

# File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)

file_menu.add_separator()

file_menu.add_command(label="Exit", command=root.quit)

# Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+X)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+C)")
edit_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="(Ctrl+V)")

edit_menu.add_separator()

edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+Z)")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+Y)")

# Add Status Bar at bottom
status_bar = Label(root, text="Ready    ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# Edit Bindings
root.bind("<Control-x>", cut_text)
root.bind("<Control-c>", copy_text)
root.bind("<Control-v>", paste_text)

# Create ToolBar Buttons
bold_button = Button(toolbar_frame, text="Bold", command=text_bold)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

italics_button = Button(toolbar_frame, text="Italics", command=text_italics)
italics_button.grid(row=0, column=1, padx=5)

undo_button = Button(toolbar_frame, text="Undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)

redo_button = Button(toolbar_frame, text="Redo", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

root.mainloop()
