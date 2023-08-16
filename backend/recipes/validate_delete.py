from django.forms.models import BaseInlineFormSet
from django.forms import ValidationError


class ValidateDeliteForm(BaseInlineFormSet):

    def clean(self):
        super().clean()

        delete_flags = [form.cleaned_data.get('DELETE')
                        for form in self.forms if hasattr(form,
                                                          'cleaned_data')]
        if all(delete_flags):
            raise ValidationError('Нужен минимум один тег и один ингредиент')
