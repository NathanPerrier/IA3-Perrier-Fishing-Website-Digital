 

def routes_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'user__username__icontains'
    }
    for key in request.GET:
        if request.GET.get(key) and key != 'page':
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string

def login_log_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'user__username__icontains'
    }
    for key in request.GET:
        if request.GET.get(key) and key != 'page':
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string

def user_visits_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'user__username__icontains'
    }
    for key in request.GET:
        if request.GET.get(key) and key != 'page':
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string