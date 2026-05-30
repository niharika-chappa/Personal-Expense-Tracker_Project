from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')


class TransactionForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])

    amount = FloatField('Amount', validators=[DataRequired()])

    type = SelectField(
        'Type',
        choices=[('Income', 'Income'), ('Expense', 'Expense')],
        validators=[DataRequired()]
    )

    category = SelectField(
        'Category',
        validators=[DataRequired()]
    )

    submit = SubmitField('Add Transaction')