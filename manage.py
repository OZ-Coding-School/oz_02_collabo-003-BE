#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
<<<<<<< HEAD
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kluck.settings')
=======
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Kluck_config.settings")
>>>>>>> f0f9b72e9f002559ba5a67d98864a3cbe396d455
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


<<<<<<< HEAD
if __name__ == '__main__':
=======
if __name__ == "__main__":
>>>>>>> f0f9b72e9f002559ba5a67d98864a3cbe396d455
    main()
