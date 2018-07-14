from django.http import HttpResponse
from dbmodels.model import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json, os, string, random
from django.template import Context, Template
from django.contrib import messages
from django.db import IntegrityError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        ob = request.POST.dict()
        user = User._filter(**{"user_id" : ob["user_id"]})["data"]
        print User._filter()
        if not len(user):
            messages.add_message(request, messages.INFO, 'User not registred')
        elif user[0]["password"] != ob["password"]:
            messages.add_message(request, messages.INFO, 'User id/ password wrong')
        else:
            request.session['user_id'] = user[0]["user_id"]
            return redirect("/") 

    return render(request, 'login.html')

@require_http_methods(["GET"])
def logout(request):
    request.session.pop('user_id')
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully!')
    return redirect("/login")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        try:
            print User._filter()
            print request.POST.dict()
            obj = User._create(**request.POST.dict())
            messages.add_message(request, messages.SUCCESS, 'User created successfully')
            return redirect("/login")
        except AlreadyExists as ex:
            messages.add_message(request, messages.INFO, ex.message)
    return render(request, 'signup.html')

@require_http_methods(["GET"])
def dashboard(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.INFO, 'Unautherized')
        return redirect("/login")

    objects = Post._filter()
    for i in objects["data"]:
        i.update(User._get(i["user_id"]))
        reaction = Reaction._filter(**{"reacted_user_id" : request.session['user_id'], "post_id" : i["post_id"]})["data"]
        if reaction:
            i.update(reaction.pop())

        i["likes"] = Reaction.objects.filter(**{"reaction_type" : "Like", "post_id" : i["post_id"]}).count()
        i["dislikes"] = Reaction.objects.filter(**{"reaction_type" : "Dislike", "post_id" : i["post_id"]}).count()

    return render(request, "dashboard.html", objects)


def image_id(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

@csrf_exempt
@require_http_methods(["POST"])
def upload_post(request):
    if 'post_image' not in request.FILES or not request.FILES['post_image'].name:
        messages.add_message(request, messages.INFO, 'No image to upload!')
        return redirect("/")

    obj = request.POST.dict()
    obj["user"] = User.objects.get(user_id = request.session['user_id'])

    fil = request.FILES['post_image']
    ext = fil.name.rsplit(".", 1)[-1]

    while True:
        filename = "{}.{}".format(image_id(), ext)
        filepath = os.path.join('static', 'uploads', filename)
        fullpath =  os.path.join(BASE_DIR, filepath)
        if not os.path.exists(fullpath):
            break

    with open(fullpath, 'wb+') as destination:
        for chunk in fil.chunks():
            destination.write(chunk)
    
    obj["image_url"] = filepath
    obj = Post._create(**obj)
    return redirect("/")

@csrf_exempt
@require_http_methods(["POST"])
def add_reaction(request):
    try:
        obj = json.loads(request.body)
        
        obj["reacted_user"] = User.objects.get(user_id = request.session['user_id'])
        obj["post"] = Post.objects.get(post_id = int(obj.pop("post_id")))
        reaction_id = obj.pop("reaction_id", None) or None

        if reaction_id:
            Reaction._update(reaction_id, **obj)
            return JsonResponse({"success" : "Reaction updated successfully"})
        Reaction._create(**obj)
        return JsonResponse({"success" : "Reaction added successfully"})

    except AlreadyExists as ex:
        return JsonResponse({"error" : ex.message}, status=400)
    except IntegrityError as ex:
        return JsonResponse({"error" : ex.message}, status=400)
  
    return JsonResponse()

@csrf_exempt
@require_http_methods(["GET"])
def get_reaction(request):
    try:
        obj = request.GET.dict()
        return JsonResponse(Reaction._unique("reacted_user", **obj))
    except AlreadyExists as ex:
        return JsonResponse({"error" : ex.message}, status=400)
    return JsonResponse()



