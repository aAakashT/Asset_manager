from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AssetForm, AssetImageForm, AssetTypeForm

from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from .forms import AssetForm, AssetImageForm, AssetTypeForm
from chartjs.views.lines import BaseLineChartView
from django.views.generic import TemplateView

from .models import Asset, AssetImage, AssetType

import csv
from django.http import HttpResponse

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
                request.session.set_expiry(0)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')





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


@login_required
def create_asset_type(request):
    if request.method == 'POST':
        form = AssetTypeForm(request.POST)
        if form.is_valid():
            asset_type = form.save()
            messages.success(request, 'Asset type created successfully.')
            return redirect('asset_types')
    else:
        form = AssetTypeForm() 
    return render(request, 'create_asset_type.html', {'form': form})



class AssetTypeListJson(BaseDatatableView):
    model = AssetType
    columns = ['id', 'asset_type', 'description', 'created_at', 'updated_at']
    order_columns = ['id', 'asset_type', 'description', 'created_at', 'updated_at']
    max_display_length = 10
    def render_column(self, row, column):
        if column == 'actions':
            return f'<a href="#" class="delete_asset_type" data-id="{row.pk}">Delete</a>'+\
              f'<a href="#" class="update_asset_type" data-id="{row.pk}">update    </a>' # added underscoes to delete asset type
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        return self.model.objects.all()


class AssetTypeListView(TemplateView):  
    template_name = 'list_asset_types.html'

@login_required
def update_asset_type(request, pk):
    asset_type = get_object_or_404(AssetType, pk=pk)
    if request.method == 'POST':
        form = AssetTypeForm(request.POST, instance=asset_type)
        if form.is_valid():
            asset_type = form.save()
            return redirect('asset_types')
    else:
        form = AssetTypeForm(instance=asset_type)
    return render(request, 'update_asset_type.html', {'form': form, 'asset_type': asset_type})

@login_required
def delete_asset_type(request, pk):
    asset_type = get_object_or_404(AssetType, pk=pk)
    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            asset_type.delete()
            messages.success(request, 'Asset type and its assets deleted successfully.')
        else:
            messages.info(request, 'Asset type deletion cancelled.')
        return redirect('asset_types')
    return render(request, 'delete_asset_type.html', {'asset_type': asset_type})


# Create operation for Asset
def create_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assets')  
    else:
        form = AssetForm()
    return render(request, 'create_asset.html', {'form': form})

class AssetListJson(BaseDatatableView):
    model = Asset
    columns = ['id', 'asset_name', 'asset_code', 'asset_type', 'is_active', 'created_at', 'updated_at', '_prefetched_objects_cache'] 
    order_columns = ['id', 'asset_name', 'asset_code', 'asset_type', 'is_active', 'created_at', 'updated_at', '_prefetched_objects_cache'] 
    print(Asset.objects.all().prefetch_related('images').order_by('-created_at'))
    def render_column(self, row, column):
        if column == 'actions':
            return f'<a href="#" class="asset-delete" data-id="{row.pk}">Delete</a>'+\
              f'<a href="#" class="update_asset" data-id="{row.pk}">update</a>' # added underscoes to delete asset type
        else:
            return super().render_column(row, column)
 
    def get_initial_queryset(self):
        # for i in self.model.objects.all().prefetch_related('images').order_by('-created_at'):
            # for j in i.__dict__.get('_prefetched_objects_cache'):
                # print(j)
        #         print(i.__dict__)
        #         print(i._prefetched_objects_cache)
        #         k = i._prefetched_objects_cache['images']
        #         for j in k:
        #             print(j.__dict__)
        #         print((k)) 
 
        # print(self.model.objects.all().prefetch_related('images').order_by('-created_at'))
        return self.model.objects.all().prefetch_related('images').order_by('-created_at')

class AssetListView(TemplateView):  
    template_name = 'asset_list.html'


class AssetDeleteView(View):
    def get(self, request, id):
        try:
            asset = Asset.objects.get(id=id)
            asset.delete()
        except Exception:
            pass
        return redirect('assets')

# Update operation for Asset
@login_required
def update_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('assets')  
    else:
        form = AssetForm(instance=asset)
    return render(request, 'update_asset.html', {'form': form, 'asset': asset})

@login_required
def create_asset_image(request):
    if request.method == 'POST':
        form = AssetImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("sucess")
            return redirect('assets')  
    else:
        form = AssetImageForm()
    return render(request, 'create_asset_image.html', {'form': form})


@login_required
def download_assets_view(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Asset Name', 'Asset Code', 'Asset Type', 'Is Active', 'Created At', 'Updated At'])

    assets = Asset.objects.all().order_by('-created_at')

    for asset in assets:
        writer.writerow([asset.asset_name, asset.asset_code, asset.asset_type.asset_type,
                         asset.is_active, asset.created_at, asset.updated_at])

    return response

