from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
import os


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.get(int(purchased_item))
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'You have successfully purchased the item: {p_item_object.name}', category='success')
            else:
                flash(f'You don\'t have enough budget to purchase this item!', category='danger')
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', items=items, owned_items=owned_items, purchase_form=purchase_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created succesfully!', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #Se não existe erro de validação do formulário
        for err_msg in form.errors.values():
            flash(f'Error while creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        input_user = User.query.filter_by(email=form.email.data).first()
        if input_user and input_user.validate_password(input_password=form.password.data):
            login_user(input_user)
            flash('Sigend in succesfully!', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('You have entered an invalid email or password', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have signed out!', category='info')
    return redirect(url_for('home_page'))