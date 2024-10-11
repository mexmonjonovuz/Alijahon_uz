from django.db.models import Model, SlugField, CharField, DateTimeField
from django.utils.text import slugify


class SlugBasedModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):  # noqa
        self.slug = slugify(self.name, allow_unicode=True)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class TimeBasedModel(Model):
    created_at = DateTimeField(auto_now=True)
    updated_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SlugTimeBasedModel(TimeBasedModel, SlugBasedModel):
    class Meta:
        abstract = True
