from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # SQLite database for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for blog posts
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Database initlization
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    posts = BlogPost.query.all()  # Get all blog posts
    return render_template('home.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = 'Anonymous'  # Replace with user authentication logic later
        new_post = BlogPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html')

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
