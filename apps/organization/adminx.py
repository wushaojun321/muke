#encoding:utf8
import xadmin

from models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    pass


class CourseOrgAdmin(object):
    pass


class TeacherAdmin(object):
    pass


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)


