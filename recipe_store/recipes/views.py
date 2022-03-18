from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from recipes.models import Ingredient, Recipe
from recipes.serializers import (
    IngredientSerializer,
    RecipeDetailSerializer,
    RecipeSerializer,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeView(APIView):
    @extend_schema(description="get all recipes", responses=RecipeSerializer)
    def get(self, request: Request) -> Response:
        recipes = Recipe.objects.all()

        print(recipes)

        return Response(
            RecipeSerializer(recipes, many=True).data,
            status=status.HTTP_200_OK,
        )


class RecipeDetailView(APIView):
    @extend_schema(
        description="get single recipe",
        parameters=[
            OpenApiParameter(
                "sku",
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                description="sku of the recipe",
            )
        ],
        responses=RecipeDetailSerializer,
    )
    def get(self, request: Request, sku: str) -> Response:
        recipe = get_object_or_404(Recipe, sku=sku)

        return Response(
            RecipeDetailSerializer(recipe).data,
            status=status.HTTP_200_OK,
        )


class IngredientsView(APIView):
    @extend_schema(
        description="get all ingredients", parameters=[], responses=IngredientSerializer
    )
    def get(self, request: Request) -> Response:
        return Response(
            IngredientSerializer(Ingredient.objects.all(), many=True).data,
            status=status.HTTP_200_OK,
        )
