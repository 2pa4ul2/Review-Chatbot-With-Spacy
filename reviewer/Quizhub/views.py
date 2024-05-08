from django.shortcuts import render, HttpResponse
from .extract import extract

# Create your views here.
def home(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        text = extract(uploaded_file)
        context['text'] = text
    return render(request, 'home.html', context)