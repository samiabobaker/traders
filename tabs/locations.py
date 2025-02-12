import tkinter as tk
from tkinter import ttk
import requests



SYSTEMS = "https://api.spacetraders.io/game/systems"

proxy_workaround = {"proxies": {"http": None, "https": None}}
# proxy_workaround = {"proxies": {"https": "http://127.0.0.1:8080"}, "verify": False}

trader_token = None

planet_tags = []

PLANET_SIZE = 10
CANVAS_SIZE = 300

is_mouse_pressed = False
just_pressed = False

old_x = 0
old_y = 0

x_diff = 0
y_diff = 0

SCALE = 5

selected_planet = ""

selected_planet_vars = {}

planets_data = []

systems = []

def planet_with_tag(tag):
    planet = list(filter(lambda x: x["tag"] == tag, planet_tags))[0]
    return planet

def set_selected_planet(tag):
    global selected_planet
    tag = canvas.find_withtag("current")[0]
    planet = planet_with_tag(tag)
    selected_planet = planet
    update_planets()
    update_text(selected_planet)

def update_text(planet):
    properties = ["name", "type", "coords"]
    for p in properties:
        selected_planet_vars[p].set(planet[p])


def initialise_planets(planets):

    for planet in planets["locations"]:
        x1, y1, x2, y2 = get_corner_coords(planet["x"]*SCALE, planet["y"]*SCALE)

        tag = {
          "tag":canvas.create_oval(x1, y1, x2, y2, fill="white"),
          "initial_x": planet["x"]*SCALE,
          "initial_y": planet["y"]*SCALE,
          "symbol": planet["symbol"],
          "type": planet["type"],
          "name": planet["name"],
          "coords": f'{planet["x"]}, {planet["y"]}'
        }

        planet_tags.append(tag)

        canvas.tag_bind(tag["tag"], "<Button-1>", set_selected_planet)
    focus_on(planet_tags[0])

  

def get_center_coords(x1, y1, x2, y2):
    return (x1 + x2) /2 , (y1+y2) / 2
    
def get_corner_coords(x, y):
    x1 = x - PLANET_SIZE + x_diff
    y1 = y - PLANET_SIZE + y_diff
    x2 = x + PLANET_SIZE + x_diff
    y2 = y + PLANET_SIZE + y_diff
    return x1, y1, x2, y2

def update_planets():
    for planet in planet_tags:

        x1, y1, x2, y2 = get_corner_coords(planet["initial_x"], planet["initial_y"])
        
        canvas.coords(planet["tag"], x1, y1, x2, y2)

        if planet == selected_planet:
            canvas.itemconfigure(planet["tag"], fill="orange")
        else:
            canvas.itemconfigure(planet["tag"], fill="white")

    

def set_mouse_pressed(a):
    global is_mouse_pressed
    is_mouse_pressed = a



def drag(event):
    global just_pressed, old_x, old_y, x_diff, y_diff
    if is_mouse_pressed:
        if not just_pressed:
            old_x = event.x
            old_y = event.y
            just_pressed = True
        else:
            x_diff -= old_x - event.x
            y_diff -= old_y - event.y
            old_x = event.x
            old_y = event.y
            
    else:
        just_pressed = False
    update_planets()

#Moves planet to center
def focus_on(planet):
    global x_diff, y_diff
    x_diff = CANVAS_SIZE/2  - planet["initial_x"]
    y_diff = CANVAS_SIZE/2 - planet["initial_y"]
    update_planets()

def refresh_locations_tab():
    global planets_data, systems
    #Update API
    try:
        response = requests.get(SYSTEMS, {"token": trader_token.get()}, **proxy_workaround)
        if response.status_code == 200:
            planets_data = response.json()
            systems = [system["name"] for system in planets_data["systems"]]
            dropdown.set_menu(systems[0], *systems)
            load_system(planets_data, 0)
            
    except ConnectionError as ce:
        print("Failed:", ce)


    
    #Draw to Canvas

def load_system(planets_data, index):
    planets = planets_data["systems"][index]  
    canvas.create_rectangle(0, 0, 500, 400, fill="black")

    initialise_planets(planets)

def change_system(*args):
    global planet_tags
    planet_tags = []
    system = selected_system.get()
    index = systems.index(system)
    load_system(planets_data, index)

    


def create_locations_tab(parent, login_token):

    global canvas, trader_token, dropdown, selected_planet_vars, selected_system
    trader_token = login_token

    #Canvas
    canvas = tk.Canvas(parent, width=CANVAS_SIZE, height=CANVAS_SIZE)
    
    canvas.grid(row = 0, column = 0)

    canvas.bind("<Motion>", drag)
    canvas.bind("<ButtonPress-1>", lambda event: set_mouse_pressed(True))
    canvas.bind("<ButtonRelease-1>", lambda event: set_mouse_pressed(False))

    selected_planet_vars = {
        "name": tk.StringVar(),
        "type": tk.StringVar(),
        "coords": tk.StringVar()
    }

    #Text
    text_frame = ttk.Frame(parent, padding = 5)
    selected_system = tk.StringVar()
    selected_system.trace("w", change_system)
    dropdown = ttk.OptionMenu(text_frame, selected_system, systems, *systems)
    dropdown.grid()
    ttk.Label(text_frame, textvariable=selected_planet_vars["name"]).grid(sticky=tk.EW)
    ttk.Label(text_frame, textvariable=selected_planet_vars["type"]).grid(sticky=tk.EW)
    ttk.Label(text_frame, textvariable=selected_planet_vars["coords"]).grid(sticky=tk.EW)

    text_frame.grid(row=0, column=1)
    text_frame.columnconfigure(0, weight=1)
    parent.columnconfigure(1, weight=1)





