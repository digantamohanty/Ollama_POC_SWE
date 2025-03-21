from django.urls import path
from .views import process_pdfs

urlpatterns = [
    path('process_pdfs/', process_pdfs, name='process_pdfs'),
]