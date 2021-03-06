from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.management.base import BaseCommand
from ask.models import Tag, Question

class Command(BaseCommand):
    args = 'No args'
    help = 'Script to create cache for best tags'

    days = 90 # entered__gte=datetime.now()-timedelta(days=self.days)
    amount_to_select = 10
    cache_time = 360000

    def handle(self, *args, **options):
        self.stdout.write('Start request to find best tags')
        questions = Question.objects.filter(created_at__gt=datetime.now()-timedelta(days=self.days))

        tags = {}
        for q in questions:
            for t in q.tags.all():
                try:
                    tags[t.text] += 1
                except:
                    tags[t.text] = 1

        tags = sorted(tags, key=tags.__getitem__, reverse=True)[:self.amount_to_select]

        self.stdout.write('Tags:')
        for t in tags:
            self.stdout.write(t)

        cache.set('best_tags', tags, self.cache_time)

        self.stdout.write('Finish calculating tags')
