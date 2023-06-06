from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = bool(request.POST.get('remember_me'))

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)  # Set session expiration to browser close
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
