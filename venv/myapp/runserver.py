import os
from flask import Flask
from flask import render_template, request, flash ,redirect, url_for, session
from forms import SignupForm, LoginForm, SuggestionForm, CommentForm, VoteForm, FlagForm 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from validate_email import validate_email
import models
import uuid
import datetime
 
app = Flask(__name__)
app.secret_key = 'peter_mwenda_njeru_1234567890'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db' 


bootstrap = Bootstrap(app)
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
        
        if not validate_email(form.email.data) and form.validate:
            return render_template('signup.html',form=form, message='The email provided is not valid')    

        if existEmail(form.email.data) and form.validate:
            return render_template('signup.html',form=form, message='The email already exist!')    
        
        if existUsername(form.username.data):
            return render_template('signup.html',form=form, message='The username already exist!')
        
        user = models.User(str(uuid.uuid4()),form.firstname.data, form.lastname.data,
                    form.email.data, form.username.data, form.password.data,datetime.datetime.now())
        models.db.session.add(user)
        models.db.session.commit()
       
        return redirect('/login') 
    return render_template('signup.html', form=form)

def existUsername(username): 
    if models.User.query.filter_by(username=username).first():
        return True
    
def existEmail(email): 
    if models.User.query.filter_by(email=email).first():
        return True

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
    return render_template('login.html', form=form,message='Incorrect user credentials, try again')    
	

@app.route('/suggest', methods=['GET', 'POST'])
def suggestion():
    form = SuggestionForm(request.form) 
    if request.method == 'POST' and form.validate():
        suggestion = models.Suggestion(str(uuid.uuid4()),str(session['uuid']),form.title.data,form.suggestion.data,'new','new', datetime.datetime.now())
        models.db.session.add(suggestion)
        models.db.session.commit()
        return redirect('/suggestion') 
    return render_template('suggest.html', form=form)     
	

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm(request.form) 
    if request.method == 'POST' and form.validate():
        comment = models.Comment(str(uuid.uuid4()),str(form.suggestionid.data),str(session['uuid']),form.comment.data,datetime.datetime.now())
        models.db.session.add(comment)
        models.db.session.commit()
        flash('Your comment was posted successfully')
        return redirect('/comment')
    return redirect('/suggestion') 
	

@app.route('/vote', methods=['GET', 'POST'])
def vove():
    form = VoteForm(request.form) 
    if request.method == 'POST' and form.validate():
        if voted(form.suggestionid.data,str(session['uuid'])):
            flash('You cant vote twice')
        vote = models.Vote(form.suggestionid.data,str(session['uuid']),'up')
        models.db.session.add(vote)
        flash('Thanks, suggestion up-voted')
        models.db.session.commit()
        return redirect('/suggestion')   
	return redirect('/suggestion') 

def voted(suggestionuuid,votinguseruuid):
    if models.Vote.query.filter_by(suggestionuuid=suggestionuuid,votinguseruuid=votinguseruuid).first():
        return True



@app.route('/flag', methods=['GET', 'POST'])
def flag():
    form = FlagForm(request.form)
    if request.method == 'POST' and form.validate(): 
        flag = models.FlagCount(form.suggestionid.data,str(session['uuid'])) 
        models.db.session.add(flag)
        models.db.session.commit()
        return redirect('/suggestion')
	return redirect('/suggestion') 


if __name__== '__main__':
    models.db.create_all()
    app.run(debug=True) 
	
	
