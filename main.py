# ------------------------- IMPORTS
import random
from tkinter import *
import pandas
import time
import json

# ------------------------- CONSTANTS
BACKGROUND_COLOR = "#B1DDC6"
LIGHT_BLUE = "#71BBB2"
SEA_GREEN = "#497D74"
SEA_BLUE = "#27445D"
SEASHELL = "#EFE9D5"

# ------------------------- DATA LOAD
# TODO: When the red cross is pressed add that word pair into a json file and save that as wrong_words, save the correct words as correct in the json file
wrong_right_dict = {
    "right": {},
    "wrong": {},
}

current_card = {}


# ------------------------- FUNCTIONS
def load_data():
    global wrong_right_dict
    global current_card
    try:
        with open("word_list.json", "r", encoding='utf-8') as f:
            wrong_right_dict = json.load(f)
    except FileNotFoundError:
        data = pandas.read_json("word_list.csv")
        wrong_right_dict['wrong'] = data.to_dict('records')
        with open("word_list.json", "w", encoding='utf-8') as f:
            json.dump(wrong_right_dict, f, indent=4)
    else:
        print("Word list loaded")
    finally:
        index = random.randint(0, len(wrong_right_dict['wrong'])-1)
        current_card = wrong_right_dict['wrong'].pop(index)

def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(lang_text, text="English")
    canvas.itemconfig(flash_word, text=current_card['english'])

def get_new_card():
    global current_card, flip_timer
    current_card = wrong_right_dict['wrong'][random.randint(0, len(wrong_right_dict['wrong'])-1)]
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(lang_text, text="French")
    canvas.itemconfig(flash_word, text=current_card['french'])
    window.after_cancel(flip_timer)
    flip_timer = window.after(3000, flip_card)

def got_right():
    global wrong_right_dict, current_card, flip_timer
    wrong_right_dict['right'].update(current_card)
    with open("word_list.json", "w", encoding='utf-8') as f:
        json.dump(wrong_right_dict, f, indent=4)
    get_new_card()
    window.after_cancel(flip_timer)
    flip_timer = window.after(3000, flip_card)










# ------------------------- UI SETUP



#   window setup
window = Tk()
window.config(bg=BACKGROUND_COLOR, width=1000, height=700, padx= 50, pady= 50)

load_data()
# print(wrong_right_dict)
# window.geometry("800x600")
window.title('Lang Learner 1000')

flip_timer = window.after(3000, flip_card)
#   canvas
canvas = Canvas(width=800, height=526, highlightthickness=0,bg=BACKGROUND_COLOR)
#  image
card_front_img = PhotoImage(file='images/card_front.png')
card_background = canvas.create_image(400, 263, image=card_front_img)

card_back_img = PhotoImage(file='images/card_back.png')
#   language heading
lang_text = canvas.create_text(400, 150, font=('Arial',30, 'italic'),text='French',fill=SEA_GREEN)
canvas.config(highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

#   flash word
flash_word = canvas.create_text(400,263,text=current_card['french'],font=('Arial',60,'bold'),fill=SEA_BLUE)

#   tick button
tick_img = PhotoImage(file='images/right.png')
tick_btn = Button(image=tick_img, bg=BACKGROUND_COLOR, relief=FLAT, command=got_right)
tick_btn.grid(row=1,column=0)

#   cross button
cross_img = PhotoImage(file='images/wrong.png')
cross_btn = Button(image=cross_img, bg=BACKGROUND_COLOR, relief=FLAT, command=get_new_card)
cross_btn.grid(row=1,column=1)



window.mainloop()
