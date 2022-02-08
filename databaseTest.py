import sqlite3 #import SQLite, the native database in Python
import sqlalchemy as alc #import the SQLalchemy library which makes working
#with SQLite in python easier

class database: #make the class which describes all actions with the database
    def __init__(): #initalizer (called implicitly)
        self.currentFile = "" #string to hold the current file being addressed

    def openFile(fileName): #open a database file, if no file currently exists,
    #create the file

    def closeFile(): #close the current file, this must always be performed
    #before opening another file
