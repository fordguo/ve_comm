import os
from django.core.management.base import BaseCommand
from django.conf import settings
from post_office.models import EmailTemplate
from tablib import Dataset
from ctools.post_email import send_mail_now

# 报名成功：会议名称
# 会议提醒：会议名称
# 观看回放：会议名称


class Command(BaseCommand):
    help = 'CSV邮件通知'

    def add_arguments(self, parser):
        parser.add_argument('csv_file',  type=str)
        parser.add_argument('template', type=str)
        parser.add_argument('-s', '--sender', type=str,
                            default=settings.DEFAULT_FROM_EMAIL)

    def handle(self, *args, **options):
        filename = options['csv_file']
        if not filename:
            self.stderr.write(self.style.ERROR('请输入CSV数据文件！'))
            exit(1)
        if not os.path.exists(filename):
            self.stderr.write(self.style.ERROR(f'{filename} 文件不存在！'))
            exit(1)
        template = options['template']
        sender = options['sender']
        count = 0
        template_inst = EmailTemplate.objects.get(name=template)
        with open(filename, 'r', encoding='utf-8') as f:
            mail_datas = Dataset().load(f, 'csv')
            for d in mail_datas.dict:
                data = {'sender': sender, 'recipients': [d['email']],
                        'template': template_inst, 'context': d}
                send_mail_now(data)
                count += 1
        self.stdout.write(self.style.SUCCESS(f"邮件总数：{count}"))

        self.stdout.write(self.style.SUCCESS(f'成功发送 {template} 邮件！'))
