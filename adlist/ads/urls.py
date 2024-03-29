from django.urls import path, reverse_lazy
from . import views
app_name='ads'
urlpatterns = [
    path('', views.AdListView.as_view()),
    path('ads/', views.AdListView.as_view(), name='ads'),
    path('ads/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/create',
        views.AdCreateView.as_view(success_url=reverse_lazy('ads:ads')), name='ad_create'),
    path('ads/<int:pk>/update',
        views.AdUpdateView.as_view(success_url=reverse_lazy('ads:ads')), name='ad_update'),
    path('ads/<int:pk>/delete',
        views.AdDeleteView.as_view(success_url=reverse_lazy('ads:ads')), name='ad_delete'),
    path('ad_picture1/<int:pk>', views.stream_file1, name='ad_picture1'),
    path('ad_picture2/<int:pk>', views.stream_file2, name='ad_picture2'),
    path('ad/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='ad_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads:ads')), name='ad_comment_delete'),
]
