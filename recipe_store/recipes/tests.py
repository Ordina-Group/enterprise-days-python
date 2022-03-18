from rest_framework import status
from rest_framework.test import APITestCase


class TestGetRecipes(APITestCase):
    def test_get_recipes(self) -> None:
        response = self.client.get("/recipes/")

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
        response = self.client.get("/recipes/PIZ00000001")

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
        response = self.client.get("/recipes/PIZ00000002")

        self.assertEqual(response.status_code, 404)


class TestGetIngredients(APITestCase):
    def test_get_ingredients(self) -> None:
        response = self.client.get("/ingredients/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {"sku": "ING00000001", "name": "dough", "description": "The dough"},
                {"sku": "ING00000002", "name": "tomato sauce", "description": "Sauce"},
            ],
        )
