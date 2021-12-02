"""nutrition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from upload.views import UploadView, notice_delete_view, UploadTempView, UploadResultView, UploadDetailView, \
    UploadResultListView
from django.conf import settings
from django.conf.urls.static import static

#해당 네임에서 url patterns에 있는 name의 url로 가주세요~!
app_name = "upload"

urlpatterns = [
    path('', UploadView.as_view(), name='main'), #upload
    path('detail/<slug:eaten_dt>', UploadResultView.as_view(), name='detail'),
    path('detail/info/<int:pk>',UploadDetailView.as_view(), name='detail_info'),
    path('temp/<int:pk>/delete/',notice_delete_view, name='delete'),
    path('temp/<int:pk>',UploadTempView.as_view(), name='temp'),
    path('list/',UploadResultListView.as_view(), name='list'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
