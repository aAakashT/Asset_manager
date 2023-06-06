from django import forms
from .models import Asset, AssetType, AssetImage

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_name', 'asset_type', 'is_active']

    # def clean_asset(self):
    #     asset = self.cleaned_data['asset']
    #     # if asset <= 0:
    #     #     raise forms.ValidationError("Quantity must be a positive number.")
    #     return asset


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ['asset_type', 'asset_description']

    def clean_asset_type(self):
        asset_type = self.cleaned_data['asset_type']
        return asset_type
    
class AssetImageForm(forms.ModelForm):
    class Meta:
        model = AssetImage
        fields = ['asset', 'image']

    def clean_asset_Image(self):
        asset_image =self.cleaned_data['image']
        return asset_image 