

def get_image_urls(request):
    file_urls = request.session.get('file_urls')
    request.session.pop('file_urls', None)
    request.session.save()
    
    return file_urls    