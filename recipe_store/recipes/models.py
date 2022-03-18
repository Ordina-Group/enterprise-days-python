from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    ingredients = models.ManyToManyField("Ingredient", through="RecipeIngredient")

    @property
    def sku(self) -> str:
        return f"PIZ{self.id:08d}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    @property
    def sku(self) -> str:
        return f"ING{self.id:08d}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
