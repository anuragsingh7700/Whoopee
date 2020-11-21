from django.shortcuts import render,redirect
from random import randint
from django.contrib.sessions.models import Session
running_games = list()


# Create your views here.
def home(request):
    # View code here...
    return render(request, 'index.html')


def new_game(request):
    # View code here...
    while True:
        room_id = randint(1, 10001)
        if room_id not in running_games:
            break
    running_games.append(room_id)
    context = {'room_id': room_id}
    # request.session['room_id'] = room_id
    print(request.session['room_id'])
    return render(request, 'new_game.html', context)


def add_players(request):
    if request.method == 'POST':
        name = request.POST['name']
        room_id = request.POST['room_id']
        age_grp = request.POST['age']
        print(name, age_grp, room_id)
        print(running_games)
        return render(request, 'players.html')
    else:
        return redirect(home)