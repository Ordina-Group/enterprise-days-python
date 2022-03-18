"""recipe_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import Pattern
from typing import Any

from django.contrib import admin
from django.urls import URLPattern, URLResolver, path
from django.urls.resolvers import RoutePattern
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from recipes import views as recipes_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns_: list[URLResolver | RoutePattern | URLPattern | Pattern[Any]] = [
    path("admin/", admin.site.urls),
    path("recipes/", recipes_views.RecipeView.as_view()),
    path("recipes/<str:sku>", recipes_views.RecipeDetailView.as_view()),
    path("ingredients/", recipes_views.IngredientsView.as_view()),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns_, allowed=["json"])
