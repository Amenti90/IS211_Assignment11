__author__ = 'malcolmbarnes'
from flask import Flask, render_template, request, redirect
app= Flask(__name__)


todolist= []
@app.route('/', methods=['GET', 'POST'])
def toDo():

    return render_template ('index.html', todolist= todolist)


def hello_world():
    author= "Malcolm's Page"
    name= "Malcolm"
    return render_template('index.html', author= author, name= name, users= [1,2,3])

@app.route('/submit', methods= ['POST'])
def submit():
    task= request.form['task']
    priority= request.form['priority']
    email= request.form['email']
    print(task,email,priority)
    return redirect ('/')
