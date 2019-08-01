from rest_framework import serializers

from courses.models import (
    Student,
    Course,
    CourseParticipant
    )


class StudentSerializer(serializers.ModelSerializer):
    """Serialize a student info."""

    courses_assigned = serializers.SerializerMethodField()
    courses_completed = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('full_name', 'courses_assigned', 'courses_completed')

    def get_courses_assigned(self, obj):
        return obj.participants.filter(is_deleted=False).count()

    def get_courses_completed(self, obj):
        return obj.participants.filter(completed=True).count()


class CourseSerializer(serializers.ModelSerializer):
    """Serialize a course info."""

    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('name', 'start_date', 'end_date', 'students_count')

    def get_students_count(self, obj):
        return obj.participants.filter(is_deleted=False).count()


class CourseParticipantAssignSerializer(serializers.ModelSerializer):
    """Serialize a participant info during assigning."""

    def validate(self, data):
        course_id = data.get('course')
        student_id = data.get('student')
        participant = CourseParticipant.objects.filter(
            student=student_id, course=course_id, is_deleted=False).first()
        if participant is not None:
            raise serializers.ValidationError('Student is already assigned to course')
        return data

    def save(self):
        course = self.validated_data.get('course')
        student = self.validated_data.get('student')
        participant = CourseParticipant.objects.filter(
            student=student, course=course, is_deleted=True).first()
        if participant is not None:
            participant.is_deleted = False
            participant.save()
        else:
            CourseParticipant.objects.create(**self.validated_data)

    class Meta:
        model = CourseParticipant
        fields = ('student', 'course', 'completed', 'is_deleted')


class CourseParticipantUnassignSerializer(serializers.ModelSerializer):
    """Serialize a participant info during unassigning."""

    def validate(self, data):
        course_id = data.get('course')
        student_id = data.get('student')
        participant = CourseParticipant.objects.filter(
            student=student_id, course=course_id, is_deleted=False).first()
        if participant is None:
            raise serializers.ValidationError('Student is not assigned to course')
        return data

    def save(self):
        course = self.validated_data.get('course')
        student = self.validated_data.get('student')
        participant = CourseParticipant.objects.get(student=student, course=course)
        participant.is_deleted = True
        participant.save()

    class Meta:
        model = CourseParticipant
        fields = ('student', 'course', 'completed', 'is_deleted')