from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    Main application configuration for the 'main' app.
    This class sets the default auto field type and specifies the name of the app.
    It also imports the signals module to ensure that signal handlers are registered
    when the app is ready.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self) -> None:
        """
        Method called when the app is ready.
        It imports the signals module to ensure that signal handlers are registered.
        This is necessary to ensure that the signal handlers are connected
        when the application starts.
        """
        import main.signals
