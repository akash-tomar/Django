"""gbpeclibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'library.views.main',name='main'),
    url(r'^addBook/','library.views.addBook',name='addBook'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^issue/','library.views.issue',name='issue'),
    url(r'^addAuthor/','library.views.addAuthor',name='addAuthor'),
    url(r'^addStudent/','library.views.addStudent',name='addStudent'),
    url(r'^deleteBook/','library.views.deleteBook',name='deleteBook'),
    url(r'^deleteStudent/','library.views.deleteStudent',name='deleteStudent'),
    url(r'^deleteAuthor/','library.views.deleteAuthor',name='deleteAuthor'),
    url(r'^bookSearch/','library.views.bookSearch',name='bookSearch'),   
    url(r'^authorSearch/','library.views.authorSearch',name='authorSearch'),
    url(r'^studentSearch/','library.views.studentSearch',name='studentSearch'),    
    url(r'^issueReturn/','library.views.issueReturn',name='issuereturn'),    
    url(r'^fine/','library.views.fine',name='fine'),    
    url(r'^bookbank/','library.views.bookbank',name='bookbank'),    
    url(r'^email/','library.views.email',name='email'),    
    url(r'^allbooks/','library.views.allbooks',name='allbooks'),    
    url(r'^login/','library.views.login',name='login'),
    url(r'^logout/','library.views.logout',name='logout'),
    url(r'^reissue/','library.views.reissue',name='reissue'),
    url(r'^claim/','library.views.claim',name='claim'),
    url(r'^profile/','library.views.profile',name='profile'),
    url(r'^signup/','library.views.signup',name='signup'),
    ]
