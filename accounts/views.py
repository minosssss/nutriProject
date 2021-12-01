
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from . import forms
from .decorator import required
from .models import User, Standard

user_required = [login_required, required]



class LoginView(FormView):

    template_name = "accounts/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("upload:main")

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, user_id=user_id, password=password)
        messages.info(self.request, "Welcome!")
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect('accounts:login')

class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("upload:main")

    def form_valid(self, form):
        temp_user = form.save(commit=False)
        temp_user.n_code = Standard.objects.get(gender=self.request.POST['gender'],
                                                age_category=self.request.POST['age_category'])
        weight = self.request.POST['weight']
        height = self.request.POST['height']
        activity = self.request.POST['activity']
        if self.request.POST['gender'] == 1:
            temp_user.proper_cal \
                = round((66.47 + (13.75 * float(weight)) + (5 * float(height)) - (6.76 * 30))*float(activity))
        else:
            temp_user.proper_cal \
                = round((655.1 + (9.56 * float(weight)) + (1.85 * float(height)) - (4.68 * 30))*float(activity))
        temp_user.save()
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        temp_user.password = make_password(password)
        temp_user.save()
        user = authenticate(user_id=user_id, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

@method_decorator(required, 'get')
class UserMyPageView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accounts/detail.html'


@method_decorator(required, 'get')
@method_decorator(required, 'post')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'accounts/update.html'
    context_object_name = 'target_user'
    form_class = forms.UserUpdateForm


    def form_valid(self, form):
        temp_user = form.save(commit=False)
        weight = self.request.POST['weight']
        height = self.request.POST['height']
        activity = self.request.POST['activity']
        if self.request.POST['gender'] == 1:
            temp_user.proper_cal = round((66.47 + (13.75 * float(weight)) + (5 * float(height)) - (6.76 * 30))*float(activity))
        else:
            temp_user.proper_cal = round((655.1 + (9.56 * float(weight)) + (1.85 * float(height)) - (4.68 * 30))*float(activity))
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        temp_user.password = make_password(password)
        temp_user.save()
        user = authenticate(user_id=user_id, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        messages.info(self.request, "Sucess!")
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})
