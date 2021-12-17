from django.urls import path
from .views import detail, update_tag, delete_tag


urlpatterns = [
    path('<int:id>/', detail, name='detail_tag'),
    path('update/<int:id>/', update_tag, name='update_tag'),
    path('delete/<int:id>/', delete_tag, name='delete_tag'),
]
