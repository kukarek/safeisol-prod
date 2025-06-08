from django import template

register = template.Library()

@register.inclusion_tag('main/header.html')
def header(cat_selected=None):
    """
    Renders the header template with the selected category.
    If a category is selected, it is passed to the template context.
    """
    if cat_selected:
        return {'cat_selected': cat_selected}
    else:
        return {}

@register.inclusion_tag('main/footer.html')
def footer():
    """
    Renders the footer template.
    This template does not require any specific context data.
    """
    return {}

@register.inclusion_tag('main/carousel.html')
def carousel():
    """
    Renders the carousel template.
    This template does not require any specific context data.
    """
    return {}

