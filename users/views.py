import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def autorization_page(request):
    return render(request, 'users/index.html')

@csrf_exempt
def get_auth(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        return JsonResponse("OK", safe=False)