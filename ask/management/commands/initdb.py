from django.core.management.base import BaseCommand
from ask.models import Tag, Profile, Question, Answer, Like

class Command(BaseCommand):
    args = 'No args'
    help = 'Script to init db'

    def handle(self, *args, **options):
        self.stdout.write('Start initDB')
        for i in range(10):
            #Profile.objects.create(username='User #{}'.format(i), password='0000')
            self.stdout.write('User #{} created.'.format(i))
        self.stdout.write('Finish initDB')
