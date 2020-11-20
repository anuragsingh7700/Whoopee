from django.shortcuts import render


# Create your views here.
def home(request):
    # View code here...
    return render(request, 'new_game.html')
