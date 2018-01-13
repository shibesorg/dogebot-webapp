from wtforms import Form, PasswordField, HiddenField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError


class AuthForm(Form):
    email = EmailField('Email', [
        validators.InputRequired(),
        validators.Length(min=4, max=80),
        validators.Email(),
    ])

    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=8, max=120),
    ])


class RequestPassForm(Form):
    email = EmailField('Email', [
        validators.InputRequired(),
        validators.Length(min=4, max=80),
        validators.Email(),
    ])


class ResetPasswordForm(Form):
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.length(min=8, max=120),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])

    confirm_password = PasswordField('Repeat Password', [
        validators.InputRequired(),
        validators.length(min=8, max=120),
    ])
