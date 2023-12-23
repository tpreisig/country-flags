from tkinter import *
import ttkbootstrap as tbp
import requests


def get_joke():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    response.raise_for_status()
    data = response.json()
    print(data['value'])
    joke = data['value']
    canvas.itemconfig(joke_text, text=joke)

window = tbp.Window(themename="cyborg")
window.title("Chuck Norris Jokes")
window.config(padx=50, pady=50)
canvas = Canvas(window, width=450, height=414)
label = tbp.Label(text="Chuck Norris Jokes", font=("Montserrat", 30, "bold"), bootstyle="primary")
label.pack(pady=0)
joke_text = canvas.create_text(225, 207, text='', width=400, font=("Monserrat", 24, "italic"), fill="#299AD0")
canvas.pack()
button = tbp.Button(window, text="Get Joke", command=get_joke, bootstyle="primary, outline")
button.pack()

window.mainloop()

