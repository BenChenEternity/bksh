from django.contrib import admin
from stuhelper_app import models


# # Register your models here.
# class Empty_ClassroomAdmin(admin.ModelAdmin):
#     list_display = ('location_id', 'building_id', 'floor_id', 'seat_num', 'exam_seat_num', 'classroom_type', 'empty_week', 'empty_day', 'empty_session')
#     search_fields = ('location_id', 'building_id', 'floor_id', 'seat_num', 'exam_seat_num', 'classroom_type')
#     list_filter = ('building_id',)
#     ordering = ('location_id', )


admin.site.register(models.CustomUser)
admin.site.register(models.Empty_Classroom)
admin.site.register(models.Post)
