from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def br_constitution_text() -> str:
    return Path("tests/data/br_constitution.txt").read_text()


@pytest.fixture(scope="session")
def us_constitution_text() -> str:
    return Path("tests/data/us_constitution.txt").read_text()
