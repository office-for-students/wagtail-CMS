import json
import subprocess
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = (
        "Dump all data model-by-model, skipping those that cause errors "
        "(like missing tables or serialization failures)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="safe_data.json",
            help="Output file path (default: safe_data.json)",
        )
        parser.add_argument(
            "--indent",
            type=int,
            default=None,
            help="Pretty-print JSON with given indentation level",
        )
        parser.add_argument(
            "--exclude",
            nargs="+",
            default=[],
            help="List of models to exclude, in the form app_label.model_name",
        )

    def handle(self, *args, **options):
        output_file = options["output"]
        indent = options["indent"]
        exclude_models = set(m.lower() for m in options["exclude"])
        failed = []
        dumped_objects = []

        self.stdout.write(self.style.NOTICE("Starting safe dump...\n"))

        for model in apps.get_models():
            label = f"{model._meta.app_label}.{model._meta.model_name}".lower()

            if label in exclude_models:
                self.stdout.write(self.style.WARNING(f"→ Skipping {label} (excluded)"))
                continue

            self.stdout.write(f"→ Dumping {label} ...", ending="")
            self.stdout.flush()

            try:
                result = subprocess.run(
                    ["python", "manage.py", "dumpdata", label],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                data = result.stdout.strip()
                if data not in ("[]", ""):
                    objects = json.loads(data)
                    dumped_objects.extend(objects)

                self.stdout.write(self.style.SUCCESS(" OK"))
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.strip().splitlines()[-1] if e.stderr else "unknown error"
                self.stdout.write(self.style.WARNING(f" skipped ({err_msg})"))
                failed.append(label)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f" skipped ({e})"))
                failed.append(label)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(dumped_objects, f, indent=indent, ensure_ascii=False)

        self.stdout.write("\nDump complete!")
        self.stdout.write(self.style.SUCCESS(f"Data written to {output_file}"))
        if failed:
            self.stdout.write("\nSkipped models:")
            for fmodel in failed:
                self.stdout.write(f"  - {fmodel}")
