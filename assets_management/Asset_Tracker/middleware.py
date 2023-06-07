
def user_middleware(get_response):
    
    print("hello")
    print()
    def inner_middleware(request):
        # print(dir(request))
        # print(request)
        response = get_response(request)
        return response
    return inner_middleware
