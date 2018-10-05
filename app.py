"""Adoption application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Pets
from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired,InputRequired,AnyOf,URL, NumberRange
from flask_wtf import FlaskForm
from petfunctions import get_random_pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] ='SOSECRET'
debug=DebugToolbarExtension(app)

class AddPetForm(FlaskForm):
    """Form class for adding a pet"""

    name = StringField('Pet Name')
    #make this a dropdown (species)
    species = StringField('Pet Species',validators=[InputRequired(),AnyOf(['dog','cat','porcupine','pickle'])])
    photo_url = StringField('Pet Photo Url',validators=[InputRequired(),URL()])
    age = IntegerField('Pet Age',validators=[InputRequired(), NumberRange(0, 30, "Age must be between 0 and 30")])
    notes = TextAreaField('Notes')

class EditPetForm(FlaskForm):
    """"Form class for editing pets"""
    
    photo_url = StringField('Pet Photo Url',validators=[InputRequired(),URL()])
    notes = TextAreaField('Notes')
    available = BooleanField('Available')


@app.route('/')
def pet_list():
    """Display a homepage of pets we can adopt"""

    pets = Pets.query.all()

    pet_name,pet_age,pet_url = get_random_pet()
    
    return render_template('index.html',pets=pets,pet_name=pet_name,pet_age=pet_age,pet_url=pet_url)

@app.route('/add', methods=['GET','POST'])
def add_pet_form():
    """Add pet to adoption database form"""

    form = AddPetForm()
    
    if form.validate_on_submit():
        name = form.data['name']
        species = form.data['species']
        photo_url = form.data['photo_url']
        age = form.data['age']
        notes = form.data['notes']

        pet = Pets(name=name,
                   species=species,
                   photo_url=photo_url,
                   age=age,
                   notes=notes,
              )

        db.session.add(pet)
        db.session.commit()

        return redirect('/')

    else:
        return render_template('add_pet_form.html',form=form)

@app.route('/<int:pet_id>', methods=['GET','POST'])
def pet_page(pet_id):
    """Display pet details and a form to edit pet"""

    pet = Pets.query.get_or_404(pet_id)

    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.data['photo_url']
        pet.notes = form.data['notes']
        pet.available = form.data['available']

        db.session.commit()

        return redirect(f'/{pet_id}')

    else:
        return render_template('pet_details.html',pet=pet, form=form)
