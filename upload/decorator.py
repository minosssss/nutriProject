from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from accounts.models import User
from upload.models import Upload, UploadResult


def check_user(func):
    def decorated(request,*args,**kwargs):
        upload = Upload.objects.get(pk=kwargs['pk'])
        if request.user.pk == None:
            messages.info(request, "Please Login!")
            return redirect('accounts:login')

        elif request.user.pk != upload.user.pk:
            messages.info(request, "You can't see T.T")
            return redirect('upload:main')

        return func(request, *args, **kwargs)
    return decorated

def ownership_user(func):
    def decorated(request,*args,**kwargs):
        user = request.user.pk
        search = UploadResult.objects.filter(user_id=user,eaten_dt=kwargs['eaten_dt'])
        if user == None:
            messages.info(request, "Please Login!")
            return redirect('accounts:login')
        if len(search) == 0:
            messages.info(request, "Page not found.")
            return redirect('upload:main')
        return func(request, *args, **kwargs)
    return decorated