from django.shortcuts import render
from markdown2 import markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect


class NewSearchForm(forms.Form):
    text_form = forms.CharField(label="Search Encyclopedia:")


entries = util.list_entries()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm(),
    })


def title(request, title):
    title_name = f"{title}"
    text_html = util.get_entry(title)
    if text_html is None:
        text_html = f"Page {title} is not found"
    else:
        text_html = markdown(open(f"entries/{title}.md").read())

    return render(request, "encyclopedia/title.html", {
        "title_name": title_name,
        "text_html": text_html,
        "entries": util.list_entries(),
        "form": NewSearchForm(),
    })


def search_html(request):
    title1 = request.GET.get('search_box')
    title_name = f"{title}"
    text_html = util.get_entry(title1)
    if text_html is None:
        lists = []
        for i in util.list_entries():
            if title1 in i:
                list.append(i)
        return render(request, "encyclopedia/search.html", {
            "form": NewSearchForm(),
            "list": list,
            "entries": entries,
            "title": title1
        })
    else:
        text_html = markdown(open(f"entries/{title1}.md").read())
        return render(request, "encyclopedia/title.html", {
            "title_name": title_name,
            "text_html": text_html,
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })
