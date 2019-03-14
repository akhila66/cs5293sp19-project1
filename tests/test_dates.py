from project1 import main
import pytest
file = "tests/sample2.txt"
fileopen = open(file, "r")
string =  fileopen.read()
def test_redact_dates_times():
    (string1,dates,times) = main.redact_dates_times(string)
    assert string1 is not None
    assert len(dates) == 2
