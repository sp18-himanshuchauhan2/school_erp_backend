from django.db import models


class ErrorMessageInfoLevels(models.TextChoices):
    info = "info", "Info message"
    error = "error", "Error occurred"
    warn = "warn", "Warning message"
    na = "NA", "Not Applicable"
    str = "error_message", "Error message"