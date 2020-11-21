from django.http import JsonResponse
from django.shortcuts import render, redirect
import pandas as pd
from random import randint
from .models import GamePlay
from collections import OrderedDict
from django.contrib.sessions.models import Session
running_games = list()



def dict_list(room_id):
    current_game = GamePlay.objects.get(room_id=int(room_id)).players
    all_players = []
    players_name = list(current_game.keys())
    print(list(players_name))
    for index, item in enumerate(current_game.items()):
        all_players.append([item[0], item[1]['age']])
    print(all_players)
    context = {
        'room_id': room_id,
        'players': all_players
    }
    return context


def append_player(players, name, age_grp):
    players[name] = OrderedDict([
        ('age', age_grp),
        ('score', 0)])
    return players


# Create your views here.
def home(request):
    # View code here...
    return render(request, 'index.html')


def new_game(request):
    # View code here...
    if request.method == 'POST':
        name = request.POST['name']
        room_id = request.POST['room_id']
        age_grp = request.POST['age']
        # print(request.session.get('room_id'))
        if request.session.get('room_id', None) != room_id:
            game = GamePlay(room_id=room_id, players={
                                            name: {
                                                'age': age_grp,
                                                'score': 0
                                            }
                                        })
            game.save()
        # finally:

        context = dict_list(room_id)
        return render(request, 'players.html', context)
    else:
        while True:
            room_id = randint(1, 10001)
            if room_id not in running_games:
                break
        running_games.append(room_id)
        context = {'room_id': room_id}
        request.session['room_id'] = room_id
        # print(request.session['room_id'])
        return render(request, 'new_game.html', context)


def add_players(request):
    if request.method == 'POST':
        name = request.POST['name']
        room_id = request.POST['room_id']
        age_grp = request.POST['age']
        players = None
        try:
            players = GamePlay.objects.get(room_id=room_id).players
        except:
            return redirect(home)
        finally:
            request.session['room_id'] = room_id
            if players:
                players = append_player(players, name, age_grp)
            # print(players)
            GamePlay.objects.filter(room_id=room_id).update(players=players)
            context = dict_list(room_id)
        return render(request, 'players.html', context)
    else:
        return render(request, 'add_player.html')


def ajax_player_update(request):
    if request.method == 'GET':
        room_id = request.GET.get('room_id', None)
        players = GamePlay.objects.get(room_id=room_id).players
        player_names = list(players.keys())
        # print(player_names)
        data = {
            'room_id': room_id,
            'players': players,
            'player_names': player_names
        }
        if data['players']:
            return JsonResponse(data)
        else:
            return JsonResponse('Invalid')

#######
#starting Actual Game implentation here
#######

age12_15 = pd.read_csv('data/12to15.csv',encoding='latin1')
age16_18 = pd.read_csv('data/16to18.csv',encoding='latin1')


def quiz(request):
    if request.method == 'GET':
        room_id = request.session['room_id']
        players = GamePlay.objects.get(room_id=room_id).players
        context = {
            'room_id': room_id,
            'players': players
        }
        return render(request, 'quiz.html', context)
    # else:
    #     return render(request, 'quiz.html')


def ajax_quiz(request):
    if request.method == 'GET':
        data = ['age12_15','age16_18']
        age_grp = request.get['age_grp']
        age = int(age_grp[:1])
        
        return JsonResponse('Hello')