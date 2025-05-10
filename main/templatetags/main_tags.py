from django import template


register = template.Library()




@register.inclusion_tag('main/header.html')
def header(cat_selected=None):
    
    if cat_selected:
        return {'cat_selected': cat_selected}
    else:
        return {}

@register.inclusion_tag('main/footer.html')
def footer():
    return {}

@register.inclusion_tag('main/carousel.html')
def carousel():
    return {}

