import uuid
import datetime
from models.posts import Post
from databases.database import Database as db

class Blog(object):
    """Blog object class enables the user to create posts, save posts, return
    posted posts or single post and to search for it by user id.
    """

    def __init__(self, author, title, description, author_id, _id=None):
        self._author = author
        self._author_id = author_id
        self._title  = title
        self._description = description
        self._id = uuid.uuid4().hex if _id == None else _id
        
    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        """new_post(str, str, str) -> return(None)

        title  : The title of the new post
        content: The content regarding the new post
        date   : The date the post was created
        Return : None

        New post method enables the user to create a new blog post.
        """
        new_post = Post(blog_id = self._id,
                        title   = title,
                        content = content,
                        author  = self._author,
                        created_date = date)
        new_post.save() # save post

    def get_posts(self):
        """Return all posts beloging to the user from a specific blog"""
        return Post.get_posts_by_blog_id(self._id)

    def save(self):
        """Save whatever post created by the user to the blog database.
        The post is saved in json format and it includes the author,
        the author id, the title, the description and the post id.
        """
        return db.insert('blogs', self.json())

    def json(self):
        """Returns the information associated with the blog in json format"""

        return {'author' : self._author,
                'author_id':self._author_id,
                'title'  : self._title,
                'description': self._description,
                '_id': self._id }

    @classmethod
    def get_from_db(cls, id):
        """get_from_db(str) -> return(obj)

        id      : blog id
        Returns : object

        Takes a given blog id and returns the data of a single blog.
        The return data is in the form of an object.
        """
        blog_data = db.find_one('blogs', id) # search the blog db and return one blog object based
        return cls(**blog_data)

    @classmethod
    def get_by_author_id(cls, author_id):
        """
        Return a lists of blogs belong to a specific author with the id
        """
        blogs = db.find(collections='blogs', query={'author_id': author_id})
        return [cls(**blog) for blog in blogs ]
