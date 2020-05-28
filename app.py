from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

"""

__name__ is set to the name of the current
 class, function, method, descriptor, or 
 generator instance.

 Python assigns the name "__main__" 
 to the script when the script is executed.
If the script is imported from another 
script, the script keeps it given name 
(e.g. hello.py). In our case we are 
executing the script. Therefore,
 __name__ will be equal to "__main__".
That means the if conditional statement
is satisfied and the app.

"""

# indicate flask 
app = Flask(__name__)

# add the database, define the url, 
# will use sqlite, /// means relative path, //// means absolute
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize database
db = SQLAlchemy(app)

# create a model 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# define the routes using app.route
# we add methods, it enables this route to get as well as post
@app.route('/', methods = ['POST','GET'])

# define a function for index page
def index():
    if request.method == 'POST':
        # we want to display the actual content from the form
        # we use the id i.e. content and access the user input
        task_content = request.form['content']
        # create an object of database and assign the content
        new_task = Todo(content=task_content)

        try:
            # add the content to database (each entry is an object)
            db.session.add(new_task)
            # commit the chnages
            db.session.commit()
            # reload the page
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        # order all the tasks by date
        tasks = Todo.query.order_by(Todo.date_created).all()
        # return all the task to index.html and show them in the table
        return render_template('index.html', tasks=tasks)
    # we do not need to specify the path,
    #  it knows where to look for it (i.e. in templates folder)
    # return render_template('index.html')


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'error in delete'


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'error in update'
    else:
        return render_template('update.html', task=task)


# main function
if __name__ == '__main__':
    app.run(debug=True)
