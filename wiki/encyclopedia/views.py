from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
import markdown2

from . import util


def index(request):
    entries = util.list_entries()
    if 'q' not in request.GET:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
    
    q = request.GET['q']
    if q.lower() in [e.lower() for e in entries]:
        print('yes')
        return HttpResponseRedirect(reverse("entry", kwargs={'title': q}))
    
    results = [e for e in entries if q.lower() in e.lower()]
    return render(request, "encyclopedia/search_results.html", {
        "results": results
    })


def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "error": "Entry Not Found"
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": markdown2.markdown(entry)
    })

def new_page(request):
    print(request.method)
    if request.method == 'POST':
        title = request.POST['title']
        entries = util.list_entries()
        if title.lower() in list(map(lambda e: e.lower(), entries)):
            return render(request, "encyclopedia/error.html", {
                "error": "An entry already exists with that title"
        })
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == 'POST':
        util.save_entry(title, request.POST['content'])
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "entry": entry
    })

def random_page(request):
    entries = util.list_entries()
    return HttpResponseRedirect(reverse("entry", kwargs={"title": random.choice(entries)}))
    