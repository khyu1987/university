from django.urls import path, include
from rest_framework import routers

from courses.views import (
    StudentsViewSet,
    CoursesViewSet,
    # CourseParticipantsViewSet
    )

router = routers.DefaultRouter()

router.register('students', StudentsViewSet, base_name='students')
router.register('courses', CoursesViewSet, base_name='courses')
# router.register('participants', CourseParticipantsViewSet, base_name='participants')

urlpatterns = [
	path('', include(router.urls)),
]
