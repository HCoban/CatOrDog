from django.shortcuts import render
from django.shortcuts import redirect
from .models import CatDog

def index(request):
    return render(request, "index.html")

def new(request):
    return render(request, "new.html")

def create(request):
    cat_dog = CatDog(path=request.POST['image_location'])
    cat_dog.predictAnimal()
    cat_dog.save()
    return redirect(show, cat_dog.id)

def show(request, cat_dog_id):
    cat_dog = CatDog.objects.get(id=cat_dog_id)
    return render(request, "show.html", { 'cat_dog': cat_dog })
