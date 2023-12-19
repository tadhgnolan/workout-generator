from django.shortcuts import render

# Create your views here.
def generator(request):
    context = {}
    template = "generator/generator.html"
    return render(request, template, context)