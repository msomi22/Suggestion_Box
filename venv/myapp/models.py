from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text , DateTime , SmallInteger,and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from runserver import app

db = SQLAlchemy(app)  



""" 
"""
class User(db.Model):

	def __init__(self,uuid,firstname,lastname,email,username,password,dateadded):
		self.uuid = uuid
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.username = username
		self.password = generate_password_hash(password)
		self.dateadded = dateadded
		


	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	uuid = db.Column(db.Text, unique=True, index=True)
	firstname = db.Column(db.String(100), nullable=True)
	lastname = db.Column(db.String(100), nullable=True)
	email = db.Column(db.String(200), nullable=True)
	username = db.Column(db.String(100), nullable=True)
	password = db.Column(db.String(100), nullable=True)
	dateadded = db.Column(db.DateTime(200), nullable=True)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password, password)

	def __repr__(self):
		return '<User %r>' % self.uuid



"""
"""	
class Suggestion(db.Model):

	def __init__(self,uuid,useruuid,title,suggestion,flagStatus,status,datePosted):
		self.uuid = uuid
		self.useruuid = useruuid
		self.title = title
		self.suggestion = suggestion
		self.flagStatus = flagStatus
		self.status = status
		self.datePosted = datePosted


	__tablename__ = 'suggestion'
	id = db.Column(db.Integer, primary_key=True)
	uuid = db.Column(db.Text, unique=True, index=True)
	useruuid = Column(db.Text, ForeignKey('user.uuid'), nullable=False)
	title = db.Column(db.Text, nullable=True)
	suggestion = db.Column(db.Text, nullable=True)
	flagStatus = db.Column(db.String(100), nullable=True)
	status = db.Column(db.String(100), nullable=True)
	datePosted = db.Column(db.DateTime(200), nullable=True)
	user = db.relationship('User', backref=db.backref('suggestions', lazy='dynamic')) 



	def __repr__(self):
		return '<Suggestion %r>' % self.uuid


"""
"""	
class FlagCount(db.Model):
	def __init__(self,suggestionuuid,flaginguseruuid):
		self.suggestionuuid = suggestionuuid
		self.flaginguseruuid = flaginguseruuid

	__tablename__ = 'flagcount'
	id = db.Column(db.Integer, primary_key=True)
	suggestionuuid = Column(db.Text, ForeignKey('suggestion.uuid'), nullable=False)
	flaginguseruuid = Column(db.Text, ForeignKey('user.uuid'), nullable=False) 
	
	def __repr__(self):
		return '<flagCount %r>' % self.suggestionuuid	


"""
"""	
class Vote(db.Model): 
	def __init__(self,suggestionuuid,votinguseruuid,status):
		self.suggestionuuid = suggestionuuid
		self.votinguseruuid = votinguseruuid
		self.status = status

	__tablename__ = 'vote'
	id = db.Column(db.Integer, primary_key=True)
	suggestionuuid = Column(db.Text, ForeignKey('suggestion.uuid'), nullable=False)
	votinguseruuid = Column(db.Text, ForeignKey('user.uuid'), nullable=False)
	status = db.Column(db.String(100), nullable=True)
	
	def __repr__(self):
		return '<vote %r>' % self.suggestionuuid	



"""
"""	
class Comment(db.Model):

	def __init__(self,uuid,suggestionuuid,commenting_user_id,comment,commentDate):
		self.uuid = uuid
		self.suggestionuuid = suggestionuuid
		self.commenting_user_id = commenting_user_id
		self.comment = comment
		self.commentDate = commentDate
		


	__tablename__ = 'comment'
	id = db.Column(db.Integer, primary_key=True)
	uuid = db.Column(db.Text, unique=True, index=True)
	suggestionuuid = Column(db.Text, ForeignKey('suggestion.uuid'), nullable=False)
	commenting_user_id = Column(db.Text, ForeignKey('user.uuid'), nullable=False)
	comment = db.Column(db.Text, nullable=True)
	commentDate = db.Column(db.DateTime(200), nullable=True)
	user = db.relationship('User', backref=db.backref('comments', lazy='dynamic')) 
	suggestion = db.relationship('Suggestion', backref=db.backref('comments', lazy='dynamic')) 

	
	def __repr__(self):
		return '<User %r>' % self.uuid	


'''
TODO


     important
     a) display flag count, flag a suggestion
     b) show suggestions that have been up/down voted and by who

1) Signup
     a) prevent user with the same username and/or email from signing up
     b) 

 2) Vote (!important)
     a)  prevent user from up/down voting one suggestion twice

 3) Flag
     a) prevent user from flagging one suggestion twice      

 4) General 
     a) give feedback message to the user  
     b) 

 5) Others
      a) Host on heroku     



'''