from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0030_rename_descriptions_product_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrackerEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("lead_submit", "Отправка заявки"),
                            ("phone_click", "Клик по телефону"),
                            ("doc_download", "Скачивание документа"),
                            ("product_view", "Просмотр товара"),
                            ("product_tab", "Переключение вкладки товара"),
                            ("product_image_view", "Просмотр изображения товара"),
                            ("catalog_view", "Просмотр каталога"),
                            ("category_view", "Просмотр категории"),
                            ("breadcrumb_click", "Клик по хлебным крошкам"),
                            ("search_query", "Поиск по сайту"),
                            ("search_click", "Клик по результату поиска"),
                            ("page_view", "Просмотр страницы"),
                            ("scroll_depth", "Глубина скролла"),
                            ("time_on_page", "Время на странице"),
                        ],
                        db_index=True,
                        max_length=50,
                    ),
                ),
                (
                    "url",
                    models.URLField(max_length=1024, verbose_name="URL страницы"),
                ),
                (
                    "product",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Товар",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Категория",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="Доп. данные"
                    ),
                ),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP"
                    ),
                ),
                (
                    "user_agent",
                    models.TextField(
                        blank=True, default="", verbose_name="User-Agent"
                    ),
                ),
                (
                    "visitor_id",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=64,
                        verbose_name="Visitor ID",
                    ),
                ),
                (
                    "session_id",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=64,
                        verbose_name="Session ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Время события",
                    ),
                ),
            ],
            options={
                "verbose_name": "Событие трекера",
                "verbose_name_plural": "События трекера",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(
                        fields=["event_type", "created_at"],
                        name="main_tracke_event__2e3f1c_idx",
                    ),
                    models.Index(
                        fields=["visitor_id", "created_at"],
                        name="main_tracke_visitor__8d7f6b_idx",
                    ),
                ],
            },
        ),
    ]