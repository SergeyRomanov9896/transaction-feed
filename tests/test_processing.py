import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_default_return_value(data):
    assert filter_by_state(data) == [
        {"date": "2019-07-03T18:35:29.512364", "id": 41428829, "state": "EXECUTED"},
        {"date": "2018-06-30T02:08:58.425572", "id": 939719570, "state": "EXECUTED"},
    ]

    assert sort_by_date(data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        (None, []),
        ("Nothing", []),
        (1234, []),
    ],
)
def test_filtering_by_specified_status(data, state, expected):
    assert filter_by_state(data, state) == expected


def test_sort_ascending_order(data):
    assert sort_by_date(data, False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


@pytest.mark.parametrize(
    "words, descending, new",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2018-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-07-03T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-07-03T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-07-03T08:21:33.419441"},
            ],
            True,
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-07-03T21:27:25.241689"},
                {"id": 41428829, "state": "EXECUTED", "date": "2018-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-07-03T08:21:33.419441"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-07-03T02:08:58.425572"},
            ],
        ),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2018-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-07-03T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-07-03T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-07-03T08:21:33.419441"},
            ],
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-07-03T02:08:58.425572"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-07-03T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2018-07-03T18:35:29.512364"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-07-03T21:27:25.241689"},
            ],
        ),
    ],
)
def test_checking_return_values_same_dates(words, descending, new):
    assert sort_by_date(words, descending) == new
