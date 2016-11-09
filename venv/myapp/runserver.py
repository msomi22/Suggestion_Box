import os
from flask import Flask
from flask import render_template, request, flash ,redirect, url_for, session
from forms import SignupForm, LoginForm, SuggestionForm, CommentForm, VoteForm, FlagForm 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
import models
import uuid
import datetime
 
app = Flask(__name__)
app.secret_key = 'peter_mwenda_njeru_1234567890'
bootstrap = Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

lm = LoginManager(app)
lm.login_view = 'login'

@app.route('/')
def index():
    return render_template('index.html') 



@app.route('/home') 
def homepage(): 
    return render_template('home.html', users = models.User.query.all() )


@app.route('/suggestion') 
def getsuggestion(): 
    return render_template('suggestion.html', suggestions = models.Suggestion.query.all() )    
   

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = models.User(str(uuid.uuid4()),form.firstname.data, form.lastname.data,
                    form.email.data, form.username.data, form.password.data,datetime.datetime.now())

        models.db.session.add(user)
        models.db.session.commit()
        flash('Thanks for registering')
        return redirect('/login') 
 
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST': 
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('login', **request.args))
        session['username'] = user.username
        session['uuid'] = user.uuid 
        return redirect(request.args.get('next') or url_for('homepage'))
    return render_template('login.html', form=form)    
	

@app.route('/suggest', methods=['GET', 'POST'])
def suggestion():
    form = SuggestionForm(request.form) 
    if request.method == 'POST' and form.validate():
        suggestion = models.Suggestion(str(uuid.uuid4()),str(session['uuid']),form.title.data,form.suggestion.data,2,'new','new', datetime.datetime.now())
        models.db.session.add(suggestion)
        models.db.session.commit()
        flash('Thanks for posting')
        return redirect('/suggestion') 
        
    return render_template('suggest.html', form=form)     
	

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm(request.form) 
    if request.method == 'POST' and form.validate():
        flash('Thanks for the comment')
        print form.comment.data ,'---', form.base_user.data ,'---',str(session['uuid']) 
        return redirect('/suggestion')

    return redirect('/suggestion') 
	

@app.route('/vote', methods=['GET', 'POST'])
def vove():
	pass 

@app.route('/flag', methods=['GET', 'POST'])
def flag():
	pass 






if __name__== '__main__':
	app.run() 
	
