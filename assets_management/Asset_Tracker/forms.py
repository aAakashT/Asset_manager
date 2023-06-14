from django import forms
from .models import Asset, AssetType, AssetImage

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_name', 'asset_type', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        asset_name = cleaned_data['asset_name']
        asset_type = cleaned_data['asset_type']
        if asset_name and asset_type:
                try:
                    k = type(int(asset_name))
                    raise forms.ValidationError("please check values.")
                except ValueError:
                    return cleaned_data
    

class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ['asset_type', 'asset_description']

    def clean(self):
        cleaned_data = super().clean()
        asset_type = self.cleaned_data['asset_type']
        return cleaned_data
    
class AssetImageForm(forms.ModelForm):
    class Meta:
        model = AssetImage
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data['image']
        asset = cleaned_data['asset']
        if image:
            extension = image.name.split('.')[-1]
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            if extension.lower() not in valid_extensions:
                raise forms.ValidationError("Only JPG, JPEG, PNG, and GIF images are allowed.")

            if image.size > 5 * 1024 * 1024: 
                raise forms.ValidationError("The image size should not exceed 5MB.")

        return cleaned_data