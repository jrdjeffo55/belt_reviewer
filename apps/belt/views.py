from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
from datetime import datetime
from .forms import *
import bcrypt
from django.db.models import Count

def index(request):
    if "id" in request.session:
        return redirect("/books")
    logform = LogForm()
    regform = RegForm()
    if request.method == "POST":
        if "password_confirmation" in request.POST:
            regform = RegForm(request.POST)
            if regform.is_valid():
                form = regform.cleaned_data
                newuser = User.objects.create(first_name=form["first_name"], last_name=form["last_name"], email=form["email"], hashed_pw=bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()))
                request.session["id"] = newuser.id
                return redirect("/books")
        else:
            logform = LogForm(request.POST)
            if logform.is_valid():
                form = logform.cleaned_data
                request.session["id"] = User.objects.get(email=form["email"]).id
                return redirect("/books")
    context = {
        "logform" : logform,
        "regform" : regform
    }
    return render(request, "belt/index.html", context)

def home(request):
    if "id" not in request.session:
        return redirect("/")
    last_three = Review.objects.all().order_by("-created_at")[:3]
    context = {
        "range" : range(0,5),
        "current" : User.objects.get(id=request.session["id"]),
        "all_users" : User.objects.all(),
        "books" : Book.objects.all(),
        "reviews" : last_three,
    }
    return render(request, "belt/books.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def create(request):
    if "id" not in request.session:
        return redirect("/")
    if request.method == "POST":
        form = BookReviewForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if len(form["new_author"]) > 0:
                author = Author.objects.create(name=form["new_author"])
            else:
                author = Author.objects.get(name=form["author"])
            book = Book.objects.create(title=form["title"], author=author)
            Review.objects.create(rating=form["rating"], comment=form["review"], book=book, reviewer=User.objects.get(id=request.session["id"]))
            return redirect("/books")
    else:
        form = BookReviewForm()
    return render(request, "belt/add.html", {'form': form})

def showbook(request, id):
    if "id" not in request.session:
        return redirect("/")
    book = Book.objects.get(id=int(id))
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            Review.objects.create(rating=form["rating"], comment=form["add_review"], book=book, reviewer=User.objects.get(id=request.session["id"]))
            return redirect("/books/"+id)
    else:
        form = ReviewForm()
    context = {
        "current" : User.objects.get(id=request.session["id"]),
        "range" : range(0,5),
        "form" : form,
        "book" : book,
        "author" : Author.objects.get(book=int(id)),
        "reviews" : Review.objects.filter(book=int(id)).order_by("-created_at"),
        "all_users" : User.objects.all(),
    }
    return render(request, "belt/show.html", context)

def destroy(request, id):
    if "id" not in request.session:
        return redirect("/")
    if request.method == "POST":
        Review.objects.get(id=int(id)).delete()
    return redirect("/books")

def showuser(request, id):
    if "id" not in request.session:
        return redirect("/")
    context = {
        'user' : User.objects.filter(id=int(id)).annotate(total_reviews=Count("review"))[0],
        'books' : Book.objects.filter(review__reviewer=int(id)).distinct()
    }
    return render(request, "belt/user.html", context)
