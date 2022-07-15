import os
from flask import Flask, render_template, redirect, url_for, request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TheTopSecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://twlepcxonmbsek:5c4820c0e8dd2b3d7a08655924c7124eae84744e7afef4d9269472fa64d3b5ad@ec2-52-205-61-230.compute-1.amazonaws.com:5432/d8eub7a2fanhuo'
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/register', methods=('GET','POST'))
def register():
    if request.method == "POST":
        uname = request.form['uname']
        psw = request.form['psw']
        print(uname, psw)
        admin = User(username=uname, password=psw)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        psw = request.form['psw']
                        
        stmt = select(User.password).where(User.username == uname) 
        result = db.session.execute(stmt)                                   
        og_psw = result.fetchone() 
        new_psw = ""
        for i in og_psw:
            new_psw += i
        if psw == new_psw:
            return render_template('successful.html')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)