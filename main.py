from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/') 
def index():
	return '<h1>Hello World!</h1>'

@app.route('/user/<name>/')
def user(name):
	return '<h1> Hello , %s! </h1>' % name 

@app.route('/about', methods=['GET', 'POST'])	
def about():
	firstname = ''
	form = NameForm()
	if form.validate_on_submit():
		firstname = form.firstname.data
		middlename = form.middlename.data
		form.firstname.data = ''
		form.middlename.data = ''
		form.lastname.data = ''
	return render_template('about.html', form=form, name=firstname)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500
	


class NameForm(FlaskForm):
	firstname = StringField('What is your firstname?', validators=[Required()])
	middlename = StringField('What is your middlename?', validators=[Required()])
	lastname = StringField('What is your lastname?', validators=[Required()])
	submit = SubmitField('Submit')




if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)