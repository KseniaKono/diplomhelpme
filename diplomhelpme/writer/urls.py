from django.urls import path, re_path
from . import views


urlpatterns = [
                path('', views.index, name='index'),
                re_path(r'^books/$', views.ContentListView.as_view(), name='books'),
                re_path(r'^users/$', views.UserListView.as_view(), name='users'),
    re_path(r'^top/$', views.top_contents, name='top_contents'),
    re_path(r'^book/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='writer-user-detail'),
    re_path(r'^content/create/$', views.ContentCreate.as_view(), name='content_create'),
    re_path(r'^content/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/update/$', views.ContentUpdate.as_view(), name='content_update'),
    re_path(r'^content/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.ContentDelete.as_view(), name='content_delete'),
    re_path(r'^register/$', views.register_user, name='register'),
    re_path(r'^book/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
            views.contentdetail, name='contentdetail'),
    re_path(r'^comment/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/delete/$', views.delete_comment, name='delete_comment'),
    re_path(r'^content/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/like/$', views.ContentLike.as_view(), name='like_content'),
    re_path(r'^profile/(?P<pk>\d+)$', views.profile, name='profile'),
    path('check_text/', views.check_text, name='check_text'),
]