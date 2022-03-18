from rest_framework import status
from rest_framework.test import APITestCase


class TestGetRecipes(APITestCase):
    def test_get_recipes(self) -> None:
        response = self.client.get("/recipes/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"sku": "1", "name": "Pepperoni", "description": "A nice pepperoni pizza"}])
