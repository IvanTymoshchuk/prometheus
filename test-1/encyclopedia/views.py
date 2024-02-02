from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import markdown

from . import util


class NewSearchForm(forms.Form):
    text_form = forms.CharField(label="Search Encyclopedia:")


entries = util.list_entries()


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {
            "entries": util.list_entries(),
            "form": NewSearchForm(),
        },
    )


def title(request, title):
    title_name = title
    text_html = util.get_entry(title)
    if text_html is None:
        text_html = f"Page {title} has not been found!"
    else:
        text_html = markdown(open(f"entries/{title}.md").read())

    return render(
        request,
        "encyclopedia/title.html",
        {
            "title_name": title_name,
            "text_html": text_html,
            "entries": util.list_entries(),
            "form": NewSearchForm(),
        },
    )


def search_html(request):
    title1 = request.GET.get("search_box")
    title_name = title1
    text_html = util.get_entry(title1)
    if text_html is None:
        lists = [i for i in util.list_entries() if title1 in i]
        return render(
            request,
            "encyclopedia/search.html",
            {
                "form": NewSearchForm(),
                "lists": lists,
                "entries": util.list_entries(),
                "title": title1,
            },
        )
    else:
        text_html = markdown(open(f"entries/{title1}.md").read())
        return render(
            request,
            "encyclopedia/title.html",
            {
                "title_name": title_name,
                "text_html": text_html,
                "entries": util.list_entries(),
                "form": NewSearchForm(),
            },
        )


def search_form(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            title1 = form.cleaned_data["text_form"]
            title_name = f"{title1}"
            text_html = util.get_entry(title1)
            if text_html is None:
                lists = []
                for i in util.list_entries():
                    if title1 in i:
                        lists.append(i)
                return render(
                    request,
                    "encyclopedia/search.html",
                    {
                        "form": NewSearchForm(),
                        "lists": lists,
                        "entries": entries,
                        "title1": title1,
                    },
                )
            else:
                text_html = markdown(open(f"entries/{title1}.md").read())
                return render(
                    request,
                    "encyclopedia/title.html",
                    {
                        "title_name": title_name,
                        "text_html": text_html,
                        "entries": util.list_entries(),
                        "form": NewSearchForm(),
                        "title1": title1,
                    },
                )
