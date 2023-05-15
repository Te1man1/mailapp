#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import sqlite3


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailapp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    # Создаем новую базу данных и устанавливаем ее кодировку на UTF-8
    new_conn = sqlite3.connect('mydatabase_new.db')
    new_conn.execute("PRAGMA encoding = 'UTF-8';")

    # Подключаемся к старой базе данных и экспортируем данные в новую базу данных
    old_conn = sqlite3.connect('mydatabase_old.db')
    with old_conn, new_conn:
        for line in old_conn.iterdump():
            new_conn.execute(line)


if __name__ == '__main__':
    main()
