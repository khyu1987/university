from django.db import models


class AbstractBaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Student(AbstractBaseModel):
    """Provide a student model"""

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ('-created',)

    def __str__(self):
        return self.full_name


class Course(AbstractBaseModel):
    """Provide a course model"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('-created',)

    def __str__(self):
        return self.name


class CourseParticipant(AbstractBaseModel):
    """Provide a participant model"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='participants')
    completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        ordering = ('-created',)


