from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile
from django.utils.importlib import import_module

login_url = settings.LOGIN_URL
public_urls = [compile(login_url.lstrip('/'))]
if hasattr(settings,'PUBLIC_URLS'):
    public_urls += [compile(url) for url in settings.PUBLIC_URLS]
if getattr(settings, 'SERVE_STATIC_TO_PUBLIC', True ):
    root_urlconf = import_module(settings.ROOT_URLCONF)

    public_urls.extend([ compile(url.regex)
        for url in root_urlconf.urlpatterns
        if url.__dict__.get('_callback_str') == 'django.views.static.serve'
    ])
public_urls = tuple(public_urls)


class EnforceLoginMiddleware(object):
    """
    Middlware class which requires the user to be authenticated for all urls except
    those defined in PUBLIC_URLS in settings.py. PUBLIC_URLS should be a tuple of regular
    expresssions for the urls you want anonymous users to have access to. If PUBLIC_URLS
    is not defined, it falls back to LOGIN_URL or failing that '/accounts/login/'.
    Requests for urls not matching PUBLIC_URLS get redirected to LOGIN_URL with next set
    to original path of the unauthenticted request.
    Any urls statically served by django are excluded from this check. To enforce the same
    validation on these set SERVE_STATIC_TO_PUBLIC to False.
    """

    def process_request(self, request):
        """
        Redirect anonymous users to login_url from non public urls
        """
        try:
            if request.user.is_anonymous():
                for url in public_urls:
                    if url.match(request.path[1:]):
                        return None
                return HttpResponseRedirect("%s?next=%s" % (login_url, request.path))
        except AttributeError:
            return HttpResponseRedirect("%s?next=%s" % (login_url, request.path))
