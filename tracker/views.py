from google.appengine.api import users
from google.appengine.ext import deferred

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.conf import settings

from tracker.models import Log


def log_access(ip, ua, page):
    """ Save access log"""
    log = Log(ip=ip, ua=ua, page=page)
    log.put()
    return


class BaseView(View):
    """
    Base view combined with google appengine user data
    """    
    
    def render(self, tpl, context={}, **kwargs):

        context.update({
            'user': users.get_current_user(),
            'login_url': users.create_login_url(settings.LOGIN_REDIRECT_URL),
            'logout_url': users.create_logout_url(settings.LOGIN_REDIRECT_URL)
            })
            
        return render_to_response(tpl, context, **kwargs)


class HomePage(BaseView):
    """
    Homepage view.
    """
    template = 'index.html'

    def get(self, request):
        user = users.get_current_user()
        ip = request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT')
        deferred.defer(log_access, ip, ua, 'homepage')
        return self.render(self.template, locals(), context_instance=RequestContext(request))


def plain_page(request):
    """ Plain page view"""
    ip = request.META.get('REMOTE_ADDR')
    ua = request.META.get('HTTP_USER_AGENT')
    deferred.defer(log_access, ip, ua, 'plainpage')
    return HttpResponse(request.META.get('REMOTE_ADDR'))