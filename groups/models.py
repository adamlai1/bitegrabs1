import uuid
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255)
    leader = models.ForeignKey(User, related_name='led_groups', on_delete=models.CASCADE, null=True, blank=True)
    guest_leader = models.CharField(max_length=255, null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255)
    preferences = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username if self.user else self.guest_name} in {self.group.name}'
