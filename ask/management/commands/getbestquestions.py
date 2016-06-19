from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.management.base import BaseCommand
from ask.models import Tag, Question

class Command(BaseCommand):
    args = 'No args'
    help = 'Script to create cache for best questions'

    days = 90 # entered__gte=datetime.now()-timedelta(days=self.days)
    amount_to_select = 100
    cache_time = 360000

    def handle(self, *args, **options):
        self.stdout.write('Start request to set best questions')
        questions = Question.objects.filter(created_at__gt=datetime.now()-timedelta(days=self.days))

        question_list = []
        for q in questions:
            question_list.append({
                'question' : q,
                'rating' : q.get_rating()
            })

        question_list = sorted(question_list, key=lambda k : k['rating'], reverse=True)[:self.amount_to_select]
        question_list_best = []
        for q in question_list:
            question_list_best.append(q['question'])

        cache.set('question_list_best', question_list_best, self.cache_time)
        self.stdout.write('Finish calculating best questions')
