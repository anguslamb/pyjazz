import tkinter as tk
import random

window = tk.Tk()

def choose_note():
    return random.choice(['A','B','C', 'D','E','F','G'])
note = tk.StringVar()
note.set(choose_note())
label =tk.Label(textvariable=note,font=("Arial", 44), width=2, height=2)
label.pack()

def update(*args):
    note.set(choose_note())
    label.update()

window.bind("<space>", update)
window.mainloop()