from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from . import util

# My imports
from django import forms
import markdown2
import random
import re

class ModifiedMardonwForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class NewMarkdownForm(forms.Form):
    title = forms.CharField(label="Page Title")
    message = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "content": markdown2.markdown(util.get_entry(name))
        })
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def add(request,name=None):
    if request.method == "POST":
        form1 = ModifiedMardonwForm(request.POST)
        form2 = NewMarkdownForm(request.POST)

        if form1.is_valid() and name!="None":
            message = form1.cleaned_data["message"]

            if util.get_entry(name):
                util.save_entry(name,message)
            return wiki_page(request,name)

        elif form2.is_valid():
            title   = form2.cleaned_data["title"]
            message = form2.cleaned_data["message"]

            if util.get_entry(title):
                for e in util.list_entries():
                    if e.upper()==title.upper():
                        break
                
                return render(request,"encyclopedia/document_exist.html",{
                    "entry": e
                })
            else:
                util.save_entry(title,message)
                return wiki_page(request,title)
        else:
            return HttpResponse("complete")
    else:
        if util.get_entry(name):
            return render(request,"encyclopedia/add.html",{
                "form":ModifiedMardonwForm(initial={"message":util.get_entry(name)}),
                "name": name
            })
        else:
            return render(request,"encyclopedia/add.html",{
                "form":NewMarkdownForm(),
                "name": 'None'      
            })

def random_page(request):
    name=random.choice(util.list_entries())
    return wiki_page(request,name)

def search_results(request):
    query = request.GET.get('q')
    word =query.strip().upper()

    lista=[ l.upper() for l in util.list_entries()]
    
    if word in lista:
        for e in util.list_entries():
            if e.upper()==word:
                break

        return wiki_page(request,e)
    else:
        return render(request,'encyclopedia/search_result.html',{
            "query": word,
            "lista":util.in_list(word,util.list_entries())
        })