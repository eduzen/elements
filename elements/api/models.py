from django.db import models
from django.utils.safestring import mark_safe

from imagekit.models import ImageSpecField


class Image(models.Model):
    title = models.CharField(max_length=200,)
    description = models.CharField(max_length=600, blank=True, null=True,)
    upload_date = models.DateTimeField(auto_now_add=True, )
    image_original = models.ImageField(
        upload_to='images/%Y/%m/%d', default="images/default/noimages.png", )
    image_compress = ImageSpecField(
        source='image_original',
        format='JPEG', options={'quality': 60}, )

    def image_tag(self):
        """ This method is useful for the django admin. It allows you to see a thumbnail"""
        return mark_safe(
            "<img src='{}' width='100' height='100'/>".format(self.image_original.url)
        )
    image_tag.short_description = 'Image'

    def __str__(self):
        return "{!r} - RelativePath: {}>".format(self.title, self.image_original)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
