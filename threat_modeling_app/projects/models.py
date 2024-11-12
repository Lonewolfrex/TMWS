from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure this line exists
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class ProjectStep(models.Model):
    project = models.ForeignKey(Project, related_name='steps', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name