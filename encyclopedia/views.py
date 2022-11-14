from django.shortcuts import render
import markdown2

from . import util

def md_to_html(title):
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdown2.markdown(content)
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "error": "No such entry exists"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
        
def search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        html_content = md_to_html(search_entry)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": search_entry,
                "content": html_content
            })
        else:
            recommendation = []
            allEntries = util.list_entries()
            for entry in allEntries:
                if search_entry.lower() in entry.lower():
                    recommendation.append(entry)
            if bool(recommendation):
                return render(request, "encyclopedia/search.html", {
                    "recommendation": recommendation
                })
            else:
                return render(request, "encyclopedia/error.html", {
                "error": "No such entry exists"
                })