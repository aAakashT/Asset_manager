import csv

from chartjs.views.lines import BaseLineChartView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from .forms import AssetForm, AssetImageForm, AssetTypeForm
from .models import Asset, AssetImage, AssetType

# Create your views here.


def login_view(request):
    """if user is authenticated then renders dashboard else renders login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')    
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
    return render(request, 'login_copy.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class AssetChartView(TemplateView):
    """seperating active and inactive using query and rendering them"""
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["asset_chart"] = self.get_asset_chart_data()
        context["asset_chart_inactive"] = self.get_asset_chart_data_inactive()
        return context

    def get_asset_chart_data(self):
        # get data with query filter it on count
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
@login_required
def chart_view(request):
    return render(request, 'chart.html')

@login_required
def create_asset_type(request):
    """If request is post then after validating data is created and message is sent"""
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
    """returns json type data with colums on queryset, hit by ajax call"""
    model = AssetType
    columns = ['id', 'asset_type', 'asset_description', 'created_at', 'updated_at']
    order_columns = ['id', 'asset_type', 'asset_description', 'created_at', 'updated_at']
    max_display_length = 10
    def render_column(self, row, column):
        if column == 'actions':
            return f'<a href="#" class="delete_asset_type" data-id="{row.pk}">Delete</a>'+\
              f'<a href="#" class="update_asset_type" data-id="{row.pk}">update</a>' # added underscoes to delete asset type
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        return self.model.objects.all()

class AssetTypeListView(TemplateView):  
    """ connected to assettypelistjson and renders datatable using assettypelistjson"""
    template_name = 'list_asset_types.html'

@login_required
def update_asset_type(request, pk):
    """if asset type is not present then will return 404"""
    asset_type = get_object_or_404(AssetType, pk=pk)
    if request.method == 'POST':
        form = AssetTypeForm(request.POST, instance=asset_type)
        if form.is_valid():
            asset_type = form.save()
            return redirect('asset_types')
    else:
        form = AssetTypeForm(instance=asset_type)
    return render(request, 'update_asset_type.html', {'form': form, 'asset_type': asset_type})

class AssetTypeDeleteView(View):
    def post(self, request, pk):
        try:
            asset_type = get_object_or_404(AssetType, id=pk)
            asset_type.delete()
            return redirect('asset_types')  
        except AssetType.DoesNotExist:
            return redirect('asset_types', error='Asset_Type does not exist')
        except Exception as e:
            return redirect('asset_types', error='An error occurred while deleting the asset_type: ' + str(e))

class AssetDeleteView(View):
    """if asset is not present then gives 404"""
    def get(self, request, id):
        try:
            asset = get_object_or_404(Asset, id=id)
        except Asset.DoesNotExist:
            return redirect('assets', error=f'Asset with {id} does not exist')    
        return render(request, 'asset_delete.html', {'asset': asset})

    def post(self, request, id):
        try:
            asset = get_object_or_404(Asset, id=id)
            asset.delete()
            return redirect('assets')  
        except Asset.DoesNotExist:
            return redirect('assets', error='Asset does not exist')
        except Exception as e:
            return redirect('assets', error='An error occurred while deleting the asset: ' + str(e))
# Create operation for Asset
def create_asset(request):
    """fills form with data and validates the data and saves the object"""
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assets')  
    else:
        form = AssetForm()
    return render(request, 'create_asset.html', {'form': form})

class AssetListJson(BaseDatatableView):
    """renders columns with order column and loads on get initial queryset"""
    model = Asset
    columns = ['id', 'asset_name', 'asset_code', 'asset_type', 'is_active', 'created_at', 'updated_at', '_prefetched_objects_cache', '_prefetched_objects_cache'] 
    order_columns = ['id', 'asset_name', 'asset_code', 'asset_type', 'is_active', 'created_at', 'updated_at', '_prefetched_objects_cache', '_prefetched_objects_cache'] 
    print(Asset.objects.all().prefetch_related('images').order_by('-created_at'))
    def render_column(self, row, column):
        if column == 'actions':
            return f'<a href="#" class="asset-delete" data-id="{row.pk}">Delete</a>'+\
              f'<a href="#" class="update_asset" data-id="{row.pk}">update</a>'
        else:
            return super().render_column(row, column)
 
    def get_initial_queryset(self):
        return self.model.objects.all().prefetch_related('images').order_by('-created_at')

class AssetListView(TemplateView):  
    template_name = 'asset_list.html'

# Update operation for Asset
@login_required
def update_asset(request, pk):
    """ if form is valid then i will update the asset """
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return redirect('assets')    
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
    """if request is post then cretes asset image else will render the form"""
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
    """using csv and writerow with list of columns and using for loop to append data and sending as text/csv file respose"""  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assets.csv"'
    writer = csv.writer(response)
    writer.writerow(['Asset Name', 'Asset Code', 'Asset Type', 'Is Active', 'Created At', 'Updated At'])
    assets = Asset.objects.all().order_by('-created_at')
    for asset in assets:
        writer.writerow([asset.asset_name, asset.asset_code, asset.asset_type.asset_type,
                         asset.is_active, asset.created_at, asset.updated_at])
    return response

def update_image(request, pk):
    """try for Asset image if object does not exist then redirects to asset_list"""
    try:
        image = AssetImage.objects.get(pk=pk) 
    except AssetImage.DoesNotExist:
        return render('asset_list')    
    if request.method == 'POST':
        form = AssetImageForm(request.POST, request.FILES, instance=AssetImage)
        if form.is_valid():
            return(render, "asset_list")
        return render('update_asset.html', form=AssetImageForm )
    
class ImagesJson(BaseDatatableView):
    """returns json response with all info about images"""
    model = AssetImage
    columns = ['id', 'asset', 'image'] 
    order_columns = ['id', 'asset', 'image'] 
    print(AssetImage.objects.all())
    def render_column(self, row, column):    
        return super().render_column(row, column)  
 
    def get_initial_queryset(self):
        return self.model.objects.all()

class ImageListView(TemplateView):  
    """associated with image json"""
    template_name = 'images.html'
          