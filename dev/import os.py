import os


getpath = variables["directoryfolder"]

if not os.path.exists(getpath):
    os.makedirs(getpath)
