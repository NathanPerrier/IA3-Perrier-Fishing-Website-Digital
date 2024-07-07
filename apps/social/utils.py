

def get_image_urls(request):
    file_urls = request.session.get('file_urls')
    request.session.pop('file_urls', None)
    request.session.save()
    
    return file_urls    

def post_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'user_profile__user__username__icontains'
    }
    for key in request.GET:
        if request.GET.get(key) and key != 'page':
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string
