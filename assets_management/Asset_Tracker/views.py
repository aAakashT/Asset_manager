from django.shortcuts import render, redirect
from django.contrib import messages
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


from chartjs.views.lines import BaseLineChartView
from .models import Asset, AssetType, AssetImage
from django.views.generic import TemplateView



class AssetChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["asset_chart"] = self.get_asset_chart_data()
        context["asset_chart_inactive"] = self.get_asset_chart_data_inactive()
        return context

    def get_asset_chart_data(self):
        asset_types = AssetType.objects.all()
        labels = [asset_type.asset_type for asset_type in asset_types]
        data = [Asset.objects.filter(asset_type=asset_type).count() for asset_type in asset_types]
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Number of Assets',
                'data': data,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1,
            }]
        }

    def get_asset_chart_data_inactive(self):
        active_count = Asset.objects.filter(is_active=True).count()
        inactive_count = Asset.objects.filter(is_active=False).count()
        labels = ['Active', 'Inactive']
        data = [active_count, inactive_count]
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Number of Assets',
                'data': data,
                'backgroundColor': ['rgba(54, 162, 235, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                'borderColor': ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
                'borderWidth': 1,
            }]
        }

def chart_view(request):
    return render(request, 'chart.html')
