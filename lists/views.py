# from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item


# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #    return HttpResponse(request.POST['item_text'])

    # return render(request, 'home.html')

    # -------------如果使用如下方法，那么get方法也能通过 start——————————
    # item = Item()
    # item.text = request.POST.get('item_text', '') #若无item_text则返回空串，所以无论怎么样都会存
    # item.save()
    # -------------如果使用如下方法，那么get方法也能通过 end——————————

    # if request.method == 'POST':
    #
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    #
    # else:
    #     new_item_text = ''
    #
    # return render(request, 'home.html', {
    #     'new_item_text': new_item_text
    # })

    #测试重定位
    if request.method == 'POST':

        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html',{'items': items})