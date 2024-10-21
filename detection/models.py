from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    is_video = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
