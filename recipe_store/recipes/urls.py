from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from recipes import views

urlpatterns = [
    path('', views.RecipeView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
