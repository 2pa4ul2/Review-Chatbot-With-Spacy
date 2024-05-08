from django.shortcuts import render, HttpResponse
from .extract import extract

# Create your views here.
def home(request):
    import spacy
    nlp = spacy.load('en_core_web_sm')

    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        text = extract(uploaded_file)
        context['text'] = text
    return render(request, 'index.html', context)