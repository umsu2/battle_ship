from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item


def home_page(request):

    return render(request,'home.html')

def view_list(request):

    return render(request,'list.html', {
        'item_list': Item.objects.all()
    })


def new_list(request):
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text)
    return redirect('/lists/some_list1/')