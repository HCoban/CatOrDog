from django.shortcuts import render
from django.shortcuts import redirect
from .models import CatDog
from django import forms

def index(request):
    class ImageForm(forms.Form):
        image_location = forms.CharField(widget=forms.TextInput(attrs={'id':'image-location', 'class': 'hidden'}))
    animals = CatDog.objects.order_by('-id')[:5]
    return render(request, "index.html", { 'animals': animals, 'form': ImageForm() })

def create(request):
    cat_dog = CatDog(path=request.POST['image_location'])
    
    cat_dog.save()
    from .celery import predict
    predict.delay(cat_dog.id, cat_dog.path)
    return redirect(show, cat_dog.id)

def show(request, cat_dog_id):
    cat_dog = CatDog.objects.get(id=cat_dog_id)
    return render(request, "show.html", { 'cat_dog': cat_dog })
