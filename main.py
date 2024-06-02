#importing a GUI module
from tkinter import *
# loading a package to read system files and folders
import os
# importing subprocess to run commands
import subprocess
import signal

#creating a window
root = Tk()

#setting the title of the window
root.title("Control Panel")

#setting the size of the window
root.geometry("1000x600")

#setting the background color of the window
mode = "light"
if mode == "light":
    root.configure(bg = "white")
elif mode == "dark":
    root.configure(bg = "black")

# Labels
Label(root, text = "Personal Server Control Panel", font = ("Arial", 24), bg = "white").place(x = 0, y = 00)
Label(root, text = "Server Name", font = ("Arial", 12), bg = "white").place(x = 0, y = 40)
Label(root, text = "Port", font = ("Arial", 12), bg = "white").place(x = 200, y = 40)
Label(root, text = "PID(s)", font = ("Arial", 12), bg = "white").place(x = 250, y = 40)

# a log box for the control panel
log = Text(root, width = 60, height = 35, bg = "white")
log.place(x = 500, y = 0)
log.config(state = DISABLED)

# a function to add text to the log box
def add_log(text, mode = "info"):
    log.config(state = NORMAL)
    log.insert(END,"["+ mode +"] - " + text + "\n")
    log.config(state = DISABLED)


# reading adjacend folders that have a confg and storing them into a list
folders = os.listdir()
for folder in folders:
    if not os.path.exists(folder + "/config"):
        if not os.path.exists(folder + "/config"):
            folders.remove(folder)
            continue

# server_pool example structure
# /config to get config
# /srdout.log to store pipe stdout
# /stderr.log tp store pipe stderr
# {
#     "folder_name": {
#         "Config": {
#             "PORT": 3000,
#             "COMMAND": "node index.js",
#         },
#         "PID": 1234,
#         "process": subprocess.Popen(),
#         "name": Label,
#         "pid_Label": Label,
#         "port_Label": Label,
#         "run_Button": Button,
#         "config_Button": Button
#     }
# }

server_pool = {}

# function to run the server
def toggle_server(folder):
    # getting the command from the config
    command = server_pool[folder]["Config"]["COMMAND"]
    
    # start the subprocess and store the PID
    if server_pool[folder]["PID"] == "":
        # store the logs and err properly, by using append mode
        # run this in background
        server_pool[folder]["process"] = subprocess.Popen(command, cwd=folder , stdout = open(folder + "/stdout.log", "a"), stderr = open(folder + "/stderr.log", "a"))
        server_pool[folder]["PID"] = server_pool[folder]["process"].pid
        # make the button shiw stop
        server_pool[folder]["run_Button"].config(text = "Stop")
        # name background goes green
        server_pool[folder]["name"].config(bg = "green")
        # update the PID
        server_pool[folder]["pid_Label"].config(text = server_pool[folder]["PID"])
        # log the event
        add_log("Server " + folder + " started on PID " + str(server_pool[folder]["PID"]), "info")
    else:
        # gracefully end the task the process in windows
        server_pool[folder]["process"].send_signal(signal.SIGTERM)
        # update the PID
        server_pool[folder]["PID"] = ""
        # update the PID label
        server_pool[folder]["pid_Label"].config(text = "")
        # make the button show start
        server_pool[folder]["run_Button"].config(text = "Start")
        # name background goes white
        server_pool[folder]["name"].config(bg = "white")
        # log the event
        add_log("Server " + folder + " stopped", "info")


# displaying folders
for i in range(len(folders)):
    server_pool[folders[i]] = {}

    name = Label(root, text = folders[i], font = ("Arial", 10), bg = "white")
    server_pool[folders[i]]["name"] = name
    name.place(x = 0, y = 70 + 40 * i)

    # reading the config file
    file = open(folders[i] + "/config", "r")
    lines = file.read().split("\n")
    file.close()

    # example lines : ['PORT=3000', 'TYPE=DEV']
    # storing it into a dictionary
    config = {}
    for line in lines:
        config[line.split("=")[0]] = line.split("=")[1]

    # storing config into server_pool
    server_pool[folders[i]]["Config"] = config

    # storing the PID
    server_pool[folders[i]]["PID"] = ""
    
    # displaying the port
    port_Label = Label(root, text = config["PORT"], font = ("Arial", 10), bg = "white")
    server_pool[folders[i]]["port_Label"] = port_Label
    port_Label.place(x = 200, y = 70 + 40 * i)

    # displaying the PID
    pid_Label = Label(root, text = "", font = ("Arial", 10), bg = "white")
    server_pool[folders[i]]["pid_Label"] = pid_Label
    pid_Label.place(x = 250, y = 70 + 40 * i)

    # button to run the server
    run_Button = Button(root, text = "Start", font = ("Arial", 8), bg = "white")
    server_pool[folders[i]]["run_Button"] = run_Button
    run_Button.place(x = 350, y = 65 + 40 * i)
    run_Button.config(command = lambda folder = folders[i]: toggle_server(folder))

    # button to open config
    config_Button = Button(root, text = "Config", font = ("Arial", 8), bg = "white")
    server_pool[folders[i]]["config_Button"] = config_Button
    config_Button.place(x = 400, y = 65 + 40 * i)

add_log("Control Panel Started", "info")

#running the window
root.mainloop()