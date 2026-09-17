#!/usr/bin/env python
#!/usr/bin/env python
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotelmanagement.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure Django is installed."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

   