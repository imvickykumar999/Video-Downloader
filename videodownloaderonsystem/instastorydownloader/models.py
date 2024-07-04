from django.db import models

class InstagramStoryDownload(models.Model):
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.url
