from django.conf.urls import url, include
from school import endpoints

urlpatterns = [
    url(r'^api/', include(endpoints)),
    url(r'^api/auth/', include('knox.urls')),
]
