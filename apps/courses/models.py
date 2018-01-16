# encoding:utf8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(
        choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=10)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(
        upload_to='courses/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构')
    category = models.CharField(max_length=300, verbose_name=u'课程类别')
    tag = models.CharField(default='', verbose_name=u'课程标签', max_length=10)
    teacher = models.ForeignKey(Teacher, verbose_name=u'课程老师')
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()
    get_lesson_nums.short_description = '章节数'

    def get_learn_students(self):
        return self.usercourse_set.all()

    def get_course_lesson(self):
        return self.lesson_set.all()

    def get_course_comment(self):
        return self.coursecomments_set.all()

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    '''
    为了在xadmin中将Course表分开管理，创建的model
    '''
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name

        #此参数必须为True，表示不创建新的表
        proxy = True



class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def get_lesson_video(self):
        return self.video_set.all()

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'课程名')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    url = models.CharField(max_length=300, verbose_name=u'视频链接')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(
        upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
