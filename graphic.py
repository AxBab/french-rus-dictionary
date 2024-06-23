from tkinter import *

root = Tk()
root['bg'] = "white"
root.title("Французско-русский переводчик")
root.wm_attributes('-alpha', 1)
root.geometry("800x600")
root.resizable(width=False, height=False)

frame = Frame(root, bg='white')
frame.place(relwidth=1, relheight=1)

title = Label(frame, text="Введите слово: ", bg='white', font=100)
title.place(x=0, y=0)

word_input = Entry(frame, bg="white", font=100, border="2")
word_input.place(x=150, y=0)

translate = Button(frame, text="Перевести", bg="green", font=100)
translate.place(x=0, y=100)

translating = Label(frame, bg="white", )
translating.place(x=0, y=0)

root.mainloop()