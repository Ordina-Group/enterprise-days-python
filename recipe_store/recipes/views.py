from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeView(APIView):
    def get(self, request: Request) -> Response:
        return Response(
            [
                {
                    "sku": recipe.sku,
                    "name": recipe.name,
                    "description": recipe.description,
                }
                for recipe in Recipe.objects.all()
            ],
            status=status.HTTP_200_OK,
        )


class RecipeDetailView(APIView):
    def get(self, request: Request, sku: str) -> Response:
        recipe = get_object_or_404(Recipe, sku=sku)

        return Response(
            {
                "sku": sku,
                "name": recipe.name,
                "description": recipe.description,
                "ingredients": [
                    {
                        "sku": ingredient.ingredient.sku,
                        "name": ingredient.ingredient.name,
                        "description": ingredient.ingredient.description,
                        "quantity": ingredient.quantity,
                    }
                    for ingredient in recipe.recipeingredient_set.all()
                ],
            },
            status=status.HTTP_200_OK,
        )


class IngredientsView(APIView):
    def get(self, request: Request) -> Response:
        return Response(
            [
                {
                    "sku": ingredient.sku,
                    "name": ingredient.name,
                    "description": ingredient.description,
                }
                for ingredient in Ingredient.objects.all()
            ],
            status=status.HTTP_200_OK,
        )
