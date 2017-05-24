from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item


def home_page(request):

    if request.method == 'POST':

        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')

    return render(request,'home.html', {
            'item_list': Item.objects.all()
    })

