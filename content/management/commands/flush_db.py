from django.core.management.commands.flush import Command as BaseFlushCommand

# NOTE: This command exists because the `--allow-cascade` flag on the inbuilt
#       flush command is hidden and not reachable from the commandline. This
#       command makes the flag avaliable froim the commandline

class Command(BaseFlushCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--allow-cascade', action='store_true', dest='allow_cascade', default=False,
                help='Adds "CASCADE" option to TRUNCATE command if supported by db backend. Default=False.',
        )
