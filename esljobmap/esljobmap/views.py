from django.shortcuts import render


def home(request):
    user_email = None
    if request.user.is_authenticated:
        user_email = request.user.email
    return render(request, 'core/home.html', {'user_email': user_email})
