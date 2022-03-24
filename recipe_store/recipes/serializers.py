from recipes.models import Ingredient, Recipe, RecipeIngredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["sku", "name", "description"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    sku = serializers.ReadOnlyField(source="ingredient.sku")
    name = serializers.ReadOnlyField(source="ingredient.name")
    description = serializers.ReadOnlyField(source="ingredient.description")

    class Meta:
        model = RecipeIngredient
        fields = ["sku", "name", "description", "quantity"]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["sku", "name", "description"]


class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source="recipeingredient_set"
    )

    class Meta:
        model = Recipe
        fields = ["sku", "name", "description", "ingredients"]
