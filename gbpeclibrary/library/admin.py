from django.contrib import admin
from .models import Author,Student,Book,Quantity,LastFiveIssues,Publisher
admin.site.register(Author)
admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Quantity)
admin.site.register(LastFiveIssues)
admin.site.register(Publisher)
