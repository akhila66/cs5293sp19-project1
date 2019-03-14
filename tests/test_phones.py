from project1 import main
import pytest
file = "tests/sample1.txt"
fileopen = open(file, "r")
string =  fileopen.read()
if(string != ""):
    (string,phones) = main.redact_phones(string)
    assert string is not None
    assert len(phones) == 1
