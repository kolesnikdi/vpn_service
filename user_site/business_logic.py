from urllib.parse import urlparse, urlunparse
from requests import get, options, head, post, put, patch, delete
from knox.auth import TokenAuthentication
from rest_framework.exceptions import NotFound, NotAuthenticated


def remake_links(soup, site):
    site_url = urlparse(site.site_url)
    for tag in soup.find_all(href=True):
        if all((
            tag['href'].startswith(('http:', 'https:')),
            site_url.netloc in tag['href'],
            not any(domain in tag['href'] for domain in ['www.', 'm.', 't.'])
                )):
            parsed_url = urlparse(tag['href'])
            tag['href'] = urlunparse(('http', f'localhost:8000/{site.name}/{parsed_url.netloc}',
                                      parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))

        elif tag['href'].startswith('/'):
            parsed_url = urlparse(tag['href'])
            tag['href'] = urlunparse((site_url.scheme, site_url.netloc,
                                      parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))

    for tag in soup.find_all(src=True):
        if all((
                tag['src'].startswith(('http:', 'https:')),
                site_url.netloc in tag['src'],
                not any(domain in tag['src'] for domain in ['www.', 'm.', 't.'])
        )):
            parsed_url = urlparse(tag['src'])
            tag['src'] = urlunparse(('http', f'localhost:8000/{site.name}/{parsed_url.netloc}',
                                     parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))

        elif tag['src'].startswith('/'):
            parsed_url = urlparse(tag['src'])
            tag['src'] = urlunparse((site_url.scheme, site_url.netloc, parsed_url.path, parsed_url.params,
                                     parsed_url.query, parsed_url.fragment))
    return soup


def count_site_data(site, request, content):
    if request.body:
        output_size = len(request.body)
    else:
        output_size = len(request.build_absolute_uri().encode('utf-8'))
    site.statistics.clicks_number += 1
    site.statistics.data_size += (output_size + len(content))
    site.statistics.save()
    print(site.statistics)


def get_method(request):
    request_method = {
        'GET': get,
        'POST': post,
        'PUT': put,
        'PATCH': patch,
        'DELETE': delete,
        'HEAD': head,
        'OPTIONS': options,
    }
    return request_method.get(request.method)


def authenticate_and_get_site(request, name):
    auth = TokenAuthentication()
    try:
        user, _ = auth.authenticate(request)
    except Exception:
        raise NotAuthenticated()
    if not user.is_authenticated:
        raise NotAuthenticated()
    try:
        return user.user_sites.get(name=name)
    except Exception:
        raise NotFound()
