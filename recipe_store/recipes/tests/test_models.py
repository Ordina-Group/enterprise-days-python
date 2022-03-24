from django.test import TestCase
from recipes.models import Ingredient, Recipe


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
