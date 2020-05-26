from __future__ import absolute_import, unicode_literals

import os

import kombu
from celery import Celery, bootsteps
from django.db import IntegrityError
from kombu import Exchange, Queue
from kombu.serialization import registry
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vk_poster.settings')

app = Celery('vk_poster')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

registry.enable('json')
registry.enable('application/text')

reddit_queue = Queue('reddit_queue', Exchange('reddit_exchange'), 'reddit', message_ttl=600)


class ReditVkConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[reddit_queue],
                               callbacks=[self.handle_message],
                               accept=['json', 'text/plain'])]

    def handle_message(self, body, message):
        from apps.posts.models import Community, Post

        print('*'*50)
        print(body)
        print('*'*50)

        try:
            community = Community.objects.get(subbredit_name=body['subreddit'])
            Post.objects.create(
                vk_community=community,
                score=body['score'],
                self_text=body['self_text'] or '',
                url=body['url'],
                reddit_id=body['id'],
                title=body['title'],
                is_self=body['is_self']
            )
        except (Community.DoesNotExist, IntegrityError):
            pass
        message.ack()


app.steps['consumer'].add(ReditVkConsumer)
