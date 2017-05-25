from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item, List


def home_page(request):

    return render(request,'home.html')

def view_list(request):

    return render(request,'list.html', {
        'item_list': Item.objects.all()
    })


def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text,list=list_)
    return redirect('/lists/some_list1/')