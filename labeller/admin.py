from django.contrib import admin
from .models import Course, Lesson

class CourseAdmin(admin.ModelAdmin):
    exclude = ('creator',)  # Exclude the creator field from the form

    def save_model(self, request, obj, form, change):
        if not change:  # Only set creator during the first save.
            obj.creator = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)