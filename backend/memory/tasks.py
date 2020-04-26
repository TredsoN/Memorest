from __future__ import absolute_import, unicode_literals

import time

from celery import shared_task

from memory.models import Memory


# @shared_task
# def cycleprocessing():
#     with open("output.txt", "a") as f:
#         f.write("hello world")
#         f.write("\n")
#     print("hello world")


@shared_task
def memoryLoss():
    aliveMemorys = Memory.objects.exclude(activity=0)#.exclude(recallTime__gte=4)
    deadMemorys = Memory.objects.filter(activity=0)
    for deadMemory in deadMemorys:
        newDeathtime = deadMemory.deathtime + 1
        if newDeathtime > 7:
            deadMemory.delete()
        else:
            deadMemory.deathtime = newDeathtime
            deadMemory.save()
    for aliveMemory in aliveMemorys:
        newActivity = aliveMemory.activity - 10
        if newActivity > 0:
            aliveMemory.activity = newActivity
        else:
            aliveMemory.activity = 0
            aliveMemory.deathtime = 1
        aliveMemory.save()