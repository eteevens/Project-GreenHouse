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
        self.engine = alc.create_engine('sqlite:///', echo=True)
        #create an empty SQLAlchemy engine, which will later be filled
        #with the database file to be interfaced with, but is temporary
        #connected only with memory, note that this is a relative address

    def openFile(self, file_path):

        self.file = file_path #store the file path for the database
        #based upon what the user has inputted

        if file_path != "": #the current file path must have some value
            if os.path.exists(file_path) != True:
                #if the file does not exist, create it using sqlite3
                sqlite3.connect(file_path)

        self.engine = alc.create_engine("sqlite:///{}".format(file_path))
        #create the SQLAlchemy engine which will allow the
        #database file to be interfaced with

    def __repr__(self): #return the current values of the class, can be used to
    #print information for debugging
        return("<database(file='{}', engine='{}')>".format(self.file,
        self.engine))

class table(self):
    def __init__(self, input_table_name, input_column_data):
        self.metadata = MetaData() #catelog of metadata which defines tables

        self.column = tuple([Column('id', Integer)] + [Column(input_column_data[i](0),
        input_column_data[i](1))) for i in input_column_data]) #

if __name__ == "__main__":
    test = database()
    print(test.__repr__())
    test.openFile('trial.db')
    print(test.__repr__())
    test.createTable('new', (0, Integer))
