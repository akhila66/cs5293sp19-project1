from project1 import main
import pytest
file = "tests/sample.txt"
fileopen = open(file, "r")
string =  fileopen.read()
def test_redact_locs():
    if(string != ""):
        (string1,locs) = main.redact_locs(string)
        assert string1 is not None
        assert len(locs) == 2
