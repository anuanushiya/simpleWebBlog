import datetime
from databases.database import Database as db
import uuid

class Post(object):
    """
    The Post object is responsible for all posts
    """
    def __init__(self, title, content, author, blog_id, _id=None,
                 date=datetime.datetime.utcnow()):
        self._title = title
        self._content = content
        self._author  = author
        self._blog_id = blog_id
        self._id = uuid.uuid4().hex if _id == None else _id
        self._created_date = date

    def save(self):
        """save(void) -> return(None)
        Returns :None
        Store the json representive of the data to mongo
        """
        db.insert('posts', self.json()) # insert json in the post table

    def json(self):
        """json(void) -> return(None)
        Returns a json represative of the data
        """
        return {
            'id':self._id,
            'blog_id':self._blog_id,
            'author':self._author,
            'content':self._content,
            'title':self._title,
            'created_date':self._created_date
           }

    @classmethod
    def get_post_by_id(cls, post_id):
        """get_post_by_id(str) -> return(object)

        id: the post id
        Returns: post data object

        Returns a single post based on the post id.
        """
        post_data = Database.find_one('posts', {'id': post_id})
        return cls(**post_data)

    @classmethod
    def get_posts_by_blog_id(cls, blog_id):
        """get_posts_by_id(str) -> return(obj)

        Returns all posts that belong to a specific blog.
        """
        return [cls(**post) for post in db.find('posts', {'blog_id':blog_id})]
