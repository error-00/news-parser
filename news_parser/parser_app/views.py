from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'title': 'Main',
    }
    return render(request, 'parser_app/index.html', context)


def account(request):
    context = {
        'title': 'Account',
    }
    return render(request, 'parser_app/account.html', context)
