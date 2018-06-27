from django.http import HttpResponse
from django.shortcuts import render
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required

def index(request):
    #return HttpResponse("Hello, world")
    return render(request,
                  'twitter/index.html')

@login_required
def top_page(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)

    return render(request,'twitter/top.html',{'user': user})