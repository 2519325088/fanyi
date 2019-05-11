from  django.conf.urls import url
from . import views

app_name='fanyi'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^fanyia/$',views.fanyia,name='fanyia'),
    url(r'^xiazai/$',views.xiazai,name='xiazai'),
]