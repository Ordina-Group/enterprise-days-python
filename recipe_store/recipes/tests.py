from typing import cast

from django.test import TestCase
from recipes.models import Ingredient, Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TestGetRecipes(APITestCase):
    def test_get_recipes(self) -> None:
        name = "Pepperoni"
        description = "A nice pepperoni pizza"
        recipe = Recipe.objects.create(name=name, description=description)

        response = cast(Response, self.client.get("/recipes/"))

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

        response = cast(Response, self.client.get(f"/recipes/{recipe.sku}"))

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
        response = cast(Response, self.client.get("/recipes/PIZ00000002"))

        self.assertEqual(response.status_code, 404)


class TestGetIngredients(APITestCase):
    def test_get_ingredients(self) -> None:
        Ingredient.objects.create(name="dough", description="The dough")
        Ingredient.objects.create(name="tomato sauce", description="Sauce")

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
            name="Dough", description="The dough", through_defaults={"quantity": 1}  # type: ignore[misc] # noqa: E501
        )
        pizza.ingredients.create(
            name="Sauce", description="The sauce", through_defaults={"quantity": 2}  # type: ignore[misc] # noqa: E501
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
