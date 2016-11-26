from flask import Flask
from flask import render_template, request, flash ,redirect, url_for, session
from myapp.forms import SignupForm, LoginForm, SuggestionForm, CommentForm, VoteForm, FlagForm 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from validate_email import validate_email
from myapp import models 
import uuid
import datetime
from flask_mail import Mail, Message 
 
app = Flask(__name__)
app.secret_key = 'peter_mwenda_njeru_1234567890'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

app.config.update(
      DEBUG=True,
      #For Mail Config
      MAIL_SERVER='smtp.gmail.com',
      MAIL_PORT=465,
      MAIL_USE_SSL=True,
      MAIL_USERNAME = 'mwendapeter72@gmail.com',
      MAIL_PASSWORD = 'peter*#njeru',
	)
mail = Mail(app) 


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db' 

models.db.init_app(app) 
app.app_context().push()

bootstrap = Bootstrap(app)
lm = LoginManager(app)
lm.login_view = 'login'

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/logout')  
def logout():
    session.clear() 
    return render_template('index.html')     

@app.route('/register')
def register():
    return render_template('signup.html')      

@app.route('/home') 
def homepage(): 
    if True:
        if session.get('username') == None:
            return redirect(url_for('logout'))

	suggestions = models.Suggestion.query.all()
	suggestions.reverse()
	return render_template('home.html', suggestions=suggestions ) 


@app.route('/users') 
def usres(): 
    if True:
        if session.get('username') == None:
            return redirect(url_for('logout'))

    return render_template('users.html', users = models.User.query.all() )


@app.route('/suggestion') 
def getsuggestion(): 
    if True:
        if session.get('username') == None:
            return redirect(url_for('logout'))

    return render_template('suggestion.html', suggestions = models.Suggestion.query.all() ) 


@app.route('/suggestion/<suggestid>') 
def getonesuggestion(suggestid):
    if True:
        if session.get('username') == None:
            return redirect(url_for('logout'))
            
    suggestion = models.Suggestion.query.filter_by(uuid=suggestid).first()
    vote = models.Vote.query.filter_by(suggestionuuid=suggestion.uuid).first()
    flag = models.FlagCount.query.filter_by(suggestionuuid=suggestion.uuid).count()
    uvote = models.Vote.query.filter_by(status='Upvote').count()
    dvote = models.Vote.query.filter_by(status='Downvote').count()
    return render_template('suggestion.html', suggestion=suggestion, vote=vote , flag=flag, uvote=uvote , dvote=dvote)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        
        if not validate_email(form.email.data) and form.validate:
        	flash('The email provided is not valid')
        	return redirect(url_for('register'))
            
        if existEmail(form.email.data) and form.validate:
        	flash('The email already exist!')
        	return redirect(url_for('register'))
            
        if existUsername(form.username.data):
        	flash('The username already exist!')
        	return redirect(url_for('register'))
            
        user = models.User(str(uuid.uuid4()),form.firstname.data, form.lastname.data,
                    form.email.data, form.username.data, form.password.data,datetime.datetime.now())
        models.db.session.add(user)
        models.db.session.commit()
        #send mail now
        try:
        	msg = Message('Thanks for registering with Suggestion-Box App', sender='mwendapeter72@gmail.com', recipients=[form.email.data])
        	msg.body = 'Hi ' + form.username.data + ', We are pleased to welcome you to try our amazing App, enjoy.'
        	mail.send(msg)
        	flash('Registration successful, you can login')
        	return redirect(url_for('index'))  
        except Exception as e:
        	flash('Registration successful, you can login')
        	return redirect(url_for('index'))  
        	#return str(e)
        flash('Registration successful, you can login')
        return redirect(url_for('index'))  
     
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
        	flash('Incorrect user credentials, try again')
        	return redirect(url_for('index'))

        session['username'] = user.username
        session['uuid'] = user.uuid 
        return redirect(request.args.get('next') or url_for('homepage'))

@app.route('/suggest', methods=['GET', 'POST'])
def suggestion():
    form = SuggestionForm(request.form) 
    if request.method == 'POST' and form.validate():

        if form.title.data == '':
            flash('Provide a title')
            return redirect(url_for('homepage'))
            
        if len(form.title.data) < 5:
            flash('Title too short!')
            return redirect(url_for('homepage'))
            
        if form.suggestion.data == '' or len(form.suggestion.data) < 5: 
            flash('You must guggest something more that 5 characters long!')
            return redirect(url_for('homepage'))

        else:
            suggestion = models.Suggestion(str(uuid.uuid4()),str(session['uuid']),form.title.data, form.suggestion.data,'new','new', datetime.datetime.now())
            models.db.session.add(suggestion)
            models.db.session.commit()
            flash('Suggestion posted successfully')
            return redirect(url_for('homepage'))
           
	

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm(request.form) 
    if request.method == 'POST' and form.validate():
        if len(str(form.comment.data)) > 2:
            comment = models.Comment(str(uuid.uuid4()),str(form.suggestionid.data),str(session['uuid']),form.comment.data,datetime.datetime.now())
            models.db.session.add(comment)
            models.db.session.commit()
            flash('Your comment was posted successfully')
        else:    
            flash('Write something first')
            return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data))
    return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data)) 
	

@app.route('/vote', methods=['GET', 'POST'])
def vove():
    form = VoteForm(request.form) 
    if request.method == 'POST' and form.validate():
        if voted(form.suggestionid.data,str(session['uuid'])):
            vote = models.Vote(form.suggestionid.data,str(session['uuid']),form.votestatus.data)
            vote = models.Vote.query.filter_by(suggestionuuid=form.suggestionid.data).first()
            vote.status = form.votestatus.data
            models.db.session.commit()
            flash('Thanks, suggestion voted')
            return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data))   
        vote = models.Vote(form.suggestionid.data,str(session['uuid']),form.votestatus.data)
        models.db.session.add(vote)
        models.db.session.commit()
        flash('Thanks, suggestion voted')
        return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data))   
	return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data)) 

def voted(suggestionuuid,votinguseruuid):
    if models.Vote.query.filter_by(suggestionuuid=suggestionuuid,votinguseruuid=votinguseruuid).first():
        return True



@app.route('/flag', methods=['GET', 'POST'])
def flag():
    form = FlagForm(request.form)
    if request.method == 'POST' and form.validate(): 
        if flagged(form.suggestionid.data,str(session['uuid'])):
            flash('You cant flag twice')
            return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data))   
        flag = models.FlagCount(form.suggestionid.data,str(session['uuid'])) 
        models.db.session.add(flag)
        models.db.session.commit()
        flash('Thanks for your concerns regarding this suggestion, we will act accordingly')
        return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data))
	return redirect(url_for('getonesuggestion',suggestid=form.suggestionid.data)) 

def flagged(suggestionuuid,flaginguseruuid):
    if models.FlagCount.query.filter_by(suggestionuuid=suggestionuuid,flaginguseruuid=flaginguseruuid).first():
        return True


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_found(e):
    return render_template('405.html')

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html')        



if __name__== '__main__':
    models.db.create_all()
    app.run(debug=True) 
	
	
