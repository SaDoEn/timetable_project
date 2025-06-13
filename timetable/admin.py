from django.contrib import admin
from .models import Teacher, Subject, Group, TimeSlot, Timetable


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time_slot',)
    search_fields = ('time_slot',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'time_slot', 'subject', 'teacher', 'group', 'room')
    list_filter = ('day_of_week', 'teacher', 'group')
    search_fields = ('subject__name', 'teacher__full_name', 'group__name', 'room')