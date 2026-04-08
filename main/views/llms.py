from django.http import HttpResponse


def llms_txt(request):
    base_url = f"{request.scheme}://{request.get_host()}"
    content = f"""# SAFEISOL

> Производство съёмной теплоизоляции (термочехлов) для промышленного оборудования.

## О компании

Компания SAFEISOL специализируется на производстве съёмных теплоизоляционных чехлов (термочехлов) для трубопроводной арматуры, оборудования и промышленных объектов. Продукция обеспечивает энергосбережение, защиту персонала от ожогов и снижение теплопотерь.

## Разделы сайта

- [Главная]({base_url}/)
- [Каталог продукции]({base_url}/catalog/)
- [О компании]({base_url}/about/)
- [Сертификаты]({base_url}/about/certificates/)
- [Доставка]({base_url}/delivery/)
- [Реализованные проекты]({base_url}/complete_projects/)
- [Услуги]({base_url}/services/)
- [Контакты]({base_url}/contacts/)

## Контакты

- Телефон: +7 (499) 403-17-52
- Email: info@safeisol.ru
- Сайт: {base_url}
"""
    return HttpResponse(content.strip(), content_type="text/plain; charset=utf-8")
