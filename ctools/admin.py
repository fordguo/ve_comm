from .post_email import send_mail_now
from .forms import BatchEmailForm
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib import messages
from django.shortcuts import redirect

from import_export.formats.base_formats import DEFAULT_FORMATS
from post_office.admin import EmailAdmin


from .models import BatchEmail, ImportLog, SmsLog, WechatMsgLog


class NoAddDeleteMixin:
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyAdminMixin(NoAddDeleteMixin):
    def has_change_permission(self, request, obj=None):
        return False


class ImportLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'file_name', 'resource_cls',
                    'totals', 'created_at')


class BatchEmailAdmin(EmailAdmin):
    change_list_template = "admin/email/email_changelist.html"
    batch_template_name = "admin/email/batch_send.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('batch-send/', self.batch_email,
                 name='ctools_batchemail_batch_send'),
        ]
        return my_urls + urls

    def batch_email(self, request):
        form = BatchEmailForm(DEFAULT_FORMATS,
                              request.POST or None, request.FILES or None)
        context = {"opts": self.model._meta, "form": form}
        if request.POST and form.is_valid():
            datas = form.cleaned_data
            input_format = DEFAULT_FORMATS[int(datas['input_format'])]()
            import_file = datas['import_file']
            data = import_file.read()
            if not input_format.is_binary():
                data = str(data, "utf-8")
            dataset = input_format.create_dataset(data)
            count = 0
            template = datas["template"].name
            for d in dataset.dict:
                mail_data = {'sender': datas['sender'], 'recipients': [d['email']],
                             'template': datas["template"], 'context': d}
                send_mail_now(mail_data)
                count += 1
            messages.add_message(request, messages.INFO,
                                 f"发送 {template} 总数是{count}")
            return redirect("admin:ctools_batchemail_changelist")

        return TemplateResponse(request, [self.batch_template_name], context)


class SmsLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('phones', 'template', 'sign_name',
                    'send_result', 'created_at')
    search_fields = ['phones', 'template']
    date_hierarchy = 'created_at'


class WechatLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('openid', 'template', 'url',
                    'send_result', 'created_at')
    search_fields = ['openid', 'template']
    date_hierarchy = 'created_at'


admin.site.register(ImportLog, ImportLogAdmin)
admin.site.register(BatchEmail, BatchEmailAdmin)
admin.site.register(SmsLog, SmsLogAdmin)
admin.site.register(WechatMsgLog, WechatLogAdmin)
