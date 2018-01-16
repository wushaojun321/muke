# encoding:utf8
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg


class LessonInline(object):

    model = Lesson
    # 显示的表，可以用来添加数据
    extra = 1


class CourseResourceInline(object):

    model = CourseResource
    extra = 1


class CourseAdmin(object):

    # 在点击数据表时显示的列
    list_display = ['name', 'degree', 'learn_times', 'students',
                    'fav_nums', 'image', 'click_num', 'add_time', 'org', 'category', 'tag', 'teacher', 'get_lesson_nums']

    # 可以搜索的列
    search_fields = ['name', 'desc', 'detail', 'degree',
                     'learn_times', 'students', 'fav_nums', 'image', 'click_num']

    # 过滤器中包含的列
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students','fav_nums', 'image', 'click_num', 'add_time', 'org', 'category', 'tag', 'teacher']

    # 默认排序方法
    ordering = ['-click_num']

    # 在不用点进数据表时就可以修改数据
    list_editable = ['degree']

    # 在一对多关系的一的一方设置此条目，可在xadmin管理页面中显示多的数据
    inlines = [LessonInline, CourseResourceInline]
    def queryset(self):
        '''
        重写的方法，返回的是在xadmin中显示的条目
        '''
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner = False)
        return qs

    def save_models(self):
        obj = self.new_obj
        print 1111111111111111111111111111
        obj.save()
        print obj.name
        print obj.org.name
        org = CourseOrg.objects.get(id=obj.org.id)
        org.course_nums = org.get_courses_nums()
        org.save()


class BannerCourseAdmin(object):
    # 在点击数据表时显示的列
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students','fav_nums', 'image', 'click_num', 'add_time', 'org', 'category', 'tag', 'teacher']

    # 可以搜索的列
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums', 'image', 'click_num']

    # 过滤器中包含的列
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students','fav_nums', 'image', 'click_num', 'add_time', 'org', 'category', 'tag', 'teacher']

    # 默认排序方法
    ordering = ['-click_num']

    # 在一对多关系的一的一方设置此条目，可在xadmin管理页面中显示多的数据
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        '''
        重写的方法，返回的是在xadmin中显示的条目
        '''
        qs = super(BannerCourseAdmin, self).queryset()
        print qs.count()
        qs = qs.filter(is_banner = True)
        print qs.count()
        return qs

class LessonAdmin(object):
    pass


class VideoAdmin(object):
    pass


class CourseResourceAdmin(object):
    pass

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

