from django.db import models
from django.conf import settings
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Team(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('restructured', 'Restructured'),
        ('disbanded', 'Disbanded'),
    ]

    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='teams')
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='managed_teams'
    )
    description = models.TextField(blank=True, help_text='Team purpose and description')
    mission = models.TextField(blank=True, help_text='Team mission statement')
    responsibilities = models.TextField(blank=True)
    slack_channel = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    upstream_dependencies = models.ManyToManyField(
        'self', through='Dependency',
        through_fields=('to_team', 'from_team'),
        symmetrical=False,
        related_name='downstream_dependents',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.department})"

    class Meta:
        ordering = ['department', 'name']
        unique_together = ['name', 'department']


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='team_memberships'
    )
    join_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.team.name}"

    class Meta:
        unique_together = ['team', 'user']


class Repository(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.team.name})"

    class Meta:
        verbose_name_plural = 'Repositories'


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    object_repr = models.CharField(max_length=500)
    changes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} | {self.user} | {self.action} | {self.model_name}"

    class Meta:
        ordering = ['-timestamp']


class Dependency(models.Model):
    from_team = models.ForeignKey(Team, related_name='outgoing_dependencies', on_delete=models.CASCADE)
    to_team = models.ForeignKey(Team, related_name='incoming_dependencies', on_delete=models.CASCADE)
    DEPENDENCY_TYPES = [
        ('upstream', 'Upstream'),
        ('downstream', 'Downstream')
    ]
    dependency_type = models.CharField(max_length=20, choices=DEPENDENCY_TYPES)

    def __str__(self):
        return f"{self.from_team} -> {self.to_team} ({self.dependency_type})"


class Meeting(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='meetings')
    organiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Meeting for {self.team.name} on {self.meeting_date}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='messages')
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver_team}"
