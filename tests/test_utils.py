from pathlib import Path

from pytest import raises

from openca_tools import utils

TEST_FILE_PATH = Path(__file__).parent / 'fixtures/checksum_test_file.csv'
TEST_FILE_SHA256_SUM = '5edec7b6dd87563b2d870ee01f3ba6db28d46cd0ac002b3a0ddfdec84d185b63'  # noqa: E501


def test_compute_checksum_computes_correct_SHA256_checksum():
    checksum = utils.compute_checksum(TEST_FILE_PATH, 'SHA256')
    assert checksum == TEST_FILE_SHA256_SUM


def test_compute_checksum_with_bad_hashing_algorithm_raises_ValueError():
    with raises(ValueError):
        utils.compute_checksum(TEST_FILE_PATH, 'MDD5')


def test_compute_checksum_raises_ValueError_with_list_of_available_algorithms():  # noqa: E501
    # Avaiable algorithms are retrieved from hashlib.algorithms_available, so
    # this test confirms that attribute has not changed
    try:
        utils.compute_checksum(TEST_FILE_PATH, 'MDD5')
    except ValueError as exc:
        assert 'sha256' in str(exc)
