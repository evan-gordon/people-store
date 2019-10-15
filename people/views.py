from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import store

def index(request):
  result = store.get_youngest_people(5)
  if (type(result) is dict):
    return JsonResponse({'status': 'false', 'message': result}, status=500)
  return JsonResponse({'message': result}, safe=False)