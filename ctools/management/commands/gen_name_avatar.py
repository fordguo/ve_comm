from django.core.management.base import BaseCommand
from ctools.avatar import gen_avatar, get_bucket


class Command(BaseCommand):
    help = '初始化用户头像'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--theme', type=str, default='default')

    def handle(self, *args, **options):
        bucket = get_bucket()
        theme = options['theme']
        A, Z = 65, 90
        # A(65)-Z(90)
        for i in range(A, Z+1):
            first = chr(i)
            for j in range(A, Z+1):
                last = chr(j)
                name = f"{first}{last}"
                gen_avatar(bucket, name, theme)
                print(name, end=' ', flush=True)
