from market import app
from flask import render_template, redirect, url_for
from market.models import Item, User
from market.forms import RegisterForm
from market import db


@app.route("/")
@app.route("/home")
def home_world():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data,
                              email=form.email.data,
                              password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #Se não existe erro de validação do formulário
        for err_msg in form.errors.values():
            print(f'Error while creating user: {err_msg}')
    return render_template('register.html', form=form)