from django.shortcuts import render
from django.http import HttpResponse  # HttpResponse('Hello, World !!')
from django.shortcuts import render
from django.views import View
import os
# from django import template
from ctrlS.views_module import asdf, ctrlS
# Create your views here.

class HelloView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'folder': 'D:\Twitter',
            'message': "始まりました",
        }
        return render(request, 'ctrlS/hello.html', context)

    def post(self, request, *args, **kwargs):
        nakami = request.POST
        # a = asdf.asdf(nakami['folder'])
        a = ctrlS.main(nakami['folder'])
        context = {
            'folder': 'D:\Twitter',# + '@gmail.com', 
            'message': a,
        }
        return render(request, 'ctrlS/hello.html', context)

hello = HelloView.as_view()

# def hello(request):
#     context = {
#             'message': "Hello World! from View!!",
#         }
#     if request.method == 'POST':

#         context = {
#                     'message': "POST method OK!!",
#                 }
#     return render(request, 'ctrlS/hello.html', context)

