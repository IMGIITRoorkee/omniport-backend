"""
Tests for dependency pins that carry a published advisory

These read `pyproject.toml` and `poetry.lock` directly rather than the
installed environment, so they fail on the pin that ships rather than on
whatever happens to be resolved in a particular virtualenv.
"""

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / 'pyproject.toml'
LOCK = ROOT / 'poetry.lock'

# Constraint shapes that state a lower bound. Anything else is rejected rather
# than read as a floor, so an upper bound or an exclusion fails closed.
FLOOR = re.compile(r'^(?:\^|~=?|>=)(\d+)(?:\.(\d+))?(?:\.(\d+))?$')

# package -> (first safe version, advisories, why)
ADVISORIES = {
    'pillow': (
        (12, 3, 0),
        'GHSA-cfh3-3jmp-rvhc, GHSA-pwv6-vv43-88gr, GHSA-whj4-6x5x-4v2j and 14 '
        'others',
        'Image decoder defects, reached by every upload path because Pillow '
        'sniffs format from content rather than from the filename. 12.3.0 is '
        'the first release with none open against it: everything affecting '
        '10.x is first patched in 12.1.1 or later, so no ^10 or ^11 '
        'constraint can resolve to a version that clears them.',
    ),
}


def parse_version(text):
    return tuple(int(number) for number in re.findall(r'\d+', text)[:3])


def parse_floor(constraint):
    """
    Return the lowest version a constraint admits, or None if it states no floor
    """

    match = FLOOR.match(constraint.strip())
    if not match:
        return None
    return tuple(int(part or 0) for part in match.groups())


def locked_versions():
    """
    Return a mapping of package name to the version pinned in poetry.lock
    """

    versions = {}
    name = None
    for line in LOCK.read_text().splitlines():
        match = re.match(r'^name = "(.+)"$', line)
        if match:
            name = match.group(1).lower()
            continue
        match = re.match(r'^version = "(.+)"$', line)
        if match and name:
            versions[name] = match.group(1)
            name = None
    return versions


def declared_constraints():
    """
    Return a mapping of package name to its constraint in pyproject.toml

    Read with `re` rather than `tomllib`, which is 3.11 and up while the
    image this deploys on ships 3.10.
    """

    section = re.search(
        r'^\[tool\.poetry\.dependencies\]$(.*?)(?=^\[|\Z)',
        PYPROJECT.read_text(),
        re.MULTILINE | re.DOTALL,
    )
    constraints = {}
    for line in section.group(1).splitlines():
        match = re.match(r'^([A-Za-z0-9._-]+) *= *(.+)$', line)
        if not match:
            continue
        version = re.search(r'version *= *"(.+?)"', match.group(2))
        if not version:
            version = re.match(r'^"(.+?)"$', match.group(2).strip())
        if version:
            constraints[match.group(1).lower()] = version.group(1)
    return constraints


class TestAdvisedDependencies(unittest.TestCase):
    """
    A dependency with a published advisory must be pinned past it
    """

    @classmethod
    def setUpClass(cls):
        cls.dependencies = declared_constraints()
        cls.locked = locked_versions()

    def test_the_locked_version_is_past_the_advisory(self):
        """
        The version that actually gets installed must be a safe one
        """

        for package, (minimum, advisory, detail) in ADVISORIES.items():
            with self.subTest(package=package):
                self.assertIn(
                    package, self.locked,
                    f'{package} is not in poetry.lock'
                )
                locked = parse_version(self.locked[package])
                self.assertGreaterEqual(
                    locked, minimum,
                    f'{package} is locked at {self.locked[package]}, which is '
                    f'covered by {advisory}. First safe version is '
                    f'{".".join(str(part) for part in minimum)}. {detail}'
                )

    def test_the_constraint_cannot_resolve_below_the_advisory(self):
        """
        A safe lock is not enough if the constraint permits an unsafe re-lock

        `^10.2.0` resolving to a version past the decoder advisories is
        impossible, so the constraint itself has to be above the floor, not
        just today's resolution.
        """

        for package, (minimum, advisory, _) in ADVISORIES.items():
            with self.subTest(package=package):
                constraint = self.dependencies.get(package)
                self.assertIsNotNone(
                    constraint,
                    f'{package} is not declared in pyproject.toml'
                )
                floor = parse_floor(constraint)
                self.assertIsNotNone(
                    floor,
                    f'{package} is constrained as {constraint!r}, which states '
                    f'no lower bound this test can read. Use a caret, tilde or '
                    f'>= constraint so the floor is checkable'
                )
                self.assertGreaterEqual(
                    floor, minimum,
                    f'{package} is constrained as {constraint!r}, which allows '
                    f'a version covered by {advisory} to be resolved on the '
                    f'next lock'
                )


class TestApplicationServerImports(unittest.TestCase):
    """
    The locked build backend must be one the pinned app server can import
    """

    def test_setuptools_is_below_the_pkg_resources_removal(self):
        """
        gunicorn 20 imports pkg_resources, which setuptools removed in 82

        The import is at module scope in gunicorn/util.py, so the mismatch
        kills the server at startup rather than on a request.
        """

        locked = locked_versions()
        if parse_version(locked['gunicorn']) >= (21, 0, 0):
            self.skipTest('gunicorn 21 and later read importlib.metadata')
        self.assertLess(
            parse_version(locked['setuptools']), (82, 0, 0),
            f"setuptools is locked at {locked['setuptools']}, which does not "
            f"ship pkg_resources, while gunicorn is locked at "
            f"{locked['gunicorn']}, which imports it at module scope"
        )


if __name__ == '__main__':
    unittest.main()
