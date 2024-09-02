import pytest
from ttetl.utils import format_duration

@pytest.mark.parametrize("duration, expected", [
  (0, "00:00"),
    (2, "00:02"),
    (59, "00:59"),
    (60, "01:00"),
    (61, "01:01"),
    (60*60-1, "59:59"),
    (60*60, "01:00:00"),
    (60*60+1, "01:00:01"),
    (1*24*60*60+77, "24:01:17"),
    (3*24*60*60-1, "71:59:59"),
    (3*24*60*60, "3 days"),
    (3*24*60*60+1, "3 days"),
    (5*24*60*60+1, "5 days")
])
def test_duration_formatting(duration: int, expected: str) -> None:
  assert expected == format_duration(duration)