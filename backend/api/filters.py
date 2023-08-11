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
    is_favorited = filters.NumberFilter(method='get_is_related',
                                        field_name='in_favorites')
    is_in_shopping_cart = filters.NumberFilter(method='get_is_related',
                                               field_name='in_shopping_carts')

    def get_is_related(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(**{f'{name}__user': self.request.user})
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
