import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# ================= FILTER BY STATE =================


def test_filter_by_state_default(sample_data):
    expected = [
        {"date": "2019-07-03T18:35:29.512364", "id": 41428829, "state": "EXECUTED"},
        {"date": "2018-06-30T02:08:58.425572", "id": 939719570, "state": "EXECUTED"},
    ]

    assert filter_by_state(sample_data) == expected


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        )
    ],
)
def test_filtering_by_specified_status(sample_data, state, expected):
    assert filter_by_state(sample_data, state) == expected


@pytest.mark.parametrize("invalid_state", [None, "NONEXISTENT", 1234, True, {}])
def test_filter_by_state_invalid_or_missing(sample_data, invalid_state):
    assert filter_by_state(sample_data, invalid_state) == []


# ================= SORT BY DATE =================


def test_sort_by_date_default_descending(sample_data):
    expected = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert sort_by_date(sample_data) == expected


def test_sort_by_date_ascending(sample_data):
    expected = [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]
    assert sort_by_date(sample_data, descending=False) == expected


@pytest.mark.parametrize(
    "descending, expected",
    [
        (
            True,
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-07-03T21:27:25.241689"},
                {"id": 41428829, "state": "EXECUTED", "date": "2018-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-07-03T08:21:33.419441"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-07-03T02:08:58.425572"},
            ],
        ),
        (
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
def test_sort_by_date_same_day(descending, expected):
    input_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2018-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-07-03T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-07-03T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-07-03T08:21:33.419441"},
    ]
    assert sort_by_date(input_data, descending=descending) == expected


def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []
    assert sort_by_date([], descending=False) == []
