from django.db.models import Model, SlugField
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class SlugBaseModel(Model):
    name = CKEditor5Field('Text', config_name='extends')
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):  # noqa
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name
