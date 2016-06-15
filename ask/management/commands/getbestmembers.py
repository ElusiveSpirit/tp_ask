from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.management.base import BaseCommand
from ask.models import Tag, Question, Answer

class Command(BaseCommand):
    args = 'No args'
    help = 'Script to create cache for best members'

    # Params
    days = 90 # created_at__gt=datetime.now()-timedelta(days=self.days)
    amount_to_select = 5
    cache_time = 360000

    def handle(self, *args, **options):
        self.stdout.write('Start request to find best members')
        questions = Question.objects.filter(created_at__gt=datetime.now()-timedelta(days=self.days))
        answers = Answer.objects.filter(created_at__gt=datetime.now()-timedelta(days=self.days))

        members = {}
        for q in questions:
            try:
                members[q.author] += 1
            except:
                members[q.author] = 1
        for a in answers:
            try:
                members[a.author] += 1
            except:
                members[a.author] = 1

        members = sorted(members, key=members.__getitem__, reverse=True)[:self.amount_to_select]

        self.stdout.write('Members:')
        new_members_list = []
        for m in members:
            new_members_list.append({
                'pk' : m.pk,
                'nickname' : m.first_name,
            })
            self.stdout.write(m.first_name)

        cache.set('best_members', new_members_list, self.cache_time)

        self.stdout.write('Finish calculating members')
