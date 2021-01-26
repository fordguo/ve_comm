import os
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from django.utils.text import Truncator
from tablib import Dataset
from ctools.wechat import send_msg


class Command(BaseCommand):
    help = 'CSV微信通知'

    def add_arguments(self, parser):
        parser.add_argument('csv_file',  type=str)
        parser.add_argument('template', type=str)

    def _to_msg_data(self, data):
        msg_data = {}
        for key, value in data.items():
            if key != 'openid' and key != 'url':
                msg_data[key] = {'value': value}
        return msg_data

    def handle(self, *args, **options):
        filename = options['csv_file']
        if not filename:
            print('请输入CSV数据文件！')
            exit(1)
        if not os.path.exists(filename):
            print(f'{filename} 文件不存在！')
            exit(1)
        template = options['template']
        send_count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            datas = Dataset().load(f, 'csv')
            for d in datas.dict:
                openid = d['openid']
                send_msg(openid, template, self._to_msg_data(d), d['url'])
                send_count += 1

        self.stdout.write(self.style.SUCCESS(f"微信模板消息发送数量:{send_count}"))

        self.stdout.write(self.style.SUCCESS(f'成功发送 {template} 微信通知！'))
