from django.shortcuts import render, redirect
from pydictionary import Dictionary
from .models import Search
import requests
from bs4 import BeautifulSoup

# Create your views here.

BASE_URL = 'https://www.dictionary.com/browse/{}'
BASE = 'https://www.thesaurus.com/browse/{}'


def home(request):
    return render(request, 'base.html')


def searchPage(request):

    if request.method == 'POST':
        search = request.POST["search"]
        Search.objects.create(search=search)

        new_search = BASE_URL.format(search)
        res = requests.get(new_search)
        item = BeautifulSoup(res.content, 'html.parser')
        soup = item.find('ol')
        meanings = soup.find_all('li')[0].get_text()

        new_search1 = BASE.format(search)
        res1 = requests.get(new_search1)
        item1 = BeautifulSoup(res1.content, 'html.parser')
        soup1 = item1.find_all('a', {'class': 'Bf5RRqL5MiAp4gB8wAZa'})

        synonyms = []

        for i in soup1:
            word = i.text

            synonyms.append(word)

        new_search2 = BASE.format(search)
        res2 = requests.get(new_search2)
        item2 = BeautifulSoup(res2.content, 'html.parser')
        soup2 = item2.find_all('a', {'class': 'u7owlPWJz16NbHjXogfX'})


        antonyms = []

        for i in soup2:
            word = i.text

            antonyms.append(word)

        context = {
            "meanings": meanings,
            "search": search,
            "synonyms": synonyms,
            "antonyms": antonyms
        }

        return render(request, 'search.html', context)
