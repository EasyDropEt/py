from unittest.mock import patch

import pytest

from src.package.main import main


@pytest.fixture
def test_function():
    with patch("src.package.main.test_function") as test_function:
        yield test_function


def test_main(test_function):
    # WHEN
    main()

    # THEN
    test_function.assert_called_once()
