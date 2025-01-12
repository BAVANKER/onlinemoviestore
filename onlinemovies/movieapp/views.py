from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from movieapp.forms import MovieForm
from movieapp.models import Movie


def index(request):
    movie = Movie.objects.all()
    context = {'movielist': movie}
    return render(request, 'index.html', context)


def detail(request, movie_id):
    # return HttpResponse('this is %s'%movie_id)
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'detail.html', {'movie': movie})


def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        year = request.POST['year']
        img = request.FILES['img']
        if Movie.objects.filter(name=name).exists():
            messages.info(request, 'moviename already exists')
            return redirect('/')
        else:
            movie = Movie(name=name, desc=desc,
                          year=year,
                          img=img)
            movie.save()
            messages.info(request, 'movie saved')
            return redirect('/')
    return render(request, 'add.html')


def edit(request, id):
    movie = Movie.objects.get(id=id)
    form = MovieForm(request.POST or None, request.FILES, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit.html', {'form':form, 'movie':movie})


def delete(request, id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=id)
        movie.delete()
        return redirect('/')
    return render(request, 'delete.html')
