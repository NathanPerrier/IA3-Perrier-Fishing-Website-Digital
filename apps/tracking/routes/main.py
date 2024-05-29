from apps.tracking.routes.__init__ import Routes
import time

class TrackURLChangeMiddleware:
    """
    Middleware to track URL changes and time spent on each page.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Before the view (and other middleware) are called.
        previous_url = request.session.get('previous_url')
        current_url = request.get_full_path()
    
        if previous_url != current_url:
            if current_url == '/': request.session.pop('file_urls', None)
            
            previous_time = request.session.get('previous_time')
            if previous_time:
                try:
                    previous_time = float(previous_time)
                except ValueError:
                    # Handle the case where previous_time is not a float
                    previous_time = None
                
            if previous_time:
                time_difference = time.perf_counter() - previous_time
                
                if request.user.is_authenticated:
                    Routes.objects.create(
                        user=request.user, 
                        previous_url=previous_url, 
                        current_url=current_url, 
                        method=request.method,
                        time_spent=time_difference
                    )
                else:
                    Routes.objects.create(
                        ip_address=request.META['REMOTE_ADDR'], 
                        previous_url=previous_url, 
                        current_url=current_url, 
                        method=request.method,
                        time_spent=time_difference
                    )
    
        request.session['previous_url'] = current_url
        request.session['previous_time'] = str(time.perf_counter())
    
        response = self.get_response(request)
        
        request.session.save()
    
        return response