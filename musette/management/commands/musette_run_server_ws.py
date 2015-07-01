# -*- coding: utf-8 -*-
import inspect
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run server tornado web sockets."

    def handle(self, *args, **options):
        self.stdout.write('Running server...')
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe())))
        path = os.path.dirname(os.path.dirname(path))
        self.stdout.write('Run server tornado')
        os.system("python " + path + "/websockets/server.py")
