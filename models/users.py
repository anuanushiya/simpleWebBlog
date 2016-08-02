from databases.database import Database as db
from flask import session
from models.blog import Blog
import uuid
import datetime

class User(object):

    def __init__(self, email, password, _id=None):
        self._email  = email
        self._passwd = password
        self._id = uuid.uuid4().hex if _id == None else _id

    @classmethod
    def _get_info(cls, key, query):
        """_get_info(str, str) -> return(object)

        key   : The key used to searched the database's index
        query : The query requested
        return: Returns an object

        A helper method that searches the database using a key in order
        to find infomation. If the information is found within the database's
        index it returns an object.        i
        """
        data = db.find_one("users", {key: query}) # returns a dictionary if found
        return cls(**data) if data else None # passes the dictionary in a class object

    @classmethod
    def get_by_email(cls, email):
        """Search the blog by using the author email
        """
        return cls._get_info('email', email)

    @classmethod
    def get_by_id(cls, id):
        """get_by_id(str) -> return(obj)

        id : User id
        returns: A class user object

        Search the database using the user id. If found returns
        a User class object
        """
        return cls._get_info('_id', id)

    @classmethod
    def login_valid(cls, email, password):
        """Returns True if the user login details are valid
        """
        user = cls.get_by_email(email)
        #print(user.password)
        if user:
            return user._passwd == password
        return False

    @staticmethod
    def login(user_email):
        """log the user into their account
        """
        session['email'] = user_email

    @staticmethod
    def logout():
        """log the user out of their account
        """
        session['email'] = None

    @classmethod
    def register(cls, email, password):
        """Register(str, str) -> return(boolean)

        email    : The user email address
        password : The user password
        Register the user details.
        """
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save()
            session['email'] = email
            return True
        return False


    def new_blog(self, title, description):
        """new_blog(str, str) -> return(None)

        title : The title for the new blog
        description: The description for the new blog

        Creates a new blog.
        """
        blog = Blog(author=self.email,
                   title=title,
                   description=description,
                   author_id=self._id)
        blog.save()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        """new_post(str, str, str, str) -> return(None)

        blog_id: The blog id to store the post within
        title  : The title for the new post
        content: The content for the post

        Creates a post for the blog
        """
        blog = Blog.get_from_db(blog_id)
        blog.new_post(title=title,
                      content=content,
                      blog_id=blog_id)

    def get_blogs(self):
        """Returns a list of blogs created by the user.
        """
        return Blog.get_by_author_id(self._id)

    def get_json(self):
        """Represents the users details as a json object.
        """
        return { "email":self._email,
                "_id"   : self._id,
                'password': self._passwd}

    def save(self):
        """
        Saves the user details
        """
        db.insert('users', self.get_json())
