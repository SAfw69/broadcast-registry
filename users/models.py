from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('engineer', 'Software Engineer'),
        ('senior_engineer', 'Senior Engineer'),
        ('lead', 'Tech Lead'),
        ('architect', 'Architect'),
        ('qa', 'QA Engineer'),
        ('devops', 'DevOps Engineer'),
        ('other', 'Other'),
    ]

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    department = models.ForeignKey('teams.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} (@{self.username})"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
