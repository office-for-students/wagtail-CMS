from django.test.runner import DiscoverRunner


class DefaultExcludeRunner(DiscoverRunner):
    """Skip @tag("performance") tests unless asked for explicitly."""

    DEFAULT_EXCLUDED = {"performance"}

    def __init__(self, *args, tags=None, exclude_tags=None,
                 include_performance=False, **kwargs):
        tags = set(tags or [])
        exclude_tags = set(exclude_tags or [])

        if not include_performance:
            # Only exclude defaults the user didn't explicitly request via --tag
            exclude_tags |= self.DEFAULT_EXCLUDED - tags

        super().__init__(*args, tags=tags, exclude_tags=exclude_tags, **kwargs)

    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--include-performance",
            action="store_true",
            help="Also run tests tagged 'performance'.",
        )