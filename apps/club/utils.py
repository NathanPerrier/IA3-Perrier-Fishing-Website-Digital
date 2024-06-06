def member_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'username__icontains'
    }
    for key in request.GET:
        if request.GET.get(key) and key != 'page':
            try:
                filter_string[filter_mappings[key]] = request.GET.get(key)
            except KeyError: pass
            
    return filter_string