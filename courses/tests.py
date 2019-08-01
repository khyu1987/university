from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import (
    Student,
    Course,
    CourseParticipant
    )

class CoursesAPITestCase(APITestCase):
    """Test suite for the courses API."""

    def setUp(self):
        """Setup initial data."""

        super().setUp()
        self.student1 = Student.objects.create(
            first_name='Tom1',
            last_name='Bri1',
            email='bri1@gmail.com'
            )
        self.student2 = Student.objects.create(
            first_name='Tom2',
            last_name='Bri2',
            email='bri2@gmail.com'
            )
        self.course1 = Course.objects.create(
            name='Course1',
            description='Lorem1',
            start_date='2019-11-07',
            end_date='2019-11-11'
            )
        self.course2 = Course.objects.create(
            name='Course2',
            description='Lorem2',
            start_date='2019-11-06',
            end_date='2019-11-23'
            )
        self.course_keys = set(['name', 'start_date', 'end_date', 'students_count'])

    def test_courses_list_ok(self):
        """Test that courses list is succesfully read."""

        url = reverse('courses-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Course.objects.all().count())
        self.assertTrue(self.course_keys == set(response.json()[0]))

    def test_courses_list_fail(self):
        """Test that courses list is not read."""

        url = reverse('courses-list')
        response = self.client.get(url)
        keys = set(['name', 'start_date', 'end_date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.json()), Course.objects.all().count()+1)
        self.assertFalse(keys == set(response.json()[0]))

    def test_course_create_fail(self):
        """Test that a course data is not created."""

        url = reverse('courses-list')
        course3 = {
            'name': 'Course3',
            'description': 'Lorem3',
            'start_date': '2019-11-07',
            'end_date': '2019-11-11'
            }
        response = self.client.post(url, course3, format='json')
        message_template = 'You do not have permission to perform this action.'
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(message_template, response.json()['detail'])

    def test_course_read_ok(self):
        """Test that a course data is succesfully read."""

        url = reverse('courses-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.course_keys == set(response.json()))
        self.assertTrue(response.json()['name'] == 'Course1')

    def test_course_update_ok(self):
        """Test that a course data is succesfully updated."""

        url = reverse('courses-detail', kwargs={'pk': 1})
        response = self.client.patch(url, {'name': 'New Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['name'] == 'New Name')

    def test_course_delete_ok(self):
        """Test that a course data is succesfully deleted."""

        url = reverse('courses-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Course.objects.filter(id=1).first() is None)

    def test_student_assign_ok(self):
        """Test that a student is succesfully assigned to course."""

        url = reverse('courses-assign', kwargs={'pk': 1})
        response = self.client.post(url, {'student': 1}, format='json')
        message_template = 'Student was assigned to course'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(message_template, response.json()['message'])
        new_obj = CourseParticipant.objects.filter(
            student=1, course=1, is_deleted=False).filter()
        self.assertTrue(new_obj is not None)

    def test_student_assign_fail(self):
        """Test that a student is not assigned to course."""

        url = reverse('courses-assign', kwargs={'pk': 1})
        response1 = self.client.post(url, {'student': 1}, format='json')
        response2 = self.client.post(url, {'student': 1}, format='json')
        message_template = 'Student is already assigned to course'
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(message_template, response2.json()['non_field_errors'][0])

    def test_student_unassign_ok(self):
        """Test that a student is succesfully unassigned from course."""

        url = reverse('courses-assign', kwargs={'pk': 1})
        response = self.client.post(url, {'student': 1}, format='json')

        url = reverse('courses-unassign', kwargs={'pk': 1})
        response = self.client.post(url, {'student': 1}, format='json')
        message_template = 'Student was unassigned from course'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(message_template, response.json()['message'])
        obj = CourseParticipant.objects.filter(
            student=1, course=1, is_deleted=True).first()
        self.assertTrue(obj is not None)

    def test_student_unassign_fail(self):
        """Test that a student is not unassigned from course."""

        url = reverse('courses-unassign', kwargs={'pk': 1})
        response = self.client.post(url, {'student': 1}, format='json')
        message_template = 'Student is not assigned to course'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(message_template, response.json()['non_field_errors'][0])
        obj = CourseParticipant.objects.filter(
            student=1, course=1, is_deleted=True).first()
        self.assertTrue(obj is None)

    def test_students_list_csv_ok(self):
        """Test that students list csv file is succesfully generated."""

        url = reverse('students-list')
        response = self.client.get(url)
        file_content = b'full_name,courses_assigned,courses_completed\r\nTom2 Bri2,0,0\r\nTom1 Bri1,0,0\r\n'
        file_type = ('Content-Type', 'text/csv')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(file_content, response.content)
        self.assertEqual(file_type, response._headers['content-type'])

    def test_students_list_csv_fail(self):
        """Test that students list csv file is not generated."""

        url = reverse('students-list')
        response = self.client.get(url)
        file_content = b'lorem-lorem'
        file_type = ('Content-Type', 'text/html')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(file_content, response.content)
        self.assertNotEqual(file_type, response._headers['content-type'])