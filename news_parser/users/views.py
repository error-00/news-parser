from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator


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
            backend = "users.backends.EmailBackend"
            user = auth.authenticate(
                request,
                email=user.email,
                password=form.cleaned_data["password1"],
                backend=backend,
            )
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
        if 'save_profile' in request.POST:
            # Handle profile update form submission
            form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("users:profile"))
        elif 'change_password' in request.POST:
            # Handle password change form submission
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Prevent logging out the user
                return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    # Add pagination for saved articles
    saved_articles = request.user.saved_articles.all().order_by('-id')
    paginator = Paginator(saved_articles, 9)  # Paginate with 9 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "title": f"Profile - {request.user.username}",
        "form": form,
        "password_form": password_form,
        "page_obj": page_obj,  # Pass the paginated saved articles
    }

    return render(request, "users/profile.html", context)
