from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from pathlib import Path
import win32print
import win32api

black = "#000000"
grey = "#373737"
white = "#ffffff"
default_color = "SystemButtonFace"

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


def print_file():
    try:
        printer = win32print.GetDefaultPrinter()
        status_bar.config(text=f"Default Printer - {printer}")

        file = filedialog.askopenfilename(initialdir=Path.home(),
                                          title="Open File", filetypes=(
                ("Text Files", "*.txt"),
                ("All Files", "*")
            ))

        if file:
            win32api.ShellExecute(0, "print", file, None, ".", 0)

        status_bar.config(text=f"Printed File {file}")
    except:
        print("An Error Occurred")


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
            try:
                my_text.delete(my_text.selection_get())
            except:
                pass
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


def change_selected_text_color():
    my_color = colorchooser.askcolor()[-1]

    if my_color:
        color_font = font.Font(my_text, my_text.cget('font'))
        my_text.tag_configure("colored", font=color_font, foreground=my_color)
        current_tags = my_text.tag_names("sel.first")

        if "colored" in current_tags:
            my_text.tag_remove("colored", "sel.first", "sel.last")
        else:
            my_text.tag_add("colored", "sel.first", "sel.last ")

        status_bar.config(text=f"Changed Selected Text Color To {my_color}")


def change_bg_color():
    my_color = colorchooser.askcolor()[-1]

    if my_color:
        my_text.config(bg=my_color)

        status_bar.config(text=f"Changed Background Color to {my_color}")


def change_all_text_color():
    my_color = colorchooser.askcolor()[-1]

    if my_color:
        my_text.config(fg=my_color)

        status_bar.config(text=f"Changed Text Color to {my_color}")


def select_all_text(e):
    my_text.tag_add('sel', '1.0', END)


def clear_all_text():
    my_text.delete(1.0, END)


def dark_mode_on():
    root.config(bg=black)
    status_bar.config(bg=black, fg=white)
    my_text.config(bg=black, fg=white)
    toolbar_frame.config(bg=black)

    bold_button.config(bg=black, fg=white)
    italics_button.config(bg=black, fg=white)
    color_text_button.config(bg=black, fg=white)
    undo_button.config(bg=black, fg=white)
    redo_button.config(bg=black, fg=white)
    select_all_text_button.config(bg=black, fg=white)
    clear_all_text_button.config(bg=black, fg=white)

    file_menu.config(bg=black, fg=white)
    edit_menu.config(bg=black, fg=white)
    color_menu.config(bg=black, fg=white)
    options_menu.config(bg=black, fg=white)


def dark_mode_off():
    root.config(bg=default_color)
    status_bar.config(bg=default_color, fg=black)
    my_text.config(bg=white, fg=black)
    toolbar_frame.config(bg=default_color)

    bold_button.config(bg=default_color, fg=black)
    italics_button.config(bg=default_color, fg=black)
    color_text_button.config(bg=default_color, fg=black)
    undo_button.config(bg=default_color, fg=black)
    redo_button.config(bg=default_color, fg=black)
    select_all_text_button.config(bg=default_color, fg=black)
    clear_all_text_button.config(bg=default_color, fg=black)

    file_menu.config(bg=default_color, fg=black)
    edit_menu.config(bg=default_color, fg=black)
    color_menu.config(bg=default_color, fg=black)
    options_menu.config(bg=default_color, fg=black)


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
               width=170, height=31.49,
               font=("Consolas", 11),
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

file_menu.add_command(label="Print File", command=print_file)

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

edit_menu.add_separator()

edit_menu.add_command(label="Select All", command=lambda: select_all_text(False), accelerator="(Ctrl+A)")
edit_menu.add_command(label="Clear", command=clear_all_text)

# Color Menu
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Color", menu=color_menu)

color_menu.add_command(label="Selected Text", command=change_selected_text_color)
color_menu.add_command(label="Background", command=change_bg_color)
color_menu.add_command(label="All Text ", command=change_all_text_color)

# Options Menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)

options_menu.add_command(label="Dark Mode On", command=dark_mode_on)
options_menu.add_command(label="Dark Mode Off", command=dark_mode_off)

# Add Status Bar at bottom
status_bar = Label(root, text="Ready    ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# Edit Bindings
root.bind("<Control-x>", cut_text)
root.bind("<Control-c>", copy_text)
root.bind("<Control-v>", paste_text)
root.bind("<Control-a>", select_all_text)

# Create ToolBar Buttons
bold_button = Button(toolbar_frame, text="Bold", command=text_bold)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

italics_button = Button(toolbar_frame, text="Italics", command=text_italics)
italics_button.grid(row=0, column=1, padx=5)

undo_button = Button(toolbar_frame, text="Undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)

redo_button = Button(toolbar_frame, text="Redo", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

color_text_button = Button(toolbar_frame, text="Text Color", command=change_selected_text_color)
color_text_button.grid(row=0, column=4, padx=5)

select_all_text_button = Button(toolbar_frame, text="Select All", command=lambda: select_all_text(False))
select_all_text_button.grid(row=0, column=5, padx=5)

clear_all_text_button = Button(toolbar_frame, text="Clear", command=clear_all_text)
clear_all_text_button.grid(row=0, column=6, padx=5)

root.mainloop()
