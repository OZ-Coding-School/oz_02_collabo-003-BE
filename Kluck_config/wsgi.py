"""
WSGI config for Kluck_config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Kluck_config.settings")

application = get_wsgi_application()

# from gpt_prompts.scheduler import initialize_term_scheduler
# from kluck_notifications.push_scheduler import initialize_push_scheduler
# import logging

# logger = logging.getLogger('wsgi_scheduler.log')

# # 스케쥴러 초기화
# # if os.environ.get('RUN_MAIN') != 'true':  # runserver 명령이 재시작될 때를 피하기 위함
# logger.info('스케쥴러 초기화')
# initialize_term_scheduler()
# logger.info('Term스케쥴러 초기화 완료')
# initialize_push_scheduler()
# logger.info('Push스케쥴러 초기화 완료')
# logger.info('스케쥴러 초기화 완료')
