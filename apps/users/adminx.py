#encoding:utf8
import xadmin
from xadmin import views

from models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True


class GlobalSetting(object):
    #设置base_site.html的Title
    site_title = '小武的网站'
    #设置base_site.html的Footer
    site_footer  = '小武的网站'
    menu_style = 'accordion'



class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_time', 'send_time', ]
    search_fields = ['code', 'email', 'send_time',]
    list_filter = ['code', 'email', 'send_time', 'send_time', ]

class BannerAdmin(object):
    list_display = ['title', 'img','url','index', 'add_time']
    search_fields = ['title', 'img','url','index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
