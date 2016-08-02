import pymongo

class Database(object):
    """Uses Mongodb as a means to store data within the database.
    """
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        """
        Connects to a given address, retrieves database
        by name
        """
        client = pymongo.MongoClient(Database.URI) # stores the address inside client
        Database.DATABASE = client['fullstack'] # get the name of db in question(fullstack) and stores inside database.DATABASE

    @staticmethod
    def insert(collections, data):
        """insert(str, str) -> return(none)

        collections: The name of the table(collections) to save to
        data : The data to insert into the database's collection

        Inserts data into a collection(table) for a given database.
        """
        Database.DATABASE[collections].insert(data)

    @staticmethod
    def find(collections, query):
        """find(str, value) -> return(cursor)

        collections: A table name from the database
        query : The data to query from the database
        return: returns a cursor

        Takes a query and queries the database for information.
        """
        return Database.DATABASE[collections].find(query)

    @staticmethod
    def find_one(collections, query):
        """find_one(str, value) -> return(none)

        collections: A table name from the database
        query : The information to query from the database
        return: The next data from the database

        Returs the data from the database.
        """
        return Database.DATABASE[collections].find_one(query)
