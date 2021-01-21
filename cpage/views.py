from django.shortcuts import render

# Create your views here.


class AdaptiveTemplateMixin:
    def get_template_names(self):
        names = super().get_template_names()
        if not self.request.user_agent.is_pc:
            template = names[0]
            idx = template.rfind("/")
            if idx != -1:
                names[0] = f"{template[:idx]}/mobile_{template[idx+1:]}"
            else:
                names[0] = f"mobile_{template}"
        return names
