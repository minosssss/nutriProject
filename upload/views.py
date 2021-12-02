from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, DetailView, ListView

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
        #time = timezone.now().strftime("%Y-%m-%d")
        temp_upload.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('upload:temp',kwargs={'pk':self.object.pk})


@method_decorator(check_user,'get')
class UploadDetailView(TemplateView):
    template_name = 'upload/info.html'
    queryset = Upload.objects.all()
    pk_url_kwargs = 'pk'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        return queryset.filter(pk=pk).first()

    def get(self, request, *args, **kwargs):
        result = self.get_object()
        user = self.request.user

        # 개인 데이터 가져오기 (백분율 구하기 및 페이지에 각 수치 보여주기)
        user_nutri_data = Standard.objects.values('carb', 'prot', 'fat', 'sodium').get(n_code=user.n_code)
        user_carb = user_nutri_data['carb']
        user_prot = user_nutri_data['prot']
        user_fat = user_nutri_data['fat']
        user_sodium = user_nutri_data['sodium']
        user_cal = user.proper_cal

        meal = UploadResult.objects.values('cal','carb','prot','fat','sodium').filter(upload_id=result.id)
        # 업로드ID의 영양정보 가져오기
        bio = []
        for food in meal:
            get_food_bio = food
            bio.append(get_food_bio)

        # 가져온 음식 영양정보 합치기
        total_cal = sum(item['cal'] for item in bio)
        total_carb = sum(item['carb'] for item in bio)
        total_prot = sum(item['prot'] for item in bio)
        total_fat = sum(item['fat'] for item in bio)
        total_sodium = sum(item['sodium'] for item in bio)

        cal_rate = f"{(total_cal / user_cal * 100):.2f}"
        carb_rate = f"{(total_carb / user_carb * 100):.2f}"
        prot_rate = f"{(total_prot / user_prot * 100):.2f}"
        fat_rate = f"{(total_fat / user_fat * 100):.2f}"
        sodium_rate = f"{(total_sodium / user_sodium * 100):.2f}"
        food = self.get_food()
        ctx = {
            'result': result,
            'food':food,
            'user_nutri_data': user_nutri_data,
            'cal_rate': cal_rate,
            'carb_rate': carb_rate,
            'prot_rate': prot_rate,
            'fat_rate': fat_rate,
            'sodium_rate': sodium_rate,
            'total_cal': total_cal,
            'total_carb': total_carb,
            'total_prot': total_prot,
            'total_fat': total_fat,
            'total_sodium': total_sodium,
        }

        return self.render_to_response(ctx)

    def get_food(self):
        imgURL = settings.MEDIA_URL
        img = f"{imgURL}{self.get_object().image}"
        food = imageDetection(settings.MEDIA_ROOT_URL + img)
        return food

@method_decorator(login_required(),'get')
class UploadResultListView(TemplateView):
    template_name = 'upload/list.html'
    queryset = UploadResult.objects.all()

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.request.user.id
        return queryset.filter(user_id=pk).values('eaten_dt').order_by('eaten_dt').distinct()

    def get(self, request, *args, **kwargs):
        eaten_dt = self.get_object()
        ctx = {
            'eaten_dt': eaten_dt
        }
        return self.render_to_response(ctx)

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
        # data = self.request.POST['eaten_dt']
        upload_id = self.get_object().pk
        data = self.get_object().created_at
        if UploadResult.objects.filter(upload_id=upload_id).first():
            raise Http404('이미 존재하는 식단입니다. History를 확인해주세요.')
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

    def get_object_result(self, queryset=None):
        queryset = queryset or self.queryset
        dt = self.kwargs.get(self.pk_url_kwargs)
        user = self.request.user.pk
        result = queryset.filter(eaten_dt=dt,user_id=user).all()

        if not result:
            raise Http404('invalid pk')
        return result

    def get(self, request, *args, **kwargs):
        #요청한 유저 체크
        user = self.request.user
        #[업로드 결과(영양정보)] 유저의 upload_result 가져오기 (URL의 일자만 가져옴)
        result = self.get_object_result()

        #[이미지 정렬_id필터]upload_id (upload_info테이블) 필터
        filter_upload = result.values('upload_id')


        #[이미지정렬] upload_info 의 해당 일자 'mealtimes' 정렬하여 가져오기
        info = Upload.objects.filter(id__in=filter_upload,user_id=user.pk).all().order_by('mealtimes')

        #개인 데이터 가져오기 (백분율 구하기 및 페이지에 각 수치 보여주기)
        user_nutri_data = Standard.objects.values('carb', 'prot', 'fat', 'sodium').get(n_code=user.n_code)
        user_carb = user_nutri_data['carb']
        user_prot = user_nutri_data['prot']
        user_fat = user_nutri_data['fat']
        user_sodium = user_nutri_data['sodium']
        user_cal = user.proper_cal

        #해당일자 영양정보 가져오기
        bio = []
        food_list = result.values('food_id')
        for food in food_list.values('cal', 'carb', 'prot', 'fat', 'sodium'):
            get_food_bio = food
            bio.append(get_food_bio)
        #가져온 음식 영양정보 합치기
        total_cal = sum(item['cal'] for item in bio)
        total_carb = sum(item['carb'] for item in bio)
        total_prot = sum(item['prot'] for item in bio)
        total_fat = sum(item['fat'] for item in bio)
        total_sodium = sum(item['sodium'] for item in bio)

        cal_rate = f"{(total_cal / user_cal * 100):.2f}"
        carb_rate = f"{(total_carb / user_carb * 100):.2f}"
        prot_rate = f"{(total_prot / user_prot * 100):.2f}"
        fat_rate = f"{(total_fat / user_fat * 100):.2f}"
        sodium_rate = f"{(total_sodium / user_sodium * 100):.2f}"

        morning = result.select_related('upload_id').values_list('food_id__food_nm',flat=True).filter(upload_id__mealtimes=1)
        morning_info = morning.values('upload_id__image', 'upload_id').first()
        lunch = result.select_related('upload_id').values_list('food_id__food_nm', flat=True).filter(
            upload_id__mealtimes=2)
        lunch_info = lunch.values('upload_id__image', 'upload_id').first()
        dinner = result.select_related('upload_id').values_list('food_id__food_nm', flat=True).filter(
            upload_id__mealtimes=3)
        dinner_info = dinner.values('upload_id__image', 'upload_id').first()
        dateform = UserEatenForm()


        ctx = {
            'morning':morning,
            'morning_info':morning_info,
            'lunch': lunch,
            'lunch_info':lunch_info,
            'dinner': dinner,
            'dinner_info':dinner_info,
            'result': result,
            'info':info,
            'date': result.first(),
            'user':user,
            'user_nutri_data':user_nutri_data,
            'cal_rate':cal_rate,
            'carb_rate': carb_rate,
            'prot_rate':prot_rate,
            'fat_rate':fat_rate,
            'sodium_rate':sodium_rate,
            'total_cal':total_cal,
            'total_carb': total_carb,
            'total_prot': total_prot,
            'total_fat': total_fat,
            'total_sodium': total_sodium,
            'dateform':dateform
        }

        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        post_date = kwargs['eaten_dt']
        date = self.request.POST['eaten_dt']
        check_date = UploadResult.objects.filter(eaten_dt=date).first()
        if check_date is None:
            messages.info(self.request, "해당 일자에는 데이터가 없습니다.")
            return HttpResponseRedirect(reverse('upload:detail', kwargs=({'eaten_dt': post_date})))
        else:
            return HttpResponseRedirect(reverse('upload:detail',kwargs=({'eaten_dt':date})))