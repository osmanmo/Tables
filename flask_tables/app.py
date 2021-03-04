from flask import Flask, render_template, url_for, request, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from IPython.display import HTML
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    NewName = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
        except:
            return redirect(url_for('index'))
        
        #task_content = request.form['content']

        if uploaded_file.filename != '':
            task_content =uploaded_file.filename
            NewName=os.urandom(16).hex()
            uploaded_file.save('files/'+NewName+'.xlsx')
            new_task = Todo(content=task_content, NewName=NewName)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)






@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    NewName=task.NewName+'.xlsx'
    if 'csv' in task.content:
        df=pd.read_csv('files/'+ NewName)

    if 'xls' in task.content:
        df=pd.read_excel('files/'+ NewName)


    
    return df.to_html(classes='table table-striped')


if __name__ == "__main__":
    app.run(debug=True)
