from databases.database import Database as db
from flask import Flask, render_template, url_for, request, session, make_response, redirect
from models.users import User, Blog

app = Flask(__name__)

@app.before_first_request
def initialize():
    db.initialize()

def login():
    return render_template('/login/login.html')

@app.route('/auth/login', methods=['GET','POST'])
def user_login():

    if request.method == 'GET':
        #return render_template('/login/login.html')
        return login()
    else:
        email  = request.form['email']
        passwd = request.form['password']
        if User.login_valid(email, passwd):
            User.login(email)
            return render_template('/user_page/user_profile_page.html', email=session['email'])
        else:
            session['email'] = None
            return login()


@app.route('/auth/register', methods=['GET', 'POST'])
def register_user():

    if request.method == 'GET':
        return render_template('/register/register.html')
    else:
        email  = request.form['email']
        passwd = request.form['password']

        if User.get_by_email(email):
            return 'user already exists'
        else:
            User.register(email, passwd)

    return render_template('/user_page/user_profile_page.html', email=session['email'])



@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def get_all_user_blogs(user_id=None):

    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template('/user_page/user_blogs.html', blogs=blogs, email=user._email)

@app.route("/posts/<string:blog_id>")
def get_all_user_posts(blog_id):
    """
    """
    blog  = Blog.get_from_db(blog_id)
    posts = blog.get_posts()

    return render_template('/user_page/user_posts.html',
                            posts=posts,
                            blog_title=blog._title,
                            blog_id=blog_id)


@app.route('/blog/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('/user_page/new_blog.html')
    else:
        title = request.form['title']
        descr = request.form['description']
        user  = User.get_by_email(session['email'])

        new_blog = Blog(user._email, title, descr, user._id)
        new_blog.save()

        return make_response(get_all_user_blogs(user._id))


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('/user_page/new_post.html', blog_id=blog_id)
    else:
        title   = request.form['title']
        content = request.form['description']
        user    = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user._email)
        new_post.save()

        return make_response(get_all_user_posts(blog_id))

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'some secret key'
    app.run(host='0.0.0.0',port=5000)
