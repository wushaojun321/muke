# encoding:utf8
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from models import Course, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_uitls import LoginRequiredMixin
# Create your views here.


class CourseListView(View):

    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        keywords = request.GET.get('keywords','')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))
        hot_courses = all_courses.order_by('-click_num')[:3]
        sort = request.GET.get('sort', '')

        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_num')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):

    def get(self, request, course_id):
        has_fav_course = False
        has_fav_org = False
        course = Course.objects.get(id=int(course_id))
        # 每点击一次，此课程的点击数加1
        course.click_num += 1
        course.save()
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(
                    user_id=request.user.id,
                    fav_id=int(course_id),
                    fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(
                    user_id=request.user.id,
                    fav_id=int(course.org.id),
                    fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        relate_courses = Course.objects.filter(tag=course.tag)[:2]

        return render(request, 'course-detail.html', {
            'course': course,
            'has_fav_org': has_fav_org,
            'has_fav_course': has_fav_course,
            'relate_courses': relate_courses,
        })


class CourseVideoView(LoginRequiredMixin, View):
    '''
    点击学习课程后进入此视图，向用户展示课程章节等
    '''

    def get(self, request, course_id=5):
        course = Course.objects.get(id=int(course_id))
        relate_courses = Course.objects.filter(tag=course.tag)[:2]

        #如果用户没有学习过此课程，则在数据库UserCourse中添加
        if not UserCourse.objects.filter(course=course, user=request.user):
            new_user_course = UserCourse()
            new_user_course.user = request.user
            new_user_course.course = course
            new_user_course.save()

        #课程学习人数+1
        course.students += 1
        course.save()

        return render(request, 'course-video.html', {
            'course': course,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):

    def get(self, request, course_id=5):
        #取出课程对象
        course = Course.objects.get(id=int(course_id))

        #根据课程对象取出相应评论
        all_comments = course.get_course_comment().order_by('-add_time')

        #取出学习此课程的用户学习的其他课程:先根据此课程id取出学习此课程的全部用户id，然后根据用户id取出这一批用户学习的所有课程
        user_ids = [usercourse.user.id for usercourse in UserCourse.objects.filter(course=course)]
        course_ids = [usercourse.course.id for usercourse in UserCourse.objects.filter(user_id__in=user_ids)]


        relate_courses = Course.objects.filter(tag=course.tag)[:2]
        return render(request, 'course-comment.html', {
            'course': course,
            'relate_courses': relate_courses,
            'all_comments': all_comments,
        })


class CourseAddCommentView(LoginRequiredMixin, View):
    '''
    课程评论，用来处理ajax请求
    '''
    def post(self, request):
        #判断评论内容是否为空
        content = request.POST.get('content', '')
        if not content:
            return HttpResponse('{"status":"fail", "msg":"评论内容为空"}', content_type='application/json')
        #判断用户是否登录
        if request.user.is_authenticated():
            #如果登录，将评论数据保存至数据库
            course_id = request.POST.get('course_id', 0)
            course_comment = CourseComments()
            course_comment.comments = content
            course_comment.user = request.user
            course_comment.course = Course.objects.get(id=int(course_id))
            course_comment.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            #如果未登录，返回失败
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')


class CoursePlayView(LoginRequiredMixin, View):

    def get(self, request, video_id=5):
        video = Video.objects.get(id=int(video_id))

        course = video.lesson.course

        relate_courses = Course.objects.filter(tag=course.tag)[:2]
        return render(request, 'course-play.html', {
            'course': course,
            'relate_courses': relate_courses,
            'video':video,
        })


        