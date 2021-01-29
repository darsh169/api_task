from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
    	data=JSONParser().parse(request)
    	username=data['username']
    	if username is None:
    		return None
    	try:
    		user=User.objects.get(username=username)
    	except User.DoesNotExist:
    		raise exceptions.AuthenticationFailed("no such User")
    	return (user)

    	
    
        