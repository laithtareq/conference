from django.contrib import admin
from .models import newManuscript,Comment,Category,Profile,PDF_Files
# Register your models here.
admin.site.register(newManuscript)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(PDF_Files)