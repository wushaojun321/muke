# encoding:utf8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url=settings.LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        #super并不像它的名字那样，只调用父类的方法，而是调用MRO中，下一个类型的方法。
        print settings
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)