from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeView(APIView):
    def get(self, request: Request) -> Response:
        return Response([{"sku": "PIZ00000001", "name": "Pepperoni", "description": "A nice pepperoni pizza"}],
                        status=status.HTTP_200_OK)


class RecipeDetailView(APIView):
    def get(self, request: Request, sku: str) -> Response:
        if sku != "PIZ00000001":
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({
            "sku": sku,
            "name": "Schnitzel pizza",
            "description": "For the true schnitzel lover!",
            "ingredients": [
                {"sku": "ING00000001", "name": "dough", "description": "The dough", "quantity": 1, "uom": "piece"},
                {"sku": "ING00000002", "name": "tomato sauce", "description": "Sauce", "quantity": 0.04, "uom": "ltr"},
            ]}, status=status.HTTP_200_OK)
