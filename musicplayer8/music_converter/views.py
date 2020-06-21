from django.shortcuts import render

def index(request):
    return render(request, 'music_converter/index.html')