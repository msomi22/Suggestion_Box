from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    login_required

# creating the application object of class Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
# the path of our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
# initializing bootstrap
bootstrap = Bootstrap(app)
# creating the db object that will be our database
db = SQLAlchemy(app)
# creating our login manager
lm = LoginManager(app)
# if you are not logged in redirect to a view called login
lm.login_view = 'login'


# Making the form that will be used for loging in
class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 16)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

# datbase table that defines information for the user


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # columns for the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # function for registering a user in the databse
    @staticmethod
    def register(username, password):
        user = User(username=username)
        user.set_password(password)
        # adding the user to the database
        db.session.add(user)
        # saving the change made to the database
        db.session.commit()
        return user

    # function that displays how the object will be dislayed when printed
    def __repr__(self):
        return '<User {0}>'.format(self.username)

# a function that loads a user from a database
# the loginmanager will use this when it needs to look up a user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Route for logging in


@app.route('/login', methods=['GET', 'POST'])
def login():
    # creating form object
    form = LoginForm()
    # condition for if the request is a post and all validations have passed
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('index'))
    # if the validations do not pass render the form
    return render_template('login.html', form=form)

# route for logging out


@app.route('/logout')
# protecting the route
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


if __name__ == '__main__':
    db.create_all()
    # if john isn't in the database
    if User.query.filter_by(username='john').first() is None:
        # register john with the password cat
        User.register('john', 'cat')
    app.run(debug=True, port=4000)
