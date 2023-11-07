# Name: Kevin Nguyen
# OSU Email: nguyeke8@oregonstate.edu
# Course: CS361 - Software Engineering 1
# Assignment: Assignment #7
# Due Date: 10/26/2023
# Description: Login Screen for drone interaction

import time
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import json
from functools import partial

# Main Window class variables
# LoginWindow is the primary variable that the user will interface with at the start
# Class Username and Password to be used throughout the code as needed.
loginWindow = tk.Tk()
loginWindow.title('Login Drone')
loginWindow.geometry('1920x1080')
username = tk.StringVar()
password = tk.StringVar()


class LoginPage(ttk.Frame):

    # Function to validate the Username and Password
    def validateUser():

        usercheck = username.get() + ' ' + password.get() + '\n'

        # Sets the default login state to be 0
        logintrue = 0

        # Opens up the text file to search through and verify the Username and Database
        with open('droneusers.txt', 'r') as file1:
            lines = file1.readlines()
            for line in lines:

                if (usercheck == line):
                    logintrue = 1
                    openNewWindow()

            file1.close()

        # If the Username and Password do not exist in the database/text file
        # Tell the user that there is no such person in the database
        if logintrue == 0:
            print("No such User or Password.")

        return

    # Function to incorporate the Username and Password into the Database/text file
    def signupUser():

        signuser = username.get()
        passworduser = password.get()

        # Format used to store the values in the database
        output = '\n' + signuser + ' ' + passworduser
        time.sleep(1)

        # Opens file to append the Username and the Password to the database
        with open('droneusers.txt', 'a') as file1:
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

    # Login button
    login_button = ttk.Button(loginWindow, text="Login", command=validateUser)
    login_button.grid(row=3, column=2, pady=2)

    # Signup button
    signup_button = ttk.Button(loginWindow, text="Sign Up", command=signupUser)
    signup_button.grid(row=4, column=2, pady=2)


def inventoryWindow():

    # Toplevel object which will be treated as a new window during successful login
    newWindow = tk.Toplevel(loginWindow)

    # Title of the Toplevel screen
    newWindow.title("Inventory Menu")

    # Sets the dimensions of toplevel screen
    newWindow.geometry("1980x1080")

    # A Label widget to show in toplevel for the sake of information
    tk.Label(newWindow, text="This is a new window").grid()

    # input field
    input_frame = ttk.Frame(newWindow)

    # title
    title_label = ttk.Label(newWindow, text='Inventory Menu', font='Times 36 bold')
    title_label.grid()

    def closewindow():
        newWindow.destroy()

    # A button which will close the window on a click
    close_button = ttk.Button(newWindow, text="Close Window", command=closewindow)
    close_button.grid(row=3, column=2, pady=2)


# function to open a new window (Main Screen) on a button click
def openNewWindow():

    # Toplevel object which will be treated as a new window during successful login
    newWindow = tk.Toplevel(loginWindow)

    # Title of the Toplevel screen
    newWindow.title("Main Screen Game")

    # Sets the dimensions of toplevel screen
    newWindow.geometry("1980x1080")

    # A Label widget to show in toplevel for the sake of information
    tk.Label(newWindow, text="This is a new window").grid()

    # title
    title_label = ttk.Label(newWindow, text='Main Screen Game', font='Times 36 bold')
    title_label.grid(row=0, column=7, padx=2)

    # input field
    input_frame = ttk.Frame(newWindow)

    # A button which will open a new window (Inventory) on a click
    btn = ttk.Button(newWindow, text="Inventory", command=inventoryWindow)
    btn.grid(row=6, column=1, pady=2)

    # Placeholder for functions when there is a complete Main Screen for navigating the Drone.
    def moveup():
        print("UP")

    def movedown():
        print("DOWN")

    def moveleft():
        print("LEFT")

    def moveright():
        print("RIGHT")

    # Set of Buttons to indicate directional movement (up, down, left and right)
    btnup = ttk.Button(newWindow, text="UP", command=moveup)
    btnup.grid(row=100, column=5, padx=2, pady=2)
    btnup = ttk.Button(newWindow, text="DOWN", command=movedown)
    btnup.grid(row=102, column=5, padx=2, pady=2)
    btnup = ttk.Button(newWindow, text="LEFT", command=moveleft)
    btnup.grid(row=102, column=4, padx=2, pady=2)
    btnup = ttk.Button(newWindow, text="RIGHT", command=moveright)
    btnup.grid(row=102, column=6, padx=2, pady=2)


loginWindow = LoginPage()

if __name__ == "__main__":
    loginWindow.mainloop()
