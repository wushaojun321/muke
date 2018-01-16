# encoding:utf8

from django.conf.urls import url, include

from views import UserInfoBaseView, UserCourseView, UserFavCourseView, UserFavOrgView, UserFavTeacherView, UserMessageView, UserImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView


urlpatterns = [
    url(r'^info/$', UserInfoBaseView.as_view(), name='info'),
    url(r'^course/$', UserCourseView.as_view(), name='user_course'),
    url(r'^fav_course/$', UserFavCourseView.as_view(), name='fav_course'),
    url(r'^fav_org/$', UserFavOrgView.as_view(), name='fav_org'),
    url(r'^fav_teacher/$', UserFavTeacherView.as_view(), name='fav_teacher'),
    url(r'^message/$', UserMessageView.as_view(), name='message'),
    url(r'^image/upload/$', UserImageUploadView.as_view(), name='image_upload'),
    url(r'^update/password/$', UpdatePwdView.as_view(), name='update_password'),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

]