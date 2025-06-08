from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django import forms
from django.utils.html import format_html
from .models import (
    Category,
    Product,
    ContactRequest,
    CompleteProject,
    Service,
    Certificate
)

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')
    # Русские метки в админке
    def get_model_perms(self, request):
        self.model._meta.verbose_name = "Категория"
        self.model._meta.verbose_name_plural = "Категории"
        return super().get_model_perms(request)

class ProductsAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'content': JSONEditorWidget,  # здесь виджет для удобного редактирования JSON
        }

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    form = ProductsAdminForm
    list_display = ('title', 'slug', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'category__title')
    list_filter = ('category',)
    fields = ('title', 'slug', 'category', 'content') 

    def get_model_perms(self, request):
        self.model._meta.verbose_name = "Продукт"
        self.model._meta.verbose_name_plural = "Продукты"
        return super().get_model_perms(request)

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'status')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at', 'status')
    readonly_fields = ('error_message',)

    def get_model_perms(self, request):
        self.model._meta.verbose_name = "Заявка"
        self.model._meta.verbose_name_plural = "Заявки"
        return super().get_model_perms(request)

@admin.register(CompleteProject)
class CompleteProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image_path:
            image_url = "/static/main/media/complete%20projects/" + obj.image_path
            return format_html('<img src="{}" style="height: 100px;"/>', image_url)
        return "(нет изображения)"
    image_preview.short_description = 'Превью'
    image_preview.allow_tags = True  

    def get_model_perms(self, request):
        self.model._meta.verbose_name = "Выполненный проект"
        self.model._meta.verbose_name_plural = "Выполненные проекты"
        return super().get_model_perms(request)

class ServicesAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'content': JSONEditorWidget,  # виджет для удобного редактирования JSON
        }

@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    form = ServicesAdminForm
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    fields = ('name', 'slug', 'content')

    def get_model_perms(self, request):
        self.model._meta.verbose_name = "Услуга"
        self.model._meta.verbose_name_plural = "Услуги"
        return super().get_model_perms(request)

@admin.register(Certificate)
class CertificatesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

    def get_model_perms(self, request):
        self.model._meta.verbose_name = "Сертификат"
        self.model._meta.verbose_name_plural = "Сертификаты"
        return super().get_model_perms(request)
