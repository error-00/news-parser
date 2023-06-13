import os
import sys

import django

sys.path.append('D:/2 Projects/news/news_parser')
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_parser.settings'
django.setup()
