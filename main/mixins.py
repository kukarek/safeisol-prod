



class BreadcrumbsMixin:
    """
    Mixin to add breadcrumbs to the context of a view.
    This mixin can be used in any view to provide a consistent way of managing breadcrumbs.
    """

    breadcrumbs = []

    def get_breadcrumbs(self):
        """
        Returns the breadcrumbs for the current view.
        This method can be overridden in subclasses to customize the breadcrumbs.
        """
        return self.breadcrumbs

    def get_context_data(self, **kwargs):
        """
        Adds breadcrumbs to the context data of the view.
        This method is called by Django when rendering the template.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context
