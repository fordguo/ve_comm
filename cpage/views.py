from django.shortcuts import render

# Create your views here.


class AdaptiveTemplateMixin:
    def get_template_names(self):
        names = super().get_template_names()
        if not self.request.user_agent.is_pc:
            names[0] = f"mobile_{names[0]}"
        return names
