import random
from django.core.management.base import BaseCommand
from ask.models import Tag, Profile, Question, Answer, Like

class Command(BaseCommand):
    args = 'No args'
    help = 'Script to fix db'

    def handle(self, *args, **options):
        self.stdout.write('Start initDB')
        answers = Answer.objects.all()[:]
        users = Profile.objects.all()[:]
        count = len(users) - 1

        for a in answers:
            try:
                author = a.author
            except:
                a.author = users[random.randint(0, count)]
                a.save()

        """
        for i in range(10):
            #Profile.objects.create(username='User #{}'.format(i), password='0000')
            self.stdout.write('User #{} created.'.format(i))
        """
        self.stdout.write('Finish fixDB')
