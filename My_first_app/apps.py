from django.apps import AppConfig


class MyFirstAppConfig(AppConfig):
    name = 'My_first_app'

    def ready(self):
        import My_first_app.signals