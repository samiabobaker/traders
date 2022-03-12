import tkinter as tk
from tkinter import ttk

planets = {
    "system": {
        "symbol": "OE",
        "name": "Omicron Eridani",
        "locations": [
            {
                "symbol": "OE-PM",
                "type": "PLANET",
                "name": "Prime",
                "x": -19,
                "y": 3,
                "allowsConstruction": False,
                "structures": []
            },
            {
                "symbol": "OE-PM-TR",
                "type": "MOON",
                "name": "Tritus",
                "x": -20,
                "y": 5,
                "allowsConstruction": False,
                "structures": []
            },
            {
                "symbol": "OE-CR",
                "type": "PLANET",
                "name": "Carth",
                "x": 4,
                "y": -13,
                "allowsConstruction": False,
                "structures": []
            },
            {
                "symbol": "OE-KO",
                "type": "PLANET",
                "name": "Koria",
                "x": -49,
                "y": 1,
                "allowsConstruction": False,
                "structures": []
            },
            {
                "symbol": "OE-UC",
                "type": "PLANET",
                "name": "Ucarro",
                "x": -17,
                "y": -72,
                "allowsConstruction": False,
                "structures": []
            },
            {
                "symbol": "OE-UC-AD",
                "type": "MOON",
                "name": "Ado",
                "x": -15,
                "y": -73,
                "allowsConstruction": False,
                "structures": []
            },
            {
                "symbol": "OE-UC-OB",
                "type": "MOON",
                "name": "Obo",
                "x": -17,
                "y": -74,
                "allowsConstruction": False,
                "structures": []
            },
            {
                "symbol": "OE-NY",
                "type": "ASTEROID",
                "name": "Nyon",
                "x": 43,
                "y": -46,
                "allowsConstruction": True,
                "structures": [
                    {
                        "id": "ckzlbb9z1138925615s60i5sfagz",
                        "type": "RARE_EARTH_MINE",
                        "location": "OE-NY",
                        "ownedBy": {
                            "username": "01FVQT807GAASBZFZ2D62Y68SE"
                        }
                    }
                ]
            },
            {
                "symbol": "OE-BO",
                "type": "GAS_GIANT",
                "name": "Bo",
                "x": -59,
                "y": 60,
                "allowsConstruction": True,
                "structures": [
                    {
                        "id": "ckzdl3im597518115s6v0cle2ia",
                        "type": "FUEL_REFINERY",
                        "location": "OE-BO",
                        "ownedBy": {
                            "username": "elilamb-nz"
                        }
                    },
                    {
                        "id": "ckzlhlnad91634615s67d4px38q",
                        "type": "RESEARCH_OUTPOST",
                        "location": "OE-BO",
                        "ownedBy": {
                            "username": "01FVQT807GAASBZFZ2D62Y68SE"
                        }
                    }
                ]
            },
            {
                "symbol": "OE-W-XV",
                "type": "WORMHOLE",
                "name": "Wormhole",
                "x": 5,
                "y": -101,
                "allowsConstruction": False,
                "messages": [
                    "Extensive research has revealed a partially functioning warp gate harnessing the power of an unstable but traversable wormhole.",
                    "The scientific community has determined a means of stabilizing the ancient structure.",
                    "Enter at your own risk.",
                    "POST https://api.spacetraders.io/game/structures/:structureId/deposit shipId=:shipId good=:goodSymbol quantity=:quantity",
                    "POST https://api.spacetraders.io/my/warp-jump shipId=:shipId"
                ],
                "structures": [
                    {
                        "id": "cky9igrip3241p5wwwbq6go2r",
                        "type": "WARP_GATE",
                        "location": "OE-W-XV"
                    }
                ]
            }
        ]
    }
}

planets = planets["system"]

planet_tags = []

PLANET_SIZE = 10

is_mouse_pressed = False
just_pressed = False

old_x = 0
old_y = 0

x_diff = 0
y_diff = 0

SCALE = 5

selected_planet = ""

def planet_with_tag(tag):
    planet = list(filter(lambda x: x["tag"] == tag, planet_tags))[0]
    return planet

def set_selected_planet(tag):
    global selected_planet
    tag = canvas.find_withtag("current")[0]
    planet = planet_with_tag(tag)
    selected_planet = planet
    update_planets()

def initialise_planets(planets):

    for planet in planets["locations"]:
        x1, y1, x2, y2 = get_corner_coords(planet["x"]*SCALE, planet["y"]*SCALE)

        tag = {
          "tag":canvas.create_oval(x1, y1, x2, y2, fill="white"),
          "initial_x": planet["x"]*SCALE,
          "initial_y": planet["y"]*SCALE,
          "symbol": planet["symbol"]
        }

        planet_tags.append(tag)

        canvas.tag_bind(tag["tag"], "<Button-1>", set_selected_planet)

  

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


def create_locations_tab(parent, login_token):
    global canvas
    canvas = tk.Canvas(parent, width=500, height=400)
    canvas.grid()

    canvas.create_rectangle(0, 0, 500, 400, fill="black")

    initialise_planets(planets)



    canvas.bind("<Motion>", drag)
    canvas.bind("<ButtonPress-1>", lambda event: set_mouse_pressed(True))
    canvas.bind("<ButtonRelease-1>", lambda event: set_mouse_pressed(False))