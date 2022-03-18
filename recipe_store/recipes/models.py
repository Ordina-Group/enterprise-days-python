from abc import abstractmethod
from typing import Any

from django.db import models


class SkuModelMixin(models.Model):
    sku = models.CharField(max_length=11, primary_key=True)

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def _sku_prefix(self) -> str:
        """unique 3 letter prefix for the sku"""
        ...

    def _set_sku(self) -> None:
        if self.sku == "":
            latest_recipe = self.__class__.objects.order_by("sku").last()
            if latest_recipe is not None:
                self.sku = f"{self._sku_prefix}{(int(latest_recipe.sku[3:]) + 1):08d}"
            else:
                self.sku = f"{self._sku_prefix}{1:08d}"


class Recipe(SkuModelMixin):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    ingredients = models.ManyToManyField("Ingredient", through="RecipeIngredient")

    @property
    def _sku_prefix(self) -> str:
        return "PIZ"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self._set_sku()
        super(Recipe, self).save(*args, **kwargs)


class Ingredient(SkuModelMixin):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    @property
    def _sku_prefix(self) -> str:
        return "ING"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self._set_sku()
        super(Ingredient, self).save(*args, **kwargs)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
