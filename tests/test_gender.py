from project1 import main
import pytest
file = "tests/sample.txt"
fileopen = open(file, "r")
string =  fileopen.read()
def test_redact_gender():
    if(string != ""):
        (string1,gender) = main.redact_gender(string)
        assert string1 is not None
        assert len(gender) == 43
