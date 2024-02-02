from django.shortcuts import render
from markdown2 import markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect


class NewSearchForm(forms.Form):
    text_form = forms.CharField(label="Search Encyclopedia:")


class NewTitleForm(forms.Form):
    new_title = forms.CharField(widget=forms.Textarea)


class NewContentForm(forms.Form):
    new_content = forms.CharField(widget=forms.Textarea)


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
        text_html = f"Page {title} has not been found!"
    else:
        text_html = markdown(open(f"entries/{title}.md").read())
    return render(request, "encyclopedia/title.html", {
        "title_name": title_name,
        "text_html": text_html,
        "entries": util.list_entries(),
        "form": NewSearchForm(),
    })


def search_html(request):
    title1 = request.GET.get("search_box")
    title_name = f"{title1}"
    text_html = util.get_entry(title1)
    if text_html is None:
        lists = []
        for i in util.list_entries():
            if title1 in i:
                lists.append(i)
        return render(request, "encyclopedia/search.html", {
            "form": NewSearchForm(),
            "lists": lists,
            "entries": entries,
            "title1": title1})
    else:
        text_html = markdown(open(f"entries/{title1}.md").read())
        return render(request, "encyclopedia/title.html", {
            "title_name": title_name,
            "text_html": text_html,
            "entries": util.list_entries(),
            "form": NewSearchForm(),
        })


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
                return render(request, "encyclopedia/search.html", {
                    "form": NewSearchForm(),
                    "lists": lists,
                    "entries": entries,
                    "title1": title1,
                })
            else:
                text_html = markdown(open(f"entries/{title1}.md").read())
                return render(request, "encyclopedia/title.html", {
                    "title_name": title_name,
                    "text_html": text_html,
                    "entries": util.list_entries(),
                    "form": NewSearchForm(),
                    "title1": title1,
                })


def create(request):
    warning_message = ""
    if request.method == "POST":
        form_title = NewTitleForm(request.POST)
        form_content = NewContentForm(request.POST)
        if form_title.is_valid() and form_content.is_valid():
            title3 = form_title.cleaned_data["new_title"]
            content = form_content.cleaned_data["new_content"]
            if title3 not in util.list_entries():
                with open(f"entries/{title3}.md", 'w', encoding="utf-8") as f:
                    f.write(f"{content}")
                    return HttpResponseRedirect(f"{title3}")
            else:
                warning_message = "This title exist, try another word!"
    return render(request, "encyclopedia/create.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm(),
        "form_title": NewTitleForm(),
        "form_content": NewContentForm(),
        "warning_message": warning_message,
    })


def edit(request, title):
    title_name1 = f"{title}"
    with open(f"entries/{title_name1}.md", "r", encoding="utf-8") as f:
        previous_text = f.read()

    class NewEditForm(forms.Form):
        new_edit = forms.CharField(widget=forms.Textarea, initial=previous_text)

    if request.method == "POST":
        form_edit = NewEditForm(request.POST)
        if form_edit.is_valid():
            edited_content = form_edit.cleaned_data["new_edit"]
            with open(f"entries/{title_name1}.md", 'w', encoding="utf-8") as fo:
                fo.write(f"{edited_content}")
                return HttpResponseRedirect(f"/wiki/{title_name1}")


    return render(request, "encyclopedia/edit.html", {
            "form": NewSearchForm(),
            "entries": util.list_entries(),
            "form_edit": NewEditForm(),
            "previous_text": previous_text,
            "title_name1": title_name1,
            })