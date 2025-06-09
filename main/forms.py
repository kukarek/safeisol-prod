from django import forms
from django.forms import TextInput, Textarea


class ContactForm(forms.Form):
    """
    Форма для отправки контактной информации на почту.

    Fields:
        name: Имя или название организации (обязательное)
        phone: Телефон (обязательное)
        email: Email (обязательное, с проверкой на корректность)
        comment: Комментарий (необязательное)
    """

    # Отключаем обязательность атрибутов на уровне HTML
    use_required_attribute = False

    name = forms.CharField(
        required=True,
        widget=TextInput(attrs={
            'placeholder': 'Имя / Название организации',
            'class': 'form-control',
        }),
    )

    phone = forms.CharField(
        required=True,
        widget=TextInput(attrs={
            'placeholder': 'Телефон',
            'class': 'form-control',
        }),
    )

    email = forms.EmailField(
        required=True,
        widget=TextInput(attrs={
            'placeholder': 'E-MAIL',
            'class': 'form-control',
        }),
        error_messages={
            'required': 'Введите email адрес.',
            'invalid': 'Некорректный email адрес.',
        },
    )

    comment = forms.CharField(
        required=False,
        widget=Textarea(attrs={
            'placeholder': 'Комментарий',
            'style': 'padding: 40px 20px;',
            'class': 'form-control',
        }),
    )
