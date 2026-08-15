"""
Tests for dependency pins that carry a published advisory

These read `pyproject.toml` and `poetry.lock` directly rather than the
installed environment, so they fail on the pin that ships rather than on
whatever happens to be resolved in a particular virtualenv.
"""

import pathlib
import re
import tomllib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / 'pyproject.toml'
LOCK = ROOT / 'poetry.lock'

# package -> (first safe version, advisory, what it is)
ADVISORIES = {
    'pillow': (
        (10, 2, 0),
        'CVE-2023-50447 / GHSA-3f63-hfp8-52jq',
        'PIL.ImageMath.eval executes arbitrary code passed through its '
        'environment parameter. The advisory covers every release through '
        '10.1.0, so no version under a ^9 constraint closes it.',
    ),
}

# Names Pillow 10 removed. Their presence anywhere in the package would mean
# the bump breaks at runtime rather than at import.
REMOVED_IN_PILLOW_10 = (
    'ANTIALIAS', 'textsize', 'Image.CUBIC', 'Image.LINEAR',
)


def parse_version(text):
    numbers = re.findall(r'\d+', text)
    return tuple(int(number) for number in numbers[:3])


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


class TestAdvisedDependencies(unittest.TestCase):
    """
    A dependency with a published advisory must be pinned past it
    """

    @classmethod
    def setUpClass(cls):
        with open(PYPROJECT, 'rb') as pyproject:
            cls.pyproject = tomllib.load(pyproject)
        cls.dependencies = {
            key.lower(): value
            for key, value
            in cls.pyproject['tool']['poetry']['dependencies'].items()
        }
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

        `^9.0.1` resolving to a patched 9.x is impossible, so the constraint
        itself has to be above the floor, not just today's resolution.
        """

        for package, (minimum, advisory, _) in ADVISORIES.items():
            with self.subTest(package=package):
                constraint = self.dependencies.get(package)
                self.assertIsNotNone(
                    constraint,
                    f'{package} is not declared in pyproject.toml'
                )
                if isinstance(constraint, dict):
                    constraint = constraint.get('version', '')
                floor = parse_version(constraint)
                self.assertGreaterEqual(
                    floor, minimum,
                    f'{package} is constrained as {constraint!r}, which allows '
                    f'a version covered by {advisory} to be resolved on the '
                    f'next lock'
                )


class TestPillowTenCompatibility(unittest.TestCase):
    """
    The names Pillow 10 removed must not be in use
    """

    def test_no_removed_pillow_api_is_referenced(self):
        """
        Guards the 9 -> 10 bump against a runtime failure
        """

        for path in ROOT.rglob('*.py'):
            if 'tests' in path.parts or 'migrations' in path.parts:
                continue
            text = path.read_text(errors='ignore')
            for name in REMOVED_IN_PILLOW_10:
                self.assertNotIn(
                    name, text,
                    f'{path.relative_to(ROOT)} references {name!r}, which '
                    f'Pillow 10 removed'
                )


if __name__ == '__main__':
    unittest.main()
