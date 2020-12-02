import pylint.lint
pylint_opts = ['alarm.py', 'announcement.py', 'getters.py', 'loggers.py', 'main.py', 'handlers.py', 'test_unit.py']
pylint.lint.Run(pylint_opts)
