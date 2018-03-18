from django.conf.urls import include, url
from shortenersite.views import index, redirect_original, shorten_url, lengthen_url, shorten_urls, lengthen_urls, count_access, clear_database

app_name="shortenersite"
urlpatterns = [
    url(r'^$', index, name='home'),
    # for our home/index page

    url(r'^(?P<short_id>\w{8})$', redirect_original, name='redirectoriginal'),
    # when short URL is requested it redirects to original URL

    url(r'^fetch/short-url/$', shorten_url, name='shortenurl'),
    # this will create a URL's short id and return the short URL

    url(r'^fetch/long-url/$', lengthen_url, name='lengthenurl'),
    # this will locate a URL's short id in DB and return the long URL

    url(r'^fetch/short-urls/$', shorten_urls, name='shortenurls'),
    # this will create URL's short id in DB and return the long URL(list form)

    url(r'^fetch/long-urls/$', lengthen_urls, name='lengthenurls'),
    # this will locate URL's short id in DB and return the long URL(list form)

    url(r'^fetch/count/$', count_access, name='countaccess'),

    url(r'^clean-urls$', clear_database, name='cleardatabase'),
]
