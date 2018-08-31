import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
db.create_all()


@app.route("/")
def index():
    # myapp.db에 있는 모든 레코드를 불러와 보여준다
    # SELECT * FROM posts;
    posts = Post.query.all()
    comments = Comment.query.all()
    #posts는 list인 상태
    
    posts = reversed(posts) #새 게시물을 위로 올리는 법
    return render_template('index.html', posts=posts, comments=comments)

@app.route("/create")
def create():
    title = request.args.get("title")
    content = request.args.get("content")

    post = Post(title=title, content=content)

    db.session.add(post)
    db.session.commit()
    
    #redirect()는 입력후 홈으로 돌아오는 기능
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    # 1. 수정하려는 레코드를 선택
    post = Post.query.get(id)
    # 2. 수정을 하고
    # 3. 커밋을 한다
    return render_template('edit.html', post=post)

@app.route("/delete/<int:id>")
def delete(id):
    # 1. 지우려 하는 레코드를 선택하여
    # post = Post.query.get(int(id))
    post = Post.query.get(id)
    comment = Comment.query.get(id)
    # 2. 지운다.
    db.session.delete(post)
    db.session.delete(comment)
    # 3. 확정하고 DB에 반영한다. Commit
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>")    
def update(id):
    # 1. 불러옴
    post = Post.query.get(id)
    # 2. 수정을 하고
    post.title = request.args.get('title')
    post.content = request.args.get('constent')
    # 3. 커밋한다
    db.session.commit()
    return redirect("/")
    
    
@app.route("/create_comment")
def create_comment():
    # Comment 테이블에 입력받은 내용을 저장한다
    content = request.args.get('comment_content')
    post_id = int(request.args.get('post_id'))
    comment = Comment(content=content, post_id=post_id)

    db.session.add(comment)
    db.session.commit()
    
    return redirect("/")    
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)