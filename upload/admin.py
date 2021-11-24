from django.contrib import admin

# Register your models here.

from upload.models import Upload, FoodBio, UploadResult

admin.site.register(Upload)
admin.site.register(FoodBio)
admin.site.register(UploadResult)