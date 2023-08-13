from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter


from users.models import User
from recipes.models import Recipe


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def is_favorited_or_in_cart(self, queryset, name, value, related_model):
        return queryset.filter(**{f'{related_model}__user':
                                  self.request.user}) if value else queryset

    def filter_is_favorited(self, queryset, name, value):
        return self.is_favorited_or_in_cart(queryset, name,
                                            value, 'favorites')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.is_favorited_or_in_cart(queryset, name,
                                            value, 'shoppingcarts')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
