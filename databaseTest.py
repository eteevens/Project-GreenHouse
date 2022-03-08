import sqlite3 #import SQLite, the native database in Python
import sqlalchemy as alc #import the SQLalchemy library which makes working
#with SQLite in python easier
import os #allows checking to see if a database already exists

class database():
    """
    Make the class which describes all actions with the database
    """
    def __init__(self): #initalizer (called implicitly), self refers to the
    #instance of the class
        self.file = "" #create an empty string to hold the file path for
        #the database
        self.engine = alc.create_engine('sqlite:///')
        #create an empty SQLAlchemy engine, which will later be filled
        #with the database file to be interfaced with, but is temporary
        #connected only with memory, note that this is a relative address

    def openFile(self, filePath):

        self.file = filePath #store the file that

        if filePath != "": #the current file path must have some value
            if os.path.exists(filePath) != True:
                #if the file does not exist, create it using sqlite3
                sqlite3.connect(filePath)

        self.engine = alc.create_engine("sqlite:///{}".format(filePath))
        #create the SQLAlchemy engine which will allow the
        #database file to be interfaced with

    def printFile(self): #prints the current file, for debugging
        print("The current file is: {}".format(self.file))

    def printEngine(self): #prints the current engine instance, for debugging
        print("The current engine is: {}".format(self.engine))

#class table():
"""
make the class which describes the format of a table, note that this is the
generalization which is true across all datatypes
"""


if __name__ == "__main__":
    test = database()
    test.printEngine()
    test.openFile('trial.db')
    test.printEngine()
