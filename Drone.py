# Name: Kevin Nguyen
# OSU Email: nguyeke8@oregonstate.edu
# Course: CS361 - Software Engineering 1
# Assignment: Project
# Due Date: 12/11/2023
# Description: Interactive Screens as a Concept for a "Game"

import time
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import json, requests
import datetime

loginWindow = tk.Tk()
loginWindow.title('Login Drone')
loginWindow.geometry('1920x1080')
username = tk.StringVar()
password = tk.StringVar()

description, main = "", ""
temperature, pressure = 0, 0

zipcode = tk.StringVar()

size = 10
grid = [[0 for i in range(size)] for i in range(size)]
ROWS = 5
COLUMNS = 5
inventorygrid = [[None for i in range(COLUMNS)] for i in range(ROWS)]

rowcount = 0
colcount = 0

rockcount = 0
kelpcount = 0


class LoginPage(ttk.Frame):

    # Function to validate the Username and Password
    def validateUser():

        usercheck = username.get() + ',' + password.get()

        # Opens file to append the Username and the Password to the database
        with open('passed_creds.txt', 'a') as file1:
            file1.write(usercheck)
            file1.close()

        # Sets the default login state to be 0
        time.sleep(4)
        with open('pass_status.txt', 'r') as file:
            logintrue = file.readlines()

            if (logintrue[0] == 'True'):
                openNewWindow()

            else:
                print("No such User or Password.")

        file.close()
        return

    # Function to incorporate the Username and Password into the Database/text file
    def signupUser():

        signuser = username.get()
        passworduser = password.get()

        # Format used to store the values in the database
        output = '\n' + signuser + ',' + passworduser
        time.sleep(1)

        # Opens file to append the Username and the Password to the database
        with open('cred_db.txt', 'a') as file1:
            file1.write(output)
            file1.close()

        return

    # input field
    input_frame = ttk.Frame(master=loginWindow)

    # Username label and text entry box
    username_label = ttk.Label(loginWindow, text="User Name", font='Times 36 bold')
    username_label.grid(row=3, column=0, pady=2)
    username_entry = ttk.Entry(loginWindow, textvariable=username)
    username_entry.grid(row=3, column=1, pady=2)

    # Password label and password entry box
    password_label = ttk.Label(loginWindow, text="Password", font='Times 36 bold')
    password_label.grid(row=4, column=0, pady=2)
    password_entry = ttk.Entry(loginWindow, textvariable=password, show='*')
    password_entry.grid(row=4, column=1, pady=2)

    # Login button for the main page
    login_button = ttk.Button(loginWindow, text="Login", command=validateUser)
    login_button.grid(row=3, column=2, pady=2)

    # Signup button for the main page
    signup_button = ttk.Button(loginWindow, text="Sign Up", command=signupUser)
    signup_button.grid(row=4, column=2, pady=2)

# Class that holds the items that will be a part of the inventory screen
class ItemWorld:
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

# The Grid that the "Drone" will move on based on user interactions
class WorldMap:

    def __init__(self, master, rows, cols, cell_size):

        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.canvas = tk.Canvas(master, width=cols * cell_size, height=rows * cell_size, borderwidth=0,
                                highlightthickness=0)

        self.canvas.grid(row=15, column=20)

        # Initialize the grid
        self.grid = [[0] * cols for _ in range(rows)]

        # Create the character
        self.character = self.canvas.create_rectangle(0, 0, cell_size, cell_size, fill="blue")

        # Create the items and place them on the grid
        self.kelp1 = self.canvas.create_rectangle(0, 0, cell_size, cell_size, fill="green")
        self.canvas.move(self.kelp1, 3 * self.cell_size, 3 * self.cell_size)
        self.kelp2 = self.canvas.create_rectangle(0, 0, cell_size, cell_size, fill="green")
        self.canvas.move(self.kelp2, 1 * self.cell_size, 2 * self.cell_size)
        self.rock1 = self.canvas.create_rectangle(0, 0, cell_size, cell_size, fill="grey")
        self.canvas.move(self.rock1, 1 * self.cell_size, 4 * self.cell_size)
        self.rock2 = self.canvas.create_rectangle(0, 0, cell_size, cell_size, fill="grey")
        self.canvas.move(self.rock2, 2 * self.cell_size, 0 * self.cell_size)

        # Bind arrow key events
        master.bind("<Up>", self.move_up)
        master.bind("<Down>", self.move_down)
        master.bind("<Left>", self.move_left)
        master.bind("<Right>", self.move_right)

        self.draw_grid()


    def draw_grid(self):

        for row in range(self.rows):

            for col in range(self.cols):

                # Grid is made
                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.grid[row][col] = self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")


    def move_character(self, dx, dy):

        global colcount, rowcount, kelpcount, rockcount
        colcount += dy
        rowcount += dx
        self.canvas.move(self.character, dx * self.cell_size, dy * self.cell_size)

        if (((rowcount == 3 and colcount == 3) or (rowcount == 1 and colcount == 2)) and kelpcount < 2):
            kelpcount += 1

        if (((rowcount == 1 and colcount == 4) or (rowcount == 2 and colcount == 0)) and rockcount < 2):
            rockcount += 1

    def move_up(self, event):
        if colcount > 0:
            self.move_character(0, -1)

    def move_down(self, event):
        if colcount < self.cols-1:
            self.move_character(0, 1)

    def move_left(self, event):
        if rowcount > 0:
            self.move_character(-1, 0)

    def move_right(self, event):
        if rowcount < self.rows-1:
            self.move_character(1, 0)

# Window to display the Weather based on the user's zipcode input
def weatherWindow():

    # Toplevel object which will be treated as a new window during successful login
    newWindow = tk.Toplevel(loginWindow)

    # Title of the Toplevel screen
    newWindow.title("Weather Menu")

    # Sets the dimensions of toplevel screen
    newWindow.geometry("1280x720")

    title_label = ttk.Label(newWindow, text='Weather Screen', font='Times 36 bold')
    title_label.grid(row=0, column=7, padx=2)

    # Zipcode label and text entry box
    zipcode_label = ttk.Label(newWindow, text="Enter a US Zipcode", font='Times 14 bold')
    zipcode_label.grid(row=3, column=7, pady=2)
    zipcode_entry = ttk.Entry(newWindow, textvariable=zipcode)
    zipcode_entry.focus_set()
    zipcode_entry.grid(row=4, column=7, pady=2)


    # Grabs weather data from Rest Weather API to display to the user
    def zipcodeUser():

        userzip = zipcode.get()
        url = f"http://127.0.0.1:5000/weather?zipcode={userzip}"
        response = requests.get(url)
        data = response.json()

        # If the Zipcode is invalid, displays a text to notify the user
        if (response.status_code == 404):

            zipcode_error = "Incorrect Zipcode entered. Please try again."
            text = ttk.Text(newWindow, height=10, width=50, font='Times 24 bold')
            text.grid(row=20, column=9, padx=20, pady=40)
            text.insert(ttk.END, zipcode_error)


        # Print out the weather values from the URL from the Weather API site
        else:

            main = data["main"]
            description = data["description"]
            temperature = data["temperature"]
            pressure = data["pressure"]

            weather_description = "Main: " + main + "\nDescription: " + description + "\nCurrent Temperature: " + str(
                temperature) + " Farenheit" + "\nAtmospheric Pressure: " + str(
                pressure) + " hPa" + "\nTime of Report: " + str(datetime.datetime.now())

            text = ttk.Text(newWindow, height=10, width=50, font='Times 24 bold')
            text.grid(row=20, column=9, padx=20, pady=40)
            text.insert(ttk.END, weather_description)

    # A Submit button for the user to enter in a Zipcode
    submit_button = ttk.Button(newWindow, text="Submit", command=zipcodeUser)
    submit_button.grid(row=4, column=8, pady=2)

# Displays the inventory window where it displays the Drone's collection of items currently in storage
def inventoryWindow():

    # Toplevel object which will be treated as a new window during successful login
    newWindow = tk.Toplevel(loginWindow)

    # Title of the Toplevel screen
    newWindow.title("Inventory Menu")

    # Sets the dimensions of toplevel screen
    newWindow.geometry("1980x1080")

    # title
    title_label = ttk.Label(newWindow, text='Inventory Menu', font='Times 36 bold')
    title_label.grid(row=0, column=0, padx=0, pady=10)

    rock = ItemWorld("Stone", "A piece of stone dredged up from the bottom of the sea, contains extract of Carbon", 10)
    kelp = ItemWorld("Kelp", "This piece of kelp has traces of chemicals found on the deep bottom seafloor", 1)

    global rockcount, kelpcount

    # Creates a series of text boxes in a table format to display information to the user.
    titlename = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    titlename.grid(row=10, column=1, padx=0, pady=0)
    titlename.insert(ttk.END, "Item")
    titledescription = ttk.Text(newWindow, height=3, width=50, font='Times 16 bold')
    titledescription.grid(row=10, column=2, padx=0, pady=0)
    titledescription.insert(ttk.END, "Description")
    textweight = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textweight.grid(row=10, column=3, padx=0, pady=0)
    textweight.insert(ttk.END, "Weight")
    textamount = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textamount.grid(row=10, column=4, padx=0, pady=0)
    textamount.insert(ttk.END, "Amount")


    textrockname = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textrockname.grid(row=11, column=1, padx=0, pady=0)
    textrockname.insert(ttk.END, rock.name)
    textrockdescription = ttk.Text(newWindow, height=3, width=50, font='Times 16 bold')
    textrockdescription.grid(row=11, column=2, padx=0, pady=0)
    textrockdescription.insert(ttk.END, rock.description)
    textrockweight = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textrockweight.grid(row=11, column=3, padx=0, pady=0)
    textrockweight.insert(ttk.END, rock.weight)
    textrockamount = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textrockamount.grid(row=11, column=4, padx=0, pady=0)
    textrockamount.insert(ttk.END, rockcount)

    textkelpname = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textkelpname.grid(row=12, column=1, padx=0, pady=0)
    textkelpname.insert(ttk.END, kelp.name)
    textkelpdescription = ttk.Text(newWindow, height=3, width=50, font='Times 16 bold')
    textkelpdescription.grid(row=12, column=2, padx=0, pady=0)
    textkelpdescription.insert(ttk.END, kelp.description)
    textkelpweight = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textkelpweight.grid(row=12, column=3, padx=0, pady=0)
    textkelpweight.insert(ttk.END, kelp.weight)
    textkelpamount = ttk.Text(newWindow, height=3, width=10, font='Times 16 bold')
    textkelpamount.grid(row=12, column=4, padx=0, pady=0)
    textkelpamount.insert(ttk.END, kelpcount)

    def closewindow():
        newWindow.destroy()

    # A button which will close the window on a click
    close_button = ttk.Button(newWindow, text="Close Window", command=closewindow)
    close_button.grid(row=0, column=8)

    # Resets the item count and "refreshes" the window by closing it, then opening it up again.
    def discardallitems():
        global rockcount, kelpcount
        rockcount, kelpcount = 0, 0
        newWindow.after(2, closewindow())
        newWindow.after(2, inventoryWindow())

    # A button which will drop all items in the inventory
    drop_items = ttk.Button(newWindow, text="Empty Inventory", command=discardallitems)
    drop_items.grid(row=0, column=9, padx=5)

def diagnostic_check():

    # Toplevel object which will be treated as a new window during successful login
    newWindow = tk.Toplevel(loginWindow)

    # Title of the Toplevel screen
    newWindow.title("Health Menu")

    # Sets the dimensions of toplevel screen
    newWindow.geometry("300x300")
    health = 170
    max_health = 200

    # Displays a health bar to show the user what the current condition of the Drone is
    healthbar = ttk.Progressbar(newWindow, orient="horizontal", length=200, mode="determinate")
    healthbar["maximum"] = max_health
    healthbar["value"] = health
    healthbar.grid(row=1, column=5, padx=5, pady=5)

# function to open a new window (Main Screen) on a button click
def openNewWindow():

    # Toplevel object which will be treated as a new window during successful login
    newWindow = tk.Toplevel(loginWindow)

    # Title of the Toplevel screen
    newWindow.title("Main Screen Game")

    # Sets the dimensions of toplevel screen
    newWindow.geometry("1980x1080")

    # title
    title_label = ttk.Label(newWindow, text='Main Screen Game', font='Times 36 bold')
    title_label.grid(row=0, column=2, padx=2)

    # A button which will open a new window (Inventory) on a click
    inventorybtn = ttk.Button(newWindow, text="Inventory", command=inventoryWindow)
    inventorybtn.grid(row=1, column=1, pady=2)

    # A button which will open a new window (Weather Screen) on a click
    weatherbtn = ttk.Button(newWindow, text="Get Weather", command=weatherWindow)
    weatherbtn.grid(row=2, column=1, pady=2)

    # Creates the grid where the user can see the "Drone" in operation
    app = WorldMap(newWindow, rows=5, cols=5, cell_size=80)

    instructions = "Use the Arrow Keys on the Keyboard to navigate the Blue Drone Square on the Grid. Move the drone over" \
                   "to a colored Square to pick up the Object into your Inventory."
    text = ttk.Text(newWindow, height=10, width=50, font='Times 16 bold')
    text.grid(row=15, column=2, padx=2, pady=2)
    text.insert(ttk.END, instructions)

    # Image sets to toggle between for the tool sets for the Drone
    image1 = tk.PhotoImage(
        file=r"C:\Users\KQNgu\Documents\ComputerScienceOSU\CS361 - Software Engineering 1\Project\drillicon.png")
    image2 = tk.PhotoImage(
        file=r"C:\Users\KQNgu\Documents\ComputerScienceOSU\CS361 - Software Engineering 1\Project\cutter.png")

    toolcanvas = tk.Canvas(newWindow, width=250, height=250, borderwidth=1, highlightthickness=1)
    toolcanvas.grid(row=35, column=2, padx=2, pady=2)
    toolimage = toolcanvas.create_image(200, 200, image=image1)

    # Image sets to toggle between to indicate whether the weapon is primed or not for the Drone
    weaponimage1 = tk.PhotoImage(
        file=r"C:\Users\KQNgu\Documents\ComputerScienceOSU\CS361 - Software Engineering 1\Project\torpedo.png")
    weaponimage2 = tk.PhotoImage(
        file=r"C:\Users\KQNgu\Documents\ComputerScienceOSU\CS361 - Software Engineering 1\Project\torpedoarmed.png")

    weaponcanvas = tk.Canvas(newWindow, width=250, height=250, borderwidth=1, highlightthickness=1)
    weaponcanvas.grid(row=35, column=6, padx=2, pady=2)
    weaponicon = weaponcanvas.create_image(200, 200, image=weaponimage1)

    # Closes out the window for the drone interface and removes all the storage items
    def self_destruct():

        global colcount, rowcount, kelpcount, rockcount
        colcount, rowcount, kelpcount, rockcount = 0, 0, 0, 0
        newWindow.after(3, newWindow.destroy())

    # Checks to see if the user would like to close out on the current session with the Drone
    def destruct_check():
        # Toplevel object which will be treated as a new window during successful login
        newWindow = tk.Toplevel(loginWindow)

        # Title of the Toplevel screen
        newWindow.title("Self-Destruct Check")

        # Sets the dimensions of toplevel screen
        newWindow.geometry("800x800")

        # title
        title_label = ttk.Label(newWindow, text='SELF-DESTRUCT', font='Times 36 bold')
        title_label.grid(row=0, column=5, padx=0, pady=10)

        destructmessage = "Are you sure you want to self-destruct the Drone and lose all items?"
        text = ttk.Text(newWindow, height=10, width=20, font='Times 24 bold')
        text.grid(row=1, column=5, padx=10, pady=10)
        text.insert(ttk.END, destructmessage)

        def closewindow():
            newWindow.destroy()

        # A button which will open a new window (Weather Screen) on a click
        btn = ttk.Button(newWindow, text="YES", command=self_destruct)
        btn.grid(row=1, column=6, pady=2)

        # A button which will open a new window (Weather Screen) on a click
        btn = ttk.Button(newWindow, text="NO", command=closewindow)
        btn.grid(row=1, column=7, pady=2)

    # Toggles between the icons to indicate to the user what item is in use
    def toolswap():
        currentool = toolcanvas.itemcget(toolimage, "image")
        if currentool == str(image1):
            toolcanvas.itemconfig(toolimage, image=image2)
        else:
            toolcanvas.itemconfig(toolimage, image=image1)

    # Toggles between an on/off state for weapon priming
    def weapontoggle():
        currentstate = weaponcanvas.itemcget(weaponicon, "image")
        if currentstate == str(weaponimage1):
            weaponcanvas.itemconfig(weaponicon, image=weaponimage2)
        else:
            weaponcanvas.itemconfig(weaponicon, image=weaponimage1)

    # A button which will open a Self-Destruct screen on a click
    destructbtn = ttk.Button(newWindow, text="SELF-DESTRUCT", command=destruct_check)
    destructbtn.grid(row=25, column=25, pady=2)

    # A button for a health diagnostic check for the Drone
    healthbtn = ttk.Button(newWindow, text="HEALTH", command=diagnostic_check)
    healthbtn.grid(row=25, column=30, pady=2)

    # A Toggle Image for the tool the drone is currently using
    toolbtn = ttk.Button(newWindow, text="TOGGLE TOOL", command=toolswap)
    toolbtn.grid(row=36, column=2, pady=2)

    # A Toggle Image to indicate wether the weapon is primed or not
    weaponbtn = ttk.Button(newWindow, text="TOGGLE ARMED", command=weapontoggle)
    weaponbtn.grid(row=36, column=6, pady=2)


loginWindow = LoginPage()

if __name__ == "__main__":
    loginWindow.mainloop()
