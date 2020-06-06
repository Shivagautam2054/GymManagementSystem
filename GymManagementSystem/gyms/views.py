from django.shortcuts import render,HttpResponse,redirect
from django.template import loader
from django.http import HttpResponse

from gyms.models import *

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings 

from uuid import uuid4


# Create your views here.
def index(request):
    template = loader.get_template("index.html")
    context = {
                'post_title' : "This is new post",
                'author' : "Shiva",
                'post_content' : "This is the content of the post",
                'item_list' : ['D1','D2','D3','D4'],
                'comments' : "This is the comment"

            }
 
    
    return HttpResponse(template.render(context, request))

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(user_name=username,password=password,status="Active").first()

        if user:
            request.session['username'] = username
            template = loader.get_template("index.html")
            context = {
                        'logged_in' : True,
                        'user' : user,
                        'username' : username
                 }

        else:
            template = loader.get_template("login.html")
            context = {
                        'logged_in' : False,
                        'message' : "Please enter valid credentials or have you activated your account?"
                 }

    elif request.method == 'GET':
        template = loader.get_template("login.html")
        context = {
				 }
 
    
    return HttpResponse(template.render(context, request))


def register(request):
    if request.method == 'GET':
        template = loader.get_template("register.html")
        context = {
                 }

    elif request.method == 'POST':
        full_name = request.POST.get('full_name')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        rand_token = uuid4().hex

        user = User()
        user.full_name = full_name
        user.user_name = user_name
        user.email = email
        user.password = password
        user.status = "Inactive"
        user.token = rand_token
        user.save()

        subject = 'Gym Fit: Activate your account'
        body = 'Please click on the below link to activate your account'
        sender_email = 'shivagautam2054@gmail.com'
        recipients = email.strip().split(" ")


        try:
            email_context = {
                                'full_name' : full_name,
                                'token' : rand_token,
                                'host' : request.get_host(),
                                'email' : email
                        }
            send_html_email(recipients, subject, 'email.html', email_context)
            #send_mail(subject, body, sender_email, recipients)
        except Exception as e:
            print("Email could not be sent.")
 
        context = {
                    "message" : "Success",
                    "full_name" : full_name,
                    "email" : email
                 }

        template = loader.get_template("register.html")

    return HttpResponse(template.render(context, request))

def activate(request):
    token = request.GET.get('token')
    email = request.GET.get('email')
    user = User.objects.filter(email=email,token=token).first()
    if user:
        user.status = "Active"
        user.save()
        context = {
                    "message" : "Success",
                    "activate" : True,                   
                 }
        template = loader.get_template("register.html")

    else:
        context = {
                    "message" : "Failure",
                    "activate" : False,                   
                 }

        template = loader.get_template("register.html")

    return HttpResponse(template.render(context, request))


def profile(request):
    context = {}
                 
    template = loader.get_template("profile.html")
    if check_session(request):
        context = {'logged_in' : True}
        return HttpResponse(template.render(context, request))


    
    return HttpResponse(template.render(context, request))

def logout(request):
    context = {}
    del request.session['username']
    return redirect('/')

def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
    msg.content_subtype= "html"  #Main content is now text/html
    return msg.send()

def check_session(request):
    user = request.session.get('username')
    if user:
        return True
    else:
        return redirect('/login')