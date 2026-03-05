from django.http import HttpResponse

def index(request):
    return HttpResponse(
        "Hello, Serhii !!!."
    )
def page(request):
    return HttpResponse(
        "My first page !!!."
    )