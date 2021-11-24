from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView

from upload.detection.imageDetection import imageDetection
from upload.decorator import check_user
from upload.forms import UserUploadForm
from upload.models import Upload

user_required = [login_required, check_user]

@method_decorator(login_required, 'post')
class UploadView(CreateView):
    model = Upload
    form_class = UserUploadForm
    template_name = 'upload/main.html'

    def form_valid(self, form):
        temp_upload = form.save(commit=False)
        temp_upload.user = self.request.user
        temp_upload.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('upload:detail',kwargs={'pk':self.object.pk})


    #이미지 및 class_list (음식명) return 추가
# def image_detecttion(request):
#     if request.method == 'POST':
#         form = UserUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             temp_upload = form.save(commit=False)
#             temp_upload.user = request.user
#             temp_upload.save()
#             img_URL = settings.MEDIA_URL
#             img_Field = form.instance.image.name
#             img = f"{img_URL}{img_Field}"
#             print(img)
#             food = imageDetection(settings.MEDIA_ROOT_URL + img)
#             return render(request, 'upload/detail.html', {'food':food})



@method_decorator(user_required, 'get')
class UploadDetailView(DetailView):
    model = Upload
    context_object_name = 'upload_result'
    template_name = 'upload/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imgURL = settings.MEDIA_URL
        img = f"{imgURL}{self.object.image}"
        food = imageDetection(settings.MEDIA_ROOT_URL + img)
        context['food'] = food
        return context


def notice_delete_view(request, pk):
    temp_upload = Upload.objects.get(id=pk)
    if temp_upload.user == request.user or request.user.level == '0':
        temp_upload.delete()
        return redirect("upload:main")