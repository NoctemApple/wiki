from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The page '{title}' was not found"
        })

    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q")

    if query:
        entries = util.list_entries()

        query_lower = query.lower()

        for entry in entries:
            if entry.lower() == query_lower:
                return redirect("wiki", title=entry)

        results = [entry for entry in entries if query_lower in entry.lower()]

        return render(request, "encyclopedia/search.html", {
            "entries": results,
            "query": query
        })

    return redirect("index")
    
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
            "message": f"The page '{title}' already exists"
        })

        util.save_entry(title, content)
        return redirect("wiki", title=title)

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("wiki", title=title)
    
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"the page{title}"
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def randomizer(request):
    entries = util.list_entries()
    gacha = random.choice(entries)
    return redirect("wiki", title=gacha)