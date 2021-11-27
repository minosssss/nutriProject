from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from accounts.models import Standard
from upload.detection.imageDetection import imageDetection
from upload.decorator import check_user, ownership_user
from upload.forms import UserUploadForm, UserEatenForm, ServedForm
from upload.models import Upload, UploadResult, FoodBio

user_required = [login_required, check_user]

@method_decorator(login_required, 'post')
class UploadView(CreateView):
    model = Upload
    form_class = UserUploadForm
    template_name = 'upload/main.html'

    def get_food(self):
        imgURL = settings.MEDIA_URL
        img = f"{imgURL}{self.object.image}"
        food = imageDetection(settings.MEDIA_ROOT_URL + img)
        return food

    def form_valid(self, form):
        temp_upload = form.save(commit=False)
        temp_upload.user = self.request.user
        temp_upload.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('upload:temp',kwargs={'pk':self.object.pk})


def notice_delete_view(request, pk):
    temp_upload = Upload.objects.get(id=pk)
    if temp_upload.user == request.user or request.user.level == '0':
        temp_upload.delete()
        return redirect("upload:main")

@method_decorator(user_required,'get')
@method_decorator(user_required,'post')
class UploadTempView(TemplateView):
    template_name = 'upload/temp.html'
    queryset = Upload.objects.all()
    pk_url_kwargs = 'pk'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        return queryset.filter(pk=pk).first()

    def get(self, request, *args, **kwargs):
        upload = self.get_object()
        if not upload:
            raise Http404('invalid article_id')

        ctx = {
            'pk': upload.pk,
            'view': self.__class__.__name__,
            'data': upload,
        }
        # context = super().get_context_data(**kwargs)
        food = self.get_food()
        date = UserEatenForm()
        serve = ServedForm()
        ctx['food'] = food
        ctx['date'] = date
        ctx['serve'] = serve
        return self.render_to_response(ctx)

    def get_food(self):
        imgURL = settings.MEDIA_URL
        img = f"{imgURL}{self.get_object().image}"
        food = imageDetection(settings.MEDIA_ROOT_URL + img)
        return food


    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_n_code = user.n_code  # nutri 정보 불러오기 위한 n_code 확인

        # 유저 하루 영양소기준
        user_nutri_data = Standard.objects.values('carb', 'prot', 'fat', 'sodium').get(n_code=user_n_code)
        # 유저 하루 열량
        user_carb = user_nutri_data['carb']
        user_prot = user_nutri_data['prot']
        user_fat = user_nutri_data['fat']
        user_sodium = user_nutri_data['sodium']
        user_cal = user.proper_cal

        food_list = self.get_food()
        data = self.request.POST['eaten_dt']
        upload_id = self.get_object().pk
        if UploadResult.objects.filter(upload_id=upload_id).first():
            raise Http404('이미 존재 합니다.')
        else:
            pass
        for n in range(len(food_list)):
            get_food = food_list[n]
            food_date = FoodBio.objects.values('cal', 'carb', 'prot', 'fat', 'sodium').get(food_nm=get_food)

            result = UploadResult.objects.create(food_id=FoodBio.objects.get(food_nm=get_food),
                                                 upload_id=Upload.objects.get(id=upload_id),
                                                 user_id=user.pk,
                                                 eaten_dt=data,
                                                 cal=food_date['cal'],
                                                 carb=food_date['carb'],
                                                 prot=food_date['prot'],
                                                 fat=food_date['fat'],
                                                 sodium=food_date['sodium'])

            result.save()

        return HttpResponseRedirect(reverse('upload:detail',kwargs=({'eaten_dt':data})))




@method_decorator(ownership_user,'get')
class UploadResultView(TemplateView):
    template_name = 'upload/detail.html'
    queryset = UploadResult.objects.all()
    pk_url_kwargs = 'eaten_dt'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        dt = self.kwargs.get(self.pk_url_kwargs)
        user = self.request.user.pk
        result = queryset.filter(eaten_dt=dt,user_id=user).all()

        if not result:
            raise Http404('invalid pk')
        return result

    def get(self, request, *args, **kwargs):
        result = self.get_object()

        ctx = {
            'result': result
        }
        return self.render_to_response(ctx)