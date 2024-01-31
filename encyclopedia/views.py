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
