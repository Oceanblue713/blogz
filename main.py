from flask import Flask, request, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
import cgi, os, jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Okinawa2016@localhost:8889/build-a-blog'
app.config['SLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Database
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods = ['GET','POST'])
def newpost():
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
    #if (blog_id):
        blog = db.session.query(Blog).filter_by(id = blog_id).first()    
        #title =request.args.get('title')
        #body = request.args.get('body')
        

        return render_template('individual-blog.html', blog=blog)

    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)

        
        

    #id = Blog.query.get(id)
    #return render_template('individual-blog.html', id = id, title = title, body=body, blog=blog)
                
    #blogs = Blog.query.all()
    #return render_template('blogs.html', blogs=blogs)


#@app.route('/blog/<blog_id>' , methods =['GET'])
#def get_blog():
    
    #if request.method == 'GET':
        #get_id = request.args('id')
        #get_title =request.args.get('title').first()
        #get_body = request.args.get('body').first()

    #get_title = Blog.query.get(title).first()
    #get_body = Blog.query.get(body).first()

    #id = Blog.query.get(id)
    #return render_template('individual-blog.html', id = id, get_title = get_title, get_body=get_body)


if __name__ == '__main__':
    app.run()

