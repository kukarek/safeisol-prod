from django import forms
from django.forms import TextInput, Textarea


class ContactForm(forms.Form):
    
    use_required_attribute = False  # Отключаем обязательность атрибутов на уровне HTML

    # Поле для имени
    name = forms.CharField(
        widget=TextInput(attrs={
            'placeholder': 'Имя / Название организации',
            'class': 'form-control'
        }),
        required=True,
    )

    # Поле для телефона
    phone = forms.CharField(
        widget=TextInput(attrs={
            'placeholder': 'Телефон',
            'class': 'form-control'
        }),
        required=True,
    )

    # Поле для email
    email = forms.EmailField(
        widget=TextInput(attrs={
            'placeholder': 'E-MAIL',
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Введите email адрес.',
            'invalid': 'Некорректный email адрес.'
        },
        required=True,
    )

    # Поле для комментариев
    comment = forms.CharField(
        widget=Textarea(attrs={
            'placeholder': 'Комментарий',
            'style': 'padding: 40px 20px;',
            'class': 'form-control'
        }),
        required=False,
    )
