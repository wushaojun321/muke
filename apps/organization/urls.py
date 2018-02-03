#encoding:utf8

from django.conf.urls import url, include

from views import OrgView, AddUserAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView, AddFavView, TeacherListView, TeacherDetailView


urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
    url(r'^teachers/list/$', TeacherListView.as_view(), name="teachers_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]