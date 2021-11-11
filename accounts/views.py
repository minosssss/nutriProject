import json

import bcrypt as bcrypt
import generics as generics
from django.contrib.auth import authenticate, login
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.forms import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from . import forms
from accounts.models import User, Standard

def main(request):
    return render(request, 'accounts/main.html')


class SignUpView(FormView):
    model = User, Standard
    template_name = "accounts/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("accounts:main")

    # def form_valid(self, form):
    #     form.save()
    #     user_id = form.cleaned_data.get("user_id")
    #     password = form.cleaned_data.get("password")
    #     user = authenticate(self.request, user_id=user_id, password=password)
    #     if user is not None:
    #         login(self.request, user)
    #     return super().form_valid(form)
    #
    # def post(self, request):
    #     if request.method == "POST":
    #         temp = request.POST.get('n_code')
    #         print(temp)
    #     try:
    #         data = json.loads(request.body)
    #         user_id = data['user_id']
    #         password = data['password']
    #         name = data['name']
    #         height = data['height']
    #         weight = data['weight']
    #         age_category = data['age_category']
    #         gender = data['gender']
    #         activity = data['activity']
    #
    #         user = User.objects.create(
    #             user_id=user_id,
    #             password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),  # hash이후 바로 decode,
    #             name=name,
    #             height=height,
    #             weight=weight,
    #             age_category=age_category,
    #             activity=activity,
    #             gender=gender,
    #             codename=Standard.objects.n_code.filter(Q(gender=gender)),
    #             proper_cal=66.47 + (13.75 * weight) + (5 * height) - (6.76 * 30),
    #         )
    #         print(user)
    #         return JsonResponse({'MESSAGE': 'SUCCESS TO MAKE ACCOUNT'}, status=201)
    #
    #
    #     except:
    #         return render(request, 'accounts/main.html')


# def add_info(request):
#     if request.method == "POST":
#         temp = request.POST.get("n_code")
#         n_code = Standard.all().filter(Q)

