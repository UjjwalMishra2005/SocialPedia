from .models import photo
from django.contrib import messages
def user_photo(request):
    if request.user.is_authenticated:

        try:           
            photo_rec = photo.objects.get(user = request.user)
        except photo.DoesNotExist:
            photo_rec = None
    else:
        photo_rec = None


    return {"photo":photo_rec}                 

    