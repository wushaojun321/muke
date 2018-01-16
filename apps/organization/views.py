# encoding:utf8
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q


from models import CityDict, CourseOrg, Teacher
from operation.models import UserFavorite
from courses.models import Course
from forms import UserAskForm
# Create your views here.


class OrgView(View):

    def get(self, request):
        all_citys = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        keywords = request.GET.get('keywords','')
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(name__icontains=keywords))
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        city_id = request.GET.get('city', '')
        ct = request.GET.get('ct', '')
        sort = request.GET.get('sort', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        if ct:
            all_orgs = all_orgs.filter(category=ct)

        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            if sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        org_nums = all_orgs.count()

        return render(request, 'org-list.html', {
            'all_citys': all_citys,
            'hot_orgs': hot_orgs,
            'orgs': orgs,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': ct,
            'sort': sort,
        })


class AddUserAskView(View):

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail", "msg":"提交失败"}', content_type='application/json')


class OrgHomeView(View):

    def get(self, request, org_id,):
        try:
            org = CourseOrg.objects.get(id=int(org_id))
        except:
            return render(request, '404.html')
        org.click_nums += 1
        org.save()
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org_id):
                has_fav_org = True
        all_courses = Course.objects.filter(org=int(org.id))[:4]
        all_teachers = Teacher.objects.filter(org=int(org.id))[:3]
        current_page = 'home'
        return render(request, 'org-detail-homepage.html', {
            'org': org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav_org':has_fav_org,
             })


class OrgCourseView(View):

    def get(self, request, org_id,):
        try:
            org = CourseOrg.objects.get(id=int(org_id))
        except:
            return render(request, '404.html')
        all_courses = Course.objects.filter(org=int(org.id))
        current_page = 'course'
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 4, request=request)
        courses = p.page(page)
        return render(request, 'org-detail-course.html', {
            'org': org,
            'courses': courses,
            'current_page': current_page, })


class OrgTeacherView(View):

    def get(self, request, org_id,):
        try:
            org = CourseOrg.objects.get(id=int(org_id))
        except:
            return render(request, '404.html')
        all_teachers = Teacher.objects.filter(org=int(org.id))
        current_page = 'teacher'

        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'all_teachers': all_teachers,
            'current_page': current_page, })


class OrgDescView(View):

    def get(self, request, org_id,):
        try:
            org = CourseOrg.objects.get(id=int(org_id))
        except:
            return render(request, '404.html')
        current_page = 'asdddd'

        return render(request, 'org-detail-desc.html', {
            'org': org,
            'current_page': current_page, })


class AddFavView(View):

    def update_fav_num(self, fav_type, fav_id, operate_type):
        if operate_type == 'add':
            if fav_type == '1':
                course = Course.objects.get(id=fav_id)
                course.fav_nums += 1
                course.save()
            elif fav_type == '2':
                org = CourseOrg.objects.get(id=fav_id)
                org.fav_nums += 1
                org.save()
            elif fav_type == '3':
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums += 1
                teacher.save()
        if operate_type == 'sub':
            if fav_type == '1':
                course = Course.objects.get(id=fav_id)
                course.fav_nums -= 1
                course.save()
            elif fav_type == '2':
                org = CourseOrg.objects.get(id=fav_id)
                org.fav_nums -= 1
                org.save()
            elif fav_type == '3':
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums -= 1
                teacher.save()

    def post(self, request):
        fav_type = request.POST.get('fav_type', 0)
        fav_id = request.POST.get('fav_id', 0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(
            user=request.user, fav_type=int(fav_type), fav_id=int(fav_id))
        if exist_records:
            self.update_fav_num(fav_type=fav_type, fav_id=fav_id, operate_type='sub')
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            if int(fav_type) > 0 and int(fav_id) > 0:
                self.update_fav_num(fav_type=fav_type, fav_id=fav_id, operate_type='add')
                user_fav = UserFavorite()
                user_fav.fav_type = int(fav_type)
                user_fav.fav_id = int(fav_id)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):

    def get(self, request):
        # 取出所有老师
        all_teachers = Teacher.objects.all()

        keywords = request.GET.get('keywords','')
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords) | Q(work_company__icontains=keywords))
        # 老师总数目
        teachers_count = all_teachers.count()

        # 从前端返回的GET请求里获取sort，可能为'hot'和''，如果未hot则按照点击数排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        # 取出热门老师，这里是按照点击数排序
        hot_teachers = all_teachers.order_by('-click_nums')[:3]
        # 将老师的对象与相应的次序组装，返回由多个包含两个元素的元组组成的列表[(teacher1,1),[teacher2,2]...]
        hot_teachers_sort = zip(
            hot_teachers, [i+1 for i in range(hot_teachers.count())])

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'hot_teachers_sort': hot_teachers_sort,
            'teachers_count': teachers_count,
            'sort': sort,
        })


class TeacherDetailView(View):

    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id = int(teacher_id))
        except:
            return render(request, '404.html')

        all_teachers = Teacher.objects.all()
        sorted_teacher = all_teachers.order_by('-click_nums')[:3]
        teacher_courses = teacher.get_courses()

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_type=3, fav_id=teacher.id, user=request.user):
                has_fav_teacher = True
            if UserFavorite.objects.filter(fav_type=2, fav_id=teacher.org.id, user=request.user):
                has_fav_org = True

        return render(request, 'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':teacher_courses,
            'sorted_teacher':sorted_teacher,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
            })

