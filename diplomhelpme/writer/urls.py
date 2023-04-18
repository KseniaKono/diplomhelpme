from django.urls import path, re_path
from . import views


urlpatterns = [
                path('', views.index, name='index'),
                re_path(r'^books/$', views.ContentListView.as_view(), name='books'),
                re_path(r'^users/$', views.UserListView.as_view(), name='users'),
    re_path(r'^book/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
            views.ContentDetailView.as_view(), name='content-detail'),
    re_path(r'^book/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='writer-user-detail'),
    re_path(r'^content/create/$', views.ContentCreate.as_view(), name='content_create'),
]