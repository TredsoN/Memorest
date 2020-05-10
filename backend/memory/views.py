import os

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone

from backend import settings
from memory.models import Image, Memory, Music


def a(request):
    return render(request,"a.html")

def imgViews(request):
    with transaction.atomic():
        file_img = request.FILES.get('files')
        memoryid=request.POST.get('memoryid')
        memory = Memory.objects.get(id=memoryid)
        sign = file_img.name.split('.')[-1]
        print(sign)
        if sign == 'jpg' or sign == 'png' or sign == 'gif':
            filename, full_filename = save_image(file_img)
            Image.objects.create(image=filename, memoryid=memoryid)
            memory.picture+=filename+','
        elif sign == 'mp3' or sign == 'wav':
            filename, full_filename = save_image(file_img)
            Music.objects.create(music=filename, memoryid=memoryid)
            memory.audio+=filename+','
        else:
            return
            # return HttpResponse('error')
        memory.save()
        return HttpResponse('{"status":"success"}')

def save_image(files):
    sign = files.name.split('.')[-1]
    filename = "%s.%s" % (timezone.now().strftime('%Y%m%d%H%M%S%f'), sign)
    full_filename=''
    if sign == 'jpg' or sign == 'png' or sign == 'gif':
        full_filename = "%s/%s" % (os.path.join(settings.MEDIA_ROOT, 'image'), filename)
    elif sign == 'mp3' or sign == 'wav':
        full_filename = "%s/%s" % (os.path.join(settings.MEDIA_ROOT, 'music'), filename)
    with open(full_filename, 'wb+') as destination:
        for chunk in files.chunks():
            destination.write(chunk)
    return filename, full_filename