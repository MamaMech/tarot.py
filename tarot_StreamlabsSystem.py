# ---------------------------
#   Import Libraries
# ---------------------------
import os
import sys
import json
import codecs
import clr

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))  # point at lib folder for classes / references

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Import your Settings class
# from Settings_Module import MySettings

# ---------------------------
#   [Required] Script Information
# ---------------------------

ScriptName = "Tarot Cards"
Website = "https://www.twitch.tv/mamamech"
Description = "TODO"
Creator = "MamaMech"
Version = "2.0.0"

# ---------------------------
#   [Required] Initialize Data (Only called on load)
# ---------------------------
def Init():
    return

# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
def Execute(data):
    entries = get_entries()
    if data.IsChatMessage() and data.GetParam(0).lower() == "!tarot" and (data.UserName not in entries):
        if Parent.GetPoints(data.User) >= 5000:
            write_entry(data.UserName)
            Parent.RemovePoints(data.User, data.UserName, 5000)
            Parent.SendStreamMessage(data.UserName + ", you have been added to the tarot list for a reading on stream.")
            return
        elif Parent.GetPoints(data.User) < 5000:
            Parent.SendStreamMessage(data.UserName + ", you do not have enough bells.")
        return
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!tarot" and (data.UserName in entries):
            Parent.SendStreamMessage(data.UserName + ", you are already signed up!")
            return

    elif data.IsChatMessage() and data.GetParam(0).lower() == "!tarotlist" and Parent.HasPermission(data.User, "Moderator", ""):
        Parent.SendStreamMessage(", ".join(get_entries()))
        return

    elif data.IsChatMessage() and data.GetParam(0).lower() == "!clearlist" and Parent.HasPermission(data.User, "Moderator", ""):
        clear_entries()
        Parent.SendStreamMessage("The tarot entry list has been cleared!")
        return

# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    return
# tarot entry json

def get_entries():
    try:
        with open('tarot_entries.txt') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            return lines
    except:
        return[]

def write_entry(username):
    entries = get_entries()
    if username not in entries:
        entries.append(username)
        with open('tarot_entries.txt', 'w') as f:
            for item in entries:
                f.write("%s\n" % item)

def clear_entries():
    f = open('tarot_entries.txt', 'w')
    f.truncate(0)


# test code

# class Data:
#     message = ""
#     User = "Sierra"
#     UserName = "Sierra"
#
#     def __init__(self, message):
#         self.message = message
#
#     def IsChatMessage(self):
#         return True
#
#     def GetParam(self, index):
#         try:
#             return self.message.split()[index]
#         except:
#             return ""
#
# class Parent:
#     user_points = 5001
#     user_is_mod = True
#
#     def Log(self, message):
#         return
#
#     def SendStreamMessage(self, message):
#         print(message)
#
#     def GetPoints(self, user):
#         return self.user_points
#
#     def RemovePoints(self, user, user_name, point_cost):
#         self.user_points = 5000 - point_cost
#
#     def HasPermission(self, user, perm, ignore):
#         return self.user_is_mod
#
#
# Init()
# Parent = Parent()
# while True:
#     msg = Data(raw_input())
#     Execute(msg)
