from project1 import main
import pytest
file = "tests/sample1.txt"
fileopen = open(file, "r")
string =  fileopen.read()
def test_redact_phones():
    if(string != ""):
        (string1,phones) = main.redact_phones(string)
        assert string1 is not None
        assert len(phones) == 1
