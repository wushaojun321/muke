# encoding:utf8
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from forms import LoginForm, RegisterForm, ForgetPwdForm, UserInfoForm, UserImageForm, ModifyPwdForm
from utils.email_send import send_register_email
from utils.mixin_uitls import LoginRequiredMixin

# Create your views here.


class IndexView(View):

    def get(self, request):
        banners = Banner.objects.all()
        banner_courses = Course.objects.all()[:3]
        courses = Course.objects.all()[3:]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'banners':banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
            })


class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    '''
    用户登录
    '''

    def get(self, request):
        banners = Banner.objects.all()
        next_url = request.GET.get('next', '')
        print next_url
        return render(request, 'login.html', {
            'next_url': next_url,
            'banners': banners})

    def post(self, request):

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')

            user = authenticate(username=user_name, password=pass_word)
            if user:
                login(request, user)
                next_url = request.POST.get('next', '')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '账号或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    '''
    登出
    '''

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    '''
    注册
    '''

    def get(self, request):
        banners = Banner.objects.all()
        register_form = RegisterForm()
        return render(request, 'register.html', {
            'register_form': register_form,
            'banners': banners,
            })

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            new_user = UserProfile()
            new_user.email = email
            new_user.username = email
            new_user.password = make_password(pass_word)
            new_user.is_active = False
            new_user.save()
            send_register_email(email)
            return render(request, 'login.html')
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    '''
    激活
    '''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'index.html')
        else:
            return render(request, 'active_fail.html', {})


class ForgetPwdView(View):
    '''
    忘记密码
    GET：向用户提供重置密码的表单
    POST：接受用户发送的需要修改密码的账户，并发送邮件
    '''

    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)

        if forget_form.is_valid():
            email = request.POST.get('email', '')
            user = UserProfile.objects.filter(email=email)
            if user:
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    '''
    重置密码
    获取并判断用户GET请求中所带code是否为正确的
    '''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):

    def post(self, request):
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password2 != password1:
            return render(request, 'password_reset.html', {'email': email, 'msg': '两次密码不一致'})
        elif len(password1) < 6:
            return render(request, 'password_reset.html', {'email': email, 'msg': '密码太短'})
        else:
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)
            user.save()
            return render(request, 'login.html')


class UserInfoBaseView(LoginRequiredMixin, View):

    def get(self, request,):

        return render(request, 'usercenter-base.html',)

    def post(self, request):
        userinfoform = UserInfoForm(request.POST, instance=request.user)
        if userinfoform.is_valid():
            userinfoform.save()
            return HttpResponse('{"status":"success","msg":"保存成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(userinfoform.errors), content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):

    def get(self, request,):
        courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {'user_courses': courses})


class UserFavCourseView(LoginRequiredMixin, View):

    def get(self, request,):
        user_fav_course = UserFavorite.objects.filter(
            user=request.user, fav_type=1)
        fav_course_list = [user_fav.fav_id for user_fav in user_fav_course]
        course_list = Course.objects.filter(id__in=fav_course_list)
        return render(request, 'usercenter-fav-course.html', {'course_list': course_list})


class UserFavOrgView(LoginRequiredMixin, View):

    def get(self, request,):
        user_fav_org = UserFavorite.objects.filter(
            user=request.user, fav_type=2)

        fav_org_list = [user_fav.fav_id for user_fav in user_fav_org]
        org_list = CourseOrg.objects.filter(id__in=fav_org_list)
        return render(request, 'usercenter-fav-org.html', {'org_list': org_list})


class UserFavTeacherView(LoginRequiredMixin, View):

    def get(self, request,):
        user_fav_teacher = UserFavorite.objects.filter(
            user=request.user, fav_type=3)
        fav_teacher_list = [user_fav.fav_id for user_fav in user_fav_teacher]
        teacher_list = Teacher.objects.filter(id__in=fav_teacher_list)
        return render(request, 'usercenter-fav-teacher.html', {'teacher_list': teacher_list})


class UserMessageView(LoginRequiredMixin, View):
    '''
    用户消息
    '''

    def get(self, request):
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        all_messages = UserMessage.objects.filter(user=request.user.id)
        p = Paginator(all_messages, 3, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'messages': messages})


class UserImageUploadView(View):

    def post(self, request):
        userimageform = UserImageForm(
            request.POST, request.FILES, instance=request.user)
        if userimageform.is_valid():
            userimageform.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            logout(request)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(View):
    '''
    个人中心修改邮箱第一步，接受新邮箱，并发送包含验证码的邮件
    '''

    def get(self, request):
        email = request.GET.get('email', '')
        if email:
            if UserProfile.objects.filter(email=email):
                return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
            else:
                send_register_email(email, 'update_email')
                return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"failure"}', content_type='application/json')


class UpdateEmailView(View):
    '''
    用户中心修改邮箱第二部，验证验证码，保存新邮箱
    '''

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email'):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

