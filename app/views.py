from django.shortcuts import render,redirect

from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from app.serializers import UserSerializer

User = get_user_model()


@csrf_exempt
def UserList(request):
	if request.method=="GET":
		users=User.objects.all()
		serializer=UserSerializer(users,many=True)
		return JsonResponse(serializer.data,safe=False)

	elif request.method=="POST":
		data=JSONParser().parse(request)
		serializer=UserSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data,status=201)

		return	JsonResponse(serializer.errors,status=400)

@csrf_exempt
def User1(request):#for accesing users and registering new users
	if request.method=="GET":
		id=request.session['user_id']
		user=User.objects.get(id=id)
		if user is not None:
			if user.type=="SuperAdmin":
				users=User.objects.filter(type="Man")|User.objects.filter(type="Admin")
			elif user.type=="Admin":
				users=User.objects.filter(type="Man")
			elif user.type=="Man":
				serializer=UserSerializer(user)
				return JsonResponse(serializer.data,safe=False)
				
			serializer=UserSerializer(users,many=True)
			return JsonResponse(serializer.data,safe=False)
			# return HttpResponse(user.username)
		return HttpResponse("No such user")

	if request.method=="POST":
		id=request.session['user_id']
		user=User.objects.get(id=id)

		if user is not None:
			data=JSONParser().parse(request)
			user_type=data["type"]
			serializer=UserSerializer(data=data)

			if user.type=="SuperAdmin":
				if serializer.is_valid():
					serializer.save()
					return redirect('/user1')

			elif user.type=="Admin":
				if user_type=="Man":
					if serializer.is_valid():
						serializer.save()
						return redirect('/user1')

		return HttpResponse("Forbidden Operation")

				


		# serializer=UserSerializer(user)
		# return JsonResponse(serializer.data,safe=False)



#authentication function
@csrf_exempt
def Auth(request):
	if request.method=="POST":
		data=JSONParser().parse(request)
		username=data['username']

		try:
			user =User.objects.get(username=username)
		except:
			user=None
		if user is not None:
			request.session['user_id']=user.id
			return redirect("/user1")
		return HttpResponse("no valid User")

