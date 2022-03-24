from typing import cast

from recipes.models import Ingredient, Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TestRecipeAPIView(APITestCase):
    def test_get_recipes(self) -> None:
        name = "Pepperoni"
        description = "A nice pepperoni pizza"
        recipe = Recipe.objects.create(name=name, description=description)

        response = cast(Response, self.client.get("/api/recipes/"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "sku": recipe.sku,
                    "name": name,
                    "description": description,
                }
            ],
        )


class TestRecipeDetailAPIView(APITestCase):
    def test_get_recipe__recipe_found(self) -> None:
        name = "Pepperoni"
        description = "A nice pepperoni pizza"
        recipe = Recipe.objects.create(name=name, description=description)
        recipe.ingredients.create(
            name="dough", description="The dough", through_defaults={"quantity": 1}
        )  # type: ignore[misc] # noqa: E501
        recipe.ingredients.create(
            name="tomato sauce", description="Sauce", through_defaults={"quantity": 2}
        )  # type: ignore[misc] # noqa: E501

        response = cast(Response, self.client.get(f"/api/recipes/{recipe.sku}"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "sku": recipe.sku,
                "name": recipe.name,
                "description": recipe.description,
                "ingredients": [
                    {
                        "sku": "ING00000001",
                        "name": "dough",
                        "description": "The dough",
                        "quantity": 1,
                    },
                    {
                        "sku": "ING00000002",
                        "name": "tomato sauce",
                        "description": "Sauce",
                        "quantity": 2,
                    },
                ],
            },
        )

    def test_get_recipe__recipe_not_found(self) -> None:
        response = cast(Response, self.client.get("/api/recipes/PIZ00000002"))

        self.assertEqual(response.status_code, 404)


class TestIngredientsAPIView(APITestCase):
    def test_get_ingredients(self) -> None:
        Ingredient.objects.create(name="dough", description="The dough")
        Ingredient.objects.create(name="tomato sauce", description="Sauce")

        response = cast(Response, self.client.get("/api/ingredients/"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {"sku": "ING00000001", "name": "dough", "description": "The dough"},
                {"sku": "ING00000002", "name": "tomato sauce", "description": "Sauce"},
            ],
        )
