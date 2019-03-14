from project1 import main
import pytest
file = "tests/sample.txt"
fileopen = open(file, "r")
string =  fileopen.read()
if(string != ""):
    (string,gender) = main.redact_gender(string)
    assert string is not None
    assert len(gender) == 43
