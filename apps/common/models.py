from django.db import models
from django.utils import timezone


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    all_objects = models.Manager()  # all, deleted includes
    objects = ActiveManager()  # only active in default

    class Meta:
        abstract = True

    def delete(self, soft=True, using=None, keep_parents=False):
        if soft:
            self.deleted_at = timezone.now()
            self.save(update_fields=["deleted_at"])
        else:
            super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])
