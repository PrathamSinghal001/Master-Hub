from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length 

class RegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])

    email = StringField("Email", 
                        validators=[DataRequired(message="email is must field"), 
                                    Email(message="please write a vaild email")])

    password = PasswordField("Password",
                              validators=[DataRequired(), 
                                          Length(min=8, message="password must be at least 8 characters and also use numbers(0-9), special symbols, lowecase(a-z) & uppercase(A-Z) alphabets")])
    
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", 
                        validators=[DataRequired(), 
                                    Email()])
    
    password = PasswordField("Password", 
                             validators=[DataRequired()])
    
    submit = SubmitField("Login")