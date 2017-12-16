from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi, os, jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Okinawa2016@localhost:8889/blogz'
app.config['SLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'u337kGcys&zP3B'

# Database
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if len(username) == 0 or len(password) == 0:
            return render_template('login.html', login_error='Check blank space')
        #elif username != username:
            #return render_template('login.html', login_error='Invalid username')
        elif user and user.password != password:
            return render_template('login.html', login_error='Invalid password')
        elif user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('login.html', login_error='Invalid Username')

    return render_template('login.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    return render_template('signup.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/newpost', methods = ['GET','POST'])
def newpost():

    owner = User.query.filter_by(username = session['username']).first()
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
    
        title_error = ''
        body_error = ''

        if len(title) <= 0 and len(body) <= 0:
            return render_template('add-blog.html', title_error = "Please fill in the title" ,body_error = "Please fill in the body")
        elif len(title) <= 0:
            return render_template('add-blog.html', title_error = "Please fill in the title")
        elif len(body) <= 0:
            return render_template('add-blog.html', body_error = "Please fill in the body")
        else:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()


            return redirect('/blog?id=' + str(new_blog.id))

    return render_template('add-blog.html')


@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    if request.args:
    
        blog = db.session.query(Blog).filter_by(id = blog_id).first()    
        return render_template('individual-blog.html', blog=blog)

    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)

if __name__ == '__main__':
    app.run()
