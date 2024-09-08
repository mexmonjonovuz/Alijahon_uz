from django.views.generic import TemplateView


class HomeTemplateView(TemplateView):
    template_name = 'apps/main_base.html'
