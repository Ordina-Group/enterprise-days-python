from typing import cast

from django.test import TestCase
from recipes.models import Ingredient, Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TestGetRecipes(APITestCase):
    def test_get_recipes(self) -> None:
        response = cast(Response, self.client.get("/recipes/"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "sku": "PIZ00000001",
                    "name": "Pepperoni",
                    "description": "A nice pepperoni pizza",
                }
            ],
        )

    def test_get_recipe__recipe_found(self) -> None:
        response = cast(Response, self.client.get("/recipes/PIZ00000001"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "sku": "PIZ00000001",
                "name": "Schnitzel pizza",
                "description": "For the true schnitzel lover!",
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
                        "quantity": 0.04,
                    },
                ],
            },
        )

    def test_get_recipe__recipe_not_found(self) -> None:
        response = cast(Response, self.client.get("/recipes/PIZ00000002"))

        self.assertEqual(response.status_code, 404)


class TestGetIngredients(APITestCase):
    def test_get_ingredients(self) -> None:
        response = cast(Response, self.client.get("/ingredients/"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {"sku": "ING00000001", "name": "dough", "description": "The dough"},
                {"sku": "ING00000002", "name": "tomato sauce", "description": "Sauce"},
            ],
        )


class TestRecipeModel(TestCase):
    def test_create_recipe_with_ingredients(self) -> None:
        pizza = Recipe.objects.create(
            name="Schnitzel pizza", description="For the true schnitzel lover!"
        )
        pizza.ingredients.create(
            name="Dough", description="The dough", through_defaults={"quantity": 1}
        )
        pizza.ingredients.create(
            name="Sauce", description="The sauce", through_defaults={"quantity": 2}
        )

        self.assertEqual(pizza.ingredients.count(), 2)

    def test_sku(self) -> None:
        # Test whether the initial sku is created
        recipe = Recipe.objects.create(
            name="Schnitzel pizza", description="For the true schnitzel lover!"
        )
        self.assertEqual(recipe.sku, "PIZ00000001")

        # Test whether the second sku is created
        recipe_2 = Recipe.objects.create(
            name="Another pizza", description="Just another pizza!"
        )
        self.assertEqual(recipe_2.sku, "PIZ00000002")

        # Test whether the third sku is created, and the ordering of skus is correct
        recipe_3 = Recipe.objects.create(
            name="Yet another pizza", description="Just another pizza!"
        )
        self.assertEqual(recipe_3.sku, "PIZ00000003")


class TestIngredientModel(TestCase):
    def test_sku(self) -> None:
        # Test whether the initial sku is created
        ingredient = Ingredient.objects.create(name="Dough", description="The dough")

        self.assertEqual(ingredient.sku, "ING00000001")

        # Test whether the second sku is created
        ingredient_2 = Ingredient.objects.create(name="Sauce", description="The Sauce")
        self.assertEqual(ingredient_2.sku, "ING00000002")

        # Test whether the third sku is created, and the ordering of skus is correct
        ingredient_3 = Ingredient.objects.create(
            name="Cheeeeze", description="Whichever flavor you want"
        )
        self.assertEqual(ingredient_3.sku, "ING00000003")
