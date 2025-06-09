class BreadcrumbsMixin:
    """
    Mixin to add breadcrumbs to the context of a view.
    This mixin can be used in any view to provide a consistent way of managing breadcrumbs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.breadcrumbs = []

    def get_breadcrumbs(self) -> list[dict[str, str]]:
        """
        Returns the breadcrumbs for the current view.
        This method can be overridden in subclasses to customize the breadcrumbs.
        """
        return self.breadcrumbs

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds breadcrumbs to the context data of the view.
        This method is called by Django when rendering the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class SectionMixin:
    """Mixin to add section and subtitle to the context of a view.
    This mixin can be used in any view to provide a consistent way of managing section and subtitle.
    Attributes:
        section (str): Identifier for the section.
        subtitle (str): Subtitle for the section.
    """
    
    section = None
    subtitle = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.section:
            context['section'] = self.section
        if self.subtitle:
            context['subtitle'] = self.subtitle
        return context
