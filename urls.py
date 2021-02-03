from django.urls import path
from django.conf.urls import url
from django.views.static import serve
import os

from . import views
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(BASE_DIR, 'ChromoGraph', 'static')
INDEX_ROOT = os.path.join(BASE_DIR, 'index')

app_name = 'ChromoGraph'
urlpatterns = [
    path('', views.FileFieldView.as_view(), name='multiple'),
    # url(r'^static/media/(?P<path>.*)$', serve,
    #         {'document_root': SITE_ROOT, 'show_indexes': True},
    #         name='storage'),
]
