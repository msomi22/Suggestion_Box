from wtforms import Form, StringField, HiddenField, PasswordField, TextAreaField, validators, SubmitField
#from flask_wtf import Form

class SignupForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=4, max=25)])
    lastname = StringField('Lastname', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    

class LoginForm(Form):
	username = StringField('Username')
	password = PasswordField('Password') 
	submit = SubmitField('Submit')


class SuggestionForm(Form):
	 title = StringField('Firstname', [validators.Length(min=10, max=35)])
	 suggestion = TextAreaField('Your suggestion', [validators.length(max=200)]) 
	 #useruuid = HiddenField('useruuid')
	 #status = HiddenField('status')

class CommentForm(Form):
	comment = TextAreaField('Your comment')  
	 #base_user = HiddenField('base_user')
	 #commenting_user = HiddenField('commenting_user')

class VoteForm(Form):
	#base_user = HiddenField('base_user')
	#commenting_user = HiddenField('commenting_user')
	pass 

class FlagForm(Form):
	#base_user = HiddenField('base_user')
	#commenting_user = HiddenField('commenting_user')
	pass 

