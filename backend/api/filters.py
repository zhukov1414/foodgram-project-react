from django.db.models import Q
from django.db.models import Exists, OuterRef, BooleanField
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    author = filters.NumberFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',
        label='Is Favorited',
    )

    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        label='Is In Shopping Cart',
    )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        
        subquery = user.favorites.filter(recipe=OuterRef('pk'))
        queryset = queryset.annotate(is_favorited=Exists(subquery))
        
        if value is True:
            return queryset.filter(is_favorited=True)
        elif value is False:
            return queryset.filter(Q(is_favorited=False) | Q(is_favorited__isnull=True))
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()

        subquery = user.shopping_carts.filter(recipe=OuterRef('pk'))
        queryset = queryset.annotate(is_in_shopping_cart=Exists(subquery))

        if value is True:
            return queryset.filter(is_in_shopping_cart=True)
        elif value is False:
            return queryset.filter(Q(is_in_shopping_cart=False) | Q(is_in_shopping_cart__isnull=True))
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
