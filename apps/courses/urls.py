# encoding:utf8

from django.conf.urls import url, include

from views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, CourseAddCommentView, CoursePlayView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name="course_video"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comments"),
    url(r'^add_comment/$', CourseAddCommentView.as_view(), name="add_comment"),
    url(r'^play/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name="course_play"),
    
]