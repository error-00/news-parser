from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_backends


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("parser_app:index"))
            else:
                print(
                    "Authentication failed"
                )  # Debug statement for failed authentication
    else:
        form = UserLoginForm()

    context = {"title": "Login", "form": form}
    return render(request, "users/login.html", context)


@login_required()
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("parser_app:index"))


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the user manually
            backend = 'users.backends.EmailBackend'
            user = auth.authenticate(request, email=user.email, password=form.cleaned_data['password1'], backend=backend)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("parser_app:index"))
    else:
        form = UserRegistrationForm()

    context = {"title": "Registration", "form": form}
    return render(request, "users/registration.html", context)


@login_required()
def profile(request):
    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("users:profile")
    else:
        form = ProfileForm(instance=request.user)

    context = {"title": f"Profile - {request.user.username}", "form": form}

    return render(request, "users/profile.html", context)
