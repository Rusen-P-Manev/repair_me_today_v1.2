from django import forms
from django.core.exceptions import ValidationError

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control form-control-lg'


class ReadOnlyModelMixin:
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(f"Записът '{self}' не може да бъде променян.")
        super().save(*args, **kwargs)


class ReadOnlyFieldsModelMixin:
    readonly_fields = []

    def clean(self):
        super().clean()
        if self.pk:
            original_obj = self.__class__.objects.get(pk=self.pk)

            for field_name in self.readonly_fields:
                original_value = getattr(original_obj, field_name)
                current_value = getattr(self, field_name)

                if original_value != current_value:
                    raise ValidationError({
                        field_name: f"Полето '{field_name}' не може да бъде променено."
                    })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)