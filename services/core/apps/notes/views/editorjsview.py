from django.shortcuts import render

def editorjs_view(request):
    return render(request, "notes/editorJS.html")