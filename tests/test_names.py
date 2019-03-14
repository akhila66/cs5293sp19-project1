from project1 import main
import pytest
file = "tests/sample.txt"
fileopen = open(file, "r")
def test_redact_names():
    string =  fileopen.read()
    if(string != ""):
        (string,names) = main.redact_names(string)
        assert string is not None
        assert len(names) == 1
