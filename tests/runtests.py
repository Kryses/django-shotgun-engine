import os
import sys
from types import ModuleType


def runtests(foo, settings='settings', extra=[], test_builtin=False):
    if isinstance(foo, ModuleType):
        settings = foo.__name__
        apps = foo.INSTALLED_APPS
    else:
        apps = foo
    if not test_builtin:
        apps = filter(lambda name: not name.startswith('django.contrib.'),
                      apps)
    # pre-1.6 test runners don't understand full module names
    import django
    if django.VERSION < (1, 6):
        apps = [app.replace('django.contrib.', '') for app in apps]
    execute(['python', './manage.py', 'test', '--settings', settings] + extra + apps)


def execute_python(lines):
    from textwrap import dedent
    return execute(
        [sys.executable, '-c', dedent(lines)],
        env=dict(os.environ, DJANGO_SETTINGS_MODULE='settings',
                 PYTHONPATH='..'))


def main(short):

    import settings
    import settings.shotgun

    runtests(settings, extra=['--failfast'] if short else [])

    # Assert we didn't touch the production database.

    runtests(settings.INSTALLED_APPS)



if __name__ == '__main__':
    import sys

    if 'ignorefailures' in sys.argv:
        from subprocess import call as execute
    else:
        from subprocess import check_call as execute
    if 'coverage' in sys.argv:

        def _new_check_call_closure(old_check_call):

            def _new_check_call(cmd, **kwargs):
                if not cmd[0].endswith('python'):
                    cmd = ['coverage', 'run', '-a', '--source',
                           '../django_mongodb_engine'] + cmd
                return old_check_call(cmd, **kwargs)

            return _new_check_call


        execute = _new_check_call_closure(execute)
    main('short' in sys.argv)
