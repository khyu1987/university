import csv

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from courses.models import (
    Student,
    Course,
    CourseParticipant
    )
from courses.serializers import (
    StudentSerializer,
    CourseSerializer,
    CourseParticipantAssignSerializer,
    CourseParticipantUnassignSerializer
    )


class StudentsViewSet(viewsets.ModelViewSet):
    """API endpoint that allows viewed in csv"""

    def list(self, request):
        serializer = StudentSerializer(Student.objects.all(), many=True)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.DictWriter(
            response, fieldnames=['full_name', 'courses_assigned', 'courses_completed'])
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        return response


class CoursesViewSet(viewsets.ModelViewSet):
    """API endpoint that allows courses to be viewed, edited and deleted,
       allows to assign/unassign student to course"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def read():
        serializer = CourseSerializer(queryset, many=True)
        return Response(message, status=status.HTTP_200_OK)


    def create(self, request):
        raise PermissionDenied()

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student')
        data = {
            'course': course.id,
            'student': student_id
        }
        serializer = CourseParticipantAssignSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message = {'message': 'Student was assigned to course'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student')
        data = {
            'course': course.id,
            'student': student_id
        }
        serializer = CourseParticipantUnassignSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message = {'message': 'Student was unassigned from course'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CourseParticipantsViewSet(viewsets.ModelViewSet):
#     """API endpoint that allows participants to be created, viewed, edited or deleted."""

#     queryset = CourseParticipant.objects.all()
#     serializer_class = CourseParticipantAssignSerializer
