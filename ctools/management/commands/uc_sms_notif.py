import os
from django.core.management.base import BaseCommand
from tablib import Dataset
from ctools.uc_sms import send_sms


class Command(BaseCommand):
    help = 'CSV云机短信通知'

    def add_arguments(self, parser):
        parser.add_argument('csv_file',  type=str)
        parser.add_argument('template', type=str)
        # 西门子:VU9lHhmS
        parser.add_argument('-s', '--sign', type=str, default='VU9lHhmS')

    def handle(self, *args, **options):
        filename = options['csv_file']
        if not filename:
            print('请输入CSV数据文件！')
            exit(1)
        if not os.path.exists(filename):
            print(f'{filename} 文件不存在！')
            exit(1)
        template = options['template']
        count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            mail_datas = Dataset().load(f, 'csv')
            for d in mail_datas.dict:
                context = {k: v for k, v in d.items() if k != 'mobile'}
                send_sms([d['mobile']], options['sign'],
                         template, False, **context)
            count = len(mail_datas)
        print(f"短信总数：{count}")

        self.stdout.write(self.style.SUCCESS(f'成功发送 {template} 短信通知！'))
