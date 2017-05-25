from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item, List


def home_page(request):

    return render(request,'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)

    return render(request,'list.html', {
        'list_':list_,

    })

def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text,list=list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text,list=list_)
    return redirect(f'/lists/{list_.id}/')
