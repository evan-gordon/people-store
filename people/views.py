from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import store

def index(request):
  result = store.get_youngest_people(5)
  if (type(result) is str):
    return HttpResponse(result, status=500)
  return JsonResponse({'result': result}, safe=False)