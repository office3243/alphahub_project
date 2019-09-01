from django.db import models


class Enquiry(models.Model):
    user = models.ForeignKey("accounts.User", blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email or str(self.created_on)

    class Meta:
        verbose_name_plural = "Enquiries"
