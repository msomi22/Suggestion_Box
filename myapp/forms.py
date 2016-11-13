from wtforms import Form, StringField, HiddenField, PasswordField, TextAreaField, validators, SubmitField

class SignupForm(Form):
    firstname = StringField('Firstname') #[validators.Length(min=4, max=25)]
    lastname = StringField('Lastname')
    email = StringField('Email Address')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Signup')
    

class LoginForm(Form):
	username = StringField('Username')
	password = PasswordField('Password') 
	submit = SubmitField('Login')


class SuggestionForm(Form):
	 title = StringField('Title') # [validators.Length(min=10, max=35)]
	 suggestion = TextAreaField('Your suggestion') 
	 submit = SubmitField('Suggest')
	 
class CommentForm(Form):
	comment = TextAreaField('Your comment')  
	base_user = HiddenField('base_user')
	suggestionid = HiddenField('suggestionid') 
	submit = SubmitField('Comment')
	
class VoteForm(Form):
	suggestionid = HiddenField('suggestionid')
	votestatus = HiddenField('votestatus')
	submit = SubmitField('Vote') 
	

class FlagForm(Form):
	suggestionid = HiddenField('suggestionid') 
	submit = SubmitField('Flag')
	

