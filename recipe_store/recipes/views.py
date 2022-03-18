from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeView(APIView):
    def get(self, request: Request) -> Response:
        return Response([{"sku": "1", "name": "Pepperoni", "description": "A nice pepperoni pizza"}], status=status.HTTP_200_OK)
