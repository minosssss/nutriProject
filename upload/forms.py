from django.forms import ModelForm
from upload.models import Upload, UploadResult


class UserUploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ['image', 'mealtimes']
