
def is_authenticated(request):
    if 'user' in request.session.keys():
        return True
    return False