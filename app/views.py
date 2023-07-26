from django.shortcuts import render

from django.urls import reverse

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from app.models import *
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail


def registration(request):
    USFO=UserForm()
    PFO=ProfileForm()
    d={'USFO':USFO,'PFO':PFO}
    if request.method=='POST' and request.FILES :
        USFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if USFD.is_valid()and PFD.is_valid():
            NSUFO=USFD.save(commit=False)
            submittedpassword=USFD.cleaned_data['password']
            NSUFO.set_password(submittedpassword)
            NSUFO.save()

            NSFO=PFD.save(commit=False)
            NSFO.username=NSUFO
            NSFO.save()

            send_mail('registration','successfully register','soumyanayak963@gmail.com',[NSUFO.email],fail_silently=False)
            return HttpResponse('data is saved')


    return render(request,'registration.html',d)






#resistration

def homepage(request):
    if request.session.get("username"):
        username=request.session.get('username')
        d={'username':username}
        return render(request,"homepage.html",d)
    return render(request,'homepage.html')


def user_login(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('homepage'))
            else:
                return HttpResponse('not activate')
        else:
            return HttpResponse('invalid data')
    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


#display_details
@login_required
def display_details(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_details.html',d)

#change password
@login_required
def change(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)

        UO.set_password(pw)
        UO.save()
        return HttpResponse('password change sucessfully')

    return render(request,'change.html')


#resetpassword
def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password is reset')
        else:
            return HttpResponse('invalid user')
    return render(request,'reset_password.html')

