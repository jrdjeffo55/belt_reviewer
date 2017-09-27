from django import forms
from models import *
from datetime import datetime
import re
import bcrypt

LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")

class LogForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    def clean(self):
        data = self.cleaned_data
        user = User.objects.filter(email=data.get("email"))
        if not user:
            self.add_error("email", "That email is not registered")
        elif not bcrypt.checkpw(data.get("password").encode(), user[0].hashed_pw.encode()):
            self.add_error("password", "Incorrect password")

class RegForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=255, widget=forms.PasswordInput)
    def clean(self):
        data = self.cleaned_data
        if len(data.get("first_name")) < 2:
            self.add_error("first_name", "First name must be at least 2 characters")
        if not LETTER_REGEX.match(data.get("first_name")):
            self.add_error("first_name", "First name must have only alphabetic characters")
        if len(data.get("last_name")) < 2:
            self.add_error("last_name", "Last name must be at least 2 characters")
        if not LETTER_REGEX.match(data.get("last_name")):
            self.add_error("last_name", "Last name must have only alphabetic characters")
        if User.objects.filter(email=data.get("email")):
            self.add_error("email", "Email already registered")
        if len(data.get("password")) <8:
            self.add_error("password", "Password must be at least 8 characters")
        if data.get("password") != data.get("password_confirmation"):
            self.add_error("password_confirmation", "Password confirmation must match")

class ReviewForm(forms.Form):
    add_review = forms.CharField(max_length=255, widget=forms.Textarea)
    rating = forms.ChoiceField(choices=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")))

def author_namelist():
    return Author.objects.values_list("name", "name")

class BookReviewForm(forms.Form):
    title = forms.CharField(max_length=255)
    author = forms.ChoiceField(choices=author_namelist, required=False)
    new_author = forms.CharField(max_length=255, required=False)
    review = forms.CharField(max_length=255, widget=forms.Textarea)
    rating = forms.ChoiceField(choices=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")))
    def clean(self):
        data = self.cleaned_data
        if len(data.get("author")) < 1 and len(data.get("new_author")) < 1:
            self.add_error("new_author", "Must have an author")
        elif Author.objects.filter(name=data.get("new_author")):
            self.add_error("new_author", "Author already exists")