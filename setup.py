from setuptools import setup, find_packages

setup(
    name='ve-comm',
    version='1.7.0',
    description='Virtual meeting common package',
    author='Ford Guo',
    author_email='agile.guo@qq.com',
    packages=find_packages(
        include=['webinar', 'webinar.*', 'ctools', 'ctools.*',
                 'cmedia', 'cmedia.*', 'cpage', 'cpage.*']),
    include_package_data=True,
    install_requires=[
        'django>=3.1',
        'wagtail>=2.11',
        'django-post_office>=3.4',
        'django-import-export>=2.4',
        'aliyun-python-sdk-dysmsapi>=1.0.0',
        'pypinyin>=0.40',
        'requests>=2.25'
    ],
)
