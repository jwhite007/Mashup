import re


def resolve_path(path):
    urls = [(r'^$', cities),
            (r'^cities/(city)$', city)]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    raise NameError


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]


def cities():
    all_cities = [key for key in earthquake()]
    mean_intensity = [earthquake()['city'][0] for city in all_cities]
    body = ['<h1>West Coast City Earthquake Data</h1>', '<ul>']
    item_template = ('<li><strong><a href="/cities/{city}">{city}</a></strong>'
                     '(Mean Intensity: {mean_intensity})</li>')
    for city in all_cities:
        body.append(item_template.format(**city,**mean_intensity)))
    body.append('</ul>')
    return '\n'.join(body)


def city(city):
    page = """
<h1>{city}</h1>
<table>
    <tr><th>Distance from {city}:</th><td>{city_dict[{city}][1]['1'][1]}</td></tr>
    <tr><th>Depth Distance from {city}:</th><td>{city_dict[{city}][1]['1'][2]}</td></tr>
    <tr><th>Magnitude:</th><td>{city_dict[{city}][1]['1'][3]}</td></tr>
    <tr><th>Intensity:</th><td>{city_dict[{city}][1]['1'][4]}</td></tr>
</table>
<a href="/">Back to the list</a>
"""
    city = DB.title_info(city)
    if city is None:
        raise NameError
    return page.format(**city)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
