from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "title", "image_original", "image_compress", "upload_date", "description", "image_tag", ]
    fields = (
        "image_tag", "image_original", "title", "description",
    )

    readonly_fields = ('image_tag', )


admin.site.register(Image, ImageAdmin)
