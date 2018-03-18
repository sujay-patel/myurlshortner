from django.shortcuts import render_to_response, get_object_or_404
import random, string, json
from shortenersite.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

val = URLValidator()

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('shortenersite/index.html', c)

@csrf_exempt
def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id) # get object, if not found return 404 error
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.httpurl)


@csrf_exempt
def clear_database(request):
        url = Urls.objects.all().delete()
        response_data = {}
        response_data['status'] = "OK"
        response_data['status_codes'] = [200]
        return HttpResponse(json.dumps(response_data),  content_type="application/json")

@csrf_exempt
def shorten_url(request):
    json_data = json.loads(request.body.decode("utf-8"))
    url =  json_data['long_url']
    try:
        val(url)
        if not (url == ''):
            short_id = get_short_code()
            b = Urls(httpurl=url, short_id=short_id)
            b.save()

            response_data = {}
            response_data['short_url'] = settings.SITE_URL + "/" + short_id
            response_data['status'] = "OK"
            response_data['status_codes'] = []
            return HttpResponse(json.dumps(response_data),  content_type="application/json")
        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["INVALID_URLS"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    except ValidationError:
        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["INVALID_URLS"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def lengthen_url(request):
    json_data = json.loads(request.body.decode("utf-8"))
    url =  json_data['short_url']
    try:
        val(url)
        if not (url == ''):
            extracted_short_id = url.rsplit('/', 1)[-1]

            b = Urls.objects.get(short_id=extracted_short_id)
            response_data = {}
            response_data['long_url'] = b.httpurl
            response_data['status'] = "OK"
            response_data['status_codes'] = []
            return HttpResponse(json.dumps(response_data),  content_type="application/json")

        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    except ObjectDoesNotExist:
        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except ValidationError:
        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["INVALID_URLS"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def shorten_urls(request):
    json_data = json.loads(request.body.decode("utf-8"))
    urls =  json_data['long_urls']

    short_urls_dict = {}
    if not (len(urls) < 1):
        response_data = {}
        for i in range(len(urls)):
            try:
                val(urls[i])
                short_id = get_short_code()
                b = Urls(httpurl=urls[i], short_id=short_id)
                b.save()
                short_urls_dict[urls[i]] = settings.SITE_URL + "/" + short_id
            except ValidationError:
                response_data = {}
                response_data['invalid_urls'] = "["+ urls[i] +"]"
                response_data['status'] = "FAILED"
                response_data['status_codes'] = ["INVALID_URLS"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        print(short_urls_dict)
        response_data['short_urls'] =  short_urls_dict
        response_data['status'] = "OK"
        response_data['status_codes'] = []
        response_data['invalid_urls'] = []
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    response_data = {}
    response_data['status'] = "FAILED"
    response_data['status_codes'] = ["INVALID_URLS"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def lengthen_urls(request):
    json_data = json.loads(request.body.decode("utf-8"))
    urls =  json_data['short_urls']

    long_urls_dict = {}
    if not (len(urls) == 0):
        response_data = {}
        for i in range(len(urls)):
            try:
                val(urls[i])
                extracted_short_id = urls[i].rsplit('/', 1)[-1]
                b = Urls.objects.get(short_id=extracted_short_id)
                long_urls_dict[urls[i]] = b.httpurl
            except ObjectDoesNotExist:
                response_data = {}
                response_data['invalid_urls'] = "["+ urls[i] +"]"
                response_data['status'] = "FAILED"
                response_data['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            except ValidationError:
                response_data = {}
                response_data['invalid_urls'] = "["+ urls[i] +"]"
                response_data['status'] = "FAILED"
                response_data['status_codes'] = ["INVALID_URLS"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")

        response_data['long_urls'] =  long_urls_dict
        response_data['status'] = "OK"
        response_data['status_codes'] = []
        response_data['invalid_urls'] = []
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    response_data = {}
    response_data['status'] = "FAILED"
    response_data['status_codes'] = ["INVALID_URLS"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def count_access(request):
    json_data = json.loads(request.body.decode("utf-8"))
    url =  json_data['short_url']
    try:
        val(url)
        if not (url == ''):
            extracted_short_id = url.rsplit('/', 1)[-1]
            b = Urls.objects.get(short_id=extracted_short_id)
            response_data = {}
            response_data['count'] = b.count
            response_data['status'] = "OK"
            response_data['status_codes'] = []
            return HttpResponse(json.dumps(response_data),  content_type="application/json")
        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    except ObjectDoesNotExist:
        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except ValidationError:
        response_data = {}
        response_data['status'] = "FAILED"
        response_data['status_codes'] = ["INVALID_URLS"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_short_code():
    length = 8
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return short_id
