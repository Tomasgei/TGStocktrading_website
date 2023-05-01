from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import account_activation_token
from django.contrib.auth import login
from django.core.mail import send_mail
from blog.models import Article
from .models import User


@login_required
def account_profile(request):
    context = {"section":"profile"}
    return render(request, "accounts/account_home.html", context)

@login_required
def account_premium(request):
    context = {}
    return render(request, "premium_pricing.html", context)

@login_required
def account_like(request):
    if request.POST.get("action") =="post":
        result = ""
        id = int(request.POST.get("postid"))
        post = get_object_or_404(Article, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        
        return JsonResponse({"result":result})
        
    

def account_register(request):
    if request.method == "POST":
         form = RegistrationForm(request.POST)
         if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string("registration/account_activation_email.html", {
                "user":user,
                "domain":current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
        
            send_mail(subject,message,"admin@tg.cz",[user.email])
            return HttpResponse("Registered succesfully and activation sent")
             
    else:
        registerForm = RegistrationForm()
        context = {"form": registerForm }
        return render(request, "registration/register.html", context )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/account_activation_invalid.html')    