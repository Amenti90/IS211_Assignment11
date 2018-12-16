from flask import Flask, render_template, request, redirect, url_for
import re
import pickle
import os.path

# Initialize empty list for storing tasks as tuples
todolist = list()

# Initialize empty list for storing errors from submit controller
errorlist = list()

# Check if saved list exist (For extra credit 1).
file_Name = "todolist.save"
if os.path.isfile(file_Name):
    fileObject = open(file_Name, 'r')
    todolist = pickle.load(fileObject)  



app = Flask(__name__)

# Home / Index Controller
@app.route('/')
def index():
    global todolist, errorlist

    # Test Data. TODO : Comment before submit. 
    # todolist.append(('Buy Milk', 'foo@bar.com', 'low'))
    # todolist.append(('Buy Cheese', 'foo@bar.com', 'low'))

    print todolist # For debug

    # Handle error messages
    temp_errorlist = errorlist[:] # Create a locol clone and clear errors
    errorlist[:] = [] # Clear errorlist

    return render_template('index.html', todolist = todolist, errorlist = temp_errorlist)

# Submit Controller
@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    global todolist, errorlist
    task = ''
    email = ''
    priority = ''
    errorlist[:] = [] # Clear errorlist

    priority_list = ['low', 'high', 'medium']

    if request.method == 'POST':
        if 'task' in request.form:
            task = request.form['task']
        
        if 'email' in request.form:
            email = request.form['email']

        if 'priority' in request.form:
            priority = request.form['priority']

        if not task:
            errorlist.append('Task is empty')

        if not email:
            errorlist.append('Email is empty')
        else:
            match = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', 
                email
            )
            if match == None:
                errorlist.append('Email is invalid')

        if not priority or priority not in priority_list:
            errorlist.append('Priority is empty')

        if not errorlist:
            todolist.append((task, email, priority))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
            
    else:
        return redirect(url_for('index'))

# Claer List Controller
@app.route('/clear')
def clear():
    global todolist
    todolist[:] = [] # Clear the todo list
    return redirect(url_for('index'))


# Extra Credit 2 : Delete individual item
@app.route('/save')
def save():
    global todolist, file_Name

    # open the file for writing
    fileObject = open(file_Name,'wb') 

    # save
    pickle.dump(todolist, fileObject) 

    # close file
    fileObject.close()

    return redirect(url_for('index'))
    

# Extra Credit 2 : Delete individual item
@app.route('/delete/<id>')
def delete(id = 0):
    global todolist
    try: 
        id = int(id)
        if id >= 0 and id <= len(todolist): # Check index of item to delete exists in list
            todolist.pop(id - 1)
        return redirect(url_for('index'))
    except ValueError:
        return redirect(url_for('index'))

    


if __name__ == '__main__':
    app.run(debug = True)