from django.contrib import admin
from article.models import Article
from article.models import Arctic
from article.models import Candidate
from article.models import Postjob
from article.models import Resume
from article.models import Joblist

admin.site.register(Article)
admin.site.register(Arctic)
admin.site.register(Candidate)
admin.site.register(Postjob)
admin.site.register(Resume)
admin.site.register(Joblist)
