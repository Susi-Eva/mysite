from django.shortcuts import render
from django.http import HttpResponse
from apps.inverted import main, main2, main3

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request, 'apps/home.html')

def index(request):
    return render(request, 'apps/index.html')
def index2(request):
    return render(request, 'apps/index2.html')
def index3(request):
    return render(request, 'apps/index3.html')

def lyric(request,id):
    
    text, judul = main.detail(id)
    content={
        'no': id,
        'judul':judul,
        'text':text
    }
    return render(request, 'apps/lyric.html', content)

def lyric2(request, id):
    text,judul = main2.detail(id)

    content={
        'no': id,
        'judul':judul,
        'text':text
    }
    return render(request, 'apps/lyric2.html', content)

def lyric3(request, id):

    text,judul = main3.detail(id)

    content={
        'no': id,
        'judul':judul,
        'text':text
    }
    return render(request, 'apps/lyric3.html', content)


def result2(request):
    #%%
    # proximity_index = collections.OrderedDict(sorted(proximity_index.items()))
    # for key, value in proximity_index.items():
    #     # print (key, value)
    if request.method == 'POST':
        query = request.POST['querysearch']
        hasil = main2.main(query)

        content={
            'hasil':hasil,
            'query':query
        }
        return render(request, 'apps/result2.html',content)

def result3(request):
    #%%
    # proximity_index = collections.OrderedDict(sorted(proximity_index.items()))
    # for key, value in proximity_index.items():
    #     # print (key, value)
    if request.method == 'POST':
        query = request.POST['querysearch']
        hasil = main3.main(query)

        content={
            'hasil':hasil,
            'query':query
        }
        return render(request, 'apps/result3.html',content)

def result(request):
    #%%
    # proximity_index = collections.OrderedDict(sorted(proximity_index.items()))
    # for key, value in proximity_index.items():
    #     # print (key, value)
    if request.method == 'POST':
        query = request.POST['querysearch']
        hasil = main.main(query)

        content={
            'hasil':hasil,
            'query':query
        }
        return render(request, 'apps/result.html',content)
