
from django.apps import apps
from django.forms.widgets import Select

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, ThumbnailMixin, modeladmin_register

from .models import SummitAgenda, SummitWebinar


class SummitAgendaModelAdmin(ModelAdmin):
    model = SummitAgenda
    menu_label = '议程'
    menu_icon = 'date'
    menu_order = 300
    list_display = ('summit_app', 'name', 'title', 'start')
    list_filter = ('summit_app', )
    search_fields = ('title', 'name')
    ordering = ('summit_app', 'name')

    def get_edit_handler(self, instance, request):
        handler = super().get_edit_handler(instance, request)
        summit_panel = handler.children[0].children[0]
        # 动态获取峰会编码
        summit_apps = [(app.name, app.summit_name)
                       for app in apps.get_app_configs() if hasattr(app, 'summit_name')]
        summit_panel.widget = Select(choices=summit_apps)
        # choice_field typed_choice_field model_choice_field 影响Select显示
        summit_panel.classname = 'typed_choice_field'
        return handler


class SummitWebinarModelAdmin(ModelAdmin):
    model = SummitWebinar
    menu_label = '直播间'
    menu_icon = 'view'
    menu_order = 301
    list_display = ('summit_app', 'cid', 'wid', 'vendor', 'channel_type')
    list_filter = ('summit_app', 'vendor', 'channel_type')
    search_fields = ('cid', 'wid')
    ordering = ('summit_app', 'channel_type', 'cid')

    def get_edit_handler(self, instance, request):
        handler = super().get_edit_handler(instance, request)
        summit_panel = handler.children[0]
        # 动态获取峰会编码
        summit_apps = [(app.name, app.summit_name)
                       for app in apps.get_app_configs() if hasattr(app, 'summit_name')]
        summit_panel.widget = Select(choices=summit_apps)
        # choice_field typed_choice_field model_choice_field 影响Select显示
        summit_panel.classname = 'typed_choice_field'
        return handler


class SummitGroup(ModelAdminGroup):
    menu_label = '峰会'
    menu_icon = 'group'
    menu_order = 200
    items = (SummitAgendaModelAdmin, SummitWebinarModelAdmin)


modeladmin_register(SummitGroup)
