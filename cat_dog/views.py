from django.shortcuts import render
from django.shortcuts import redirect
from .models import CatDog
from django import forms

def index(request):
    animals = CatDog.objects.order_by('-id')[:5]
    return render(request, "index.html", { 'animals': animals })

def new(request):
    class ImageForm(forms.Form):
        image_location = forms.CharField(widget=forms.TextInput(attrs={'id':'image-location', 'class': 'hidden'}))
    return render(request, "new.html", { "form": ImageForm() })

def create(request):
    cat_dog = CatDog(path=request.POST['image_location'])
    cat_dog.predictAnimal()
    cat_dog.save()
    return redirect(show, cat_dog.id)

def show(request, cat_dog_id):
    cat_dog = CatDog.objects.get(id=cat_dog_id)
    return render(request, "show.html", { 'cat_dog': cat_dog })
