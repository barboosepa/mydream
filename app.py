import os
import random

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mydream.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 1. ავტორიზაციის მენეჯერი (Flask-Login)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- მწერლის და მოთხრობის მოდელები ---
class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_initials = db.Column(db.String(10))
    stories = db.relationship('Story', backref='writer', lazy=True)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'), nullable=False)

# 2. ფორმები (Flask-WTF)
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class WriterForm(FlaskForm):
    name = StringField('სახელი და გვარი', validators=[DataRequired()])
    description = TextAreaField('მოკლე აღწერა', validators=[DataRequired()])
    photo_initials = StringField('ინიციალები (მაგ: ნ.მ)', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('მწერლის დამატება')

class StoryForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired()])
    text = TextAreaField('ტექსტი', validators=[DataRequired()])
    writer_id = SelectField('ავტორი', coerce=int, validators=[DataRequired()])
    submit = SubmitField('მოთხრობის დამატება')

# 3. Routes (გვერდები)

@app.route('/')
def index():
    all_stories = Story.query.all()
    random_story = None
    if all_stories:
        random_story = random.choice(all_stories)
    return render_template('index.html', story=random_story)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/writers')
def writers():
    all_writers = Writer.query.all()
    return render_template('writers.html', writers=all_writers)

@app.route('/add_writer', methods=['GET', 'POST'])
@login_required
def add_writer():
    if not current_user.is_admin:
        flash('მხოლოდ ადმინისტრატორს შეუძლია მწერლის დამატება!')
        return redirect(url_for('index'))

    form = WriterForm()
    if form.validate_on_submit():
        new_writer = Writer(
            name=form.name.data,
            description=form.description.data,
            photo_initials=form.photo_initials.data
        )
        db.session.add(new_writer)
        db.session.commit()

        flash('მწერალი წარმატებით დაემატა ბაზაში!')
        return redirect(url_for('writers'))

    return render_template('add_writer.html', form=form)

@app.route('/add_story', methods=['GET', 'POST'])
@login_required
def add_story():
    if not current_user.is_admin:
        flash('მხოლოდ ადმინისტრატორს შეუძლია მოთხრობის დამატება!')
        return redirect(url_for('index'))

    form = StoryForm()
    form.writer_id.choices = [(w.id, w.name) for w in Writer.query.all()]

    if form.validate_on_submit():
        new_story = Story(
            title=form.title.data,
            text=form.text.data,
            writer_id=form.writer_id.data
        )
        db.session.add(new_story)
        db.session.commit()

        flash('მოთხრობა წარმატებით დაემატა ბაზაში!')
        return redirect(url_for('index'))

    return render_template('add_story.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('ეს მომხმარებელი უკვე არსებობს. აირჩიეთ სხვა სახელი.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data)

        is_first_user = User.query.count() == 0
        new_user = User(username=form.username.data, password=hashed_password, is_admin=is_first_user)

        db.session.add(new_user)
        db.session.commit()

        flash('რეგისტრაცია წარმატებით დასრულდა! ახლა შეგიძლიათ შეხვიდეთ სისტემაში.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('მონაცემები არასწორია. სცადეთ თავიდან.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.environ.get('FLASK_DEBUG', '1') == '1')
