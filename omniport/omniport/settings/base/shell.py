"""
Nearly every aspect of Omniport can be overridden with a shell. Shell provides a
way to override Omniport in a progressive way, only customising the aspects that
need to be altered.

This settings file exposes a variable indicated whether a shell has been
installed in the current Omniport configuration.
"""

SHELL_PRESENT = False
try:
    from shell.apps import ShellConfig

    # Shell has been installed
    SHELL_PRESENT = True
except ImportError:
    # Shell has not been installed
    pass

__all__ = [
    'SHELL_PRESENT'
]
