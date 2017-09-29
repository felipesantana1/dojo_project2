from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):

    return render(request, 'dojoProject/index.html')


def wish(request):
    context = {

        'user': Users.objects.get(id=request.session['id']).username,
        'mywish': Wishes.objects.filter(user=Users.objects.get(id=request.session['id'])),
        'wishes': Wishes.objects.filter(wish=Users.objects.get(id=request.session['id'])),
        'ourwishes': Wishes.objects.exclude(wish=Users.objects.get(id=request.session['id'])).exclude(user=Users.objects.get(id=request.session['id']))

    }
    return render(request, 'dojoProject/success.html', context)

def display(request, id):
    context = {

        'wish': Wishes.objects.get(id=id),
        'users': Users.objects.filter(wish=Wishes.objects.all())
        #didn't have enough time to find correct query to display users who added item to wishlist.

    }
    return render(request, 'dojoProject/wish.html', context)

def addWish(request):
    return render(request, 'dojoProject/add.html')

def makeWish(request):
    if len(request.POST['wish']) < 3:
        messages.error(request, 'Wish Item entry must be at least 3 characters')
        return redirect('/wish/add')
    else:
        Wishes.objects.create(name=request.POST['wish'], user=Users.objects.get(id=request.session['id']))
    return redirect('/wish')


def create(request):
    errors = Users.objects.regValidator(request.POST)
    if len(errors):
        for reg, error in errors.iteritems():
            messages.error(request, error, extra_tags=reg)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = Users.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed_pw, hired=request.POST['date'])
        request.session['id'] = user.id
    return redirect('/wish')


def login(request):
    errors = Users.objects.logValidator(request.POST)
    if errors:
        for log, error in errors.iteritems():
            messages.error(request, error, extra_tags=log)
        return redirect('/')
    else:
        request.session['id'] = Users.objects.get(username=request.POST['username']).id
    return redirect('/wish')


def addMyWish(request, id):
    Wishes.objects.get(id=id).wish.add(Users.objects.get(id=request.session['id']))
    return redirect('/wish')


def delete(request, id):
    x = Wishes.objects.get(id=id)
    x.delete()
    return redirect('/wish')


def remove(request, id):
    x =  Users.objects.get(id=request.session['id'])
    y = Wishes.objects.get(id=id)
    y.wish.remove(x)
    return redirect('/wish')


def logout(request):
    request.session.clear()
    return redirect('/')


def home(request):
    return redirect('/wish')