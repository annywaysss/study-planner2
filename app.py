from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(200),nullable=False)
    disc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime)
    def __repr__(self)->str:
        return f"{self.sno}-{self.title}-{self.disc}"
@app.route('/',methods = ['GET','POST'])
def hello_wrld():
    if request.method=='POST':
        title = request.form['title']
        disc = request.form['disc']
        todo = Todo(title=title,disc=disc)
        db.session.add(todo)
        db.session.commit()
    
    # todo = Todo(title="First Todo",disc="Start Django or MongoDB")
    # db.session.add(todo)
    # db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)
@app.route('/show')
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'this is products page'
@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        disc = request.form['disc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.disc=disc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    
    return render_template('update.html', todo=todo)
@app.route('/delete/<int:sno>')
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    if not todo:
        return "Todo item not found", 404
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True, port=8000)