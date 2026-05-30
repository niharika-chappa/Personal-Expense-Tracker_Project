from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Transaction
from forms import RegisterForm, LoginForm, TransactionForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash('Email already exists')
            return redirect(url_for('register'))

        user = User(
            username=form.username.data,
            email=form.email.data
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration Successful')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login Successful')
            return redirect(url_for('dashboard'))

        flash('Invalid Email or Password')

    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():

    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    income = sum(t.amount for t in transactions if t.type == 'Income')
    expense = sum(t.amount for t in transactions if t.type == 'Expense')

    balance = income - expense

    return render_template(
        'dashboard.html',
        transactions=transactions,
        income=income,
        expense=expense,
        balance=balance
    )


@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():

    form = TransactionForm()

    income_categories = ["Salary", "Freelance", "Business"]

    expense_categories = [
        "Food",
        "Rent",
        "Utilities",
        "Travel",
        "Shopping",
        "Education",
        "Entertainment"
    ]

    if request.method == "POST":

        if form.type.data == "Income":
            form.category.choices = [(c, c) for c in income_categories]
        else:
            form.category.choices = [(c, c) for c in expense_categories]

        if form.validate_on_submit():

            transaction = Transaction(
                title=form.title.data,
                amount=form.amount.data,
                category=form.category.data,
                type=form.type.data,
                user_id=current_user.id
            )

            db.session.add(transaction)
            db.session.commit()

            flash('Transaction Added')
            return redirect(url_for('dashboard'))

    form.category.choices = [(c, c) for c in expense_categories]

    return render_template('add_transaction.html', form=form)


@app.route('/transactions')
@login_required
def transactions():

    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    return render_template('transactions.html', transactions=transactions)


@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('Logged Out')
    return redirect(url_for('home'))


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)