from project1 import main
import pytest
file = "tests/sample2.txt"
fileopen = open(file, "r")
string =  fileopen.read()
if(string != ""):
    (string,dates,times) = main.redact_dates_times(string)
    assert string is not None
    assert len(dates) == 2
