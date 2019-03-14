from project1 import main
import pytest
file = "tests/sample.txt"
fileopen = open(file, "r")
string =  fileopen.read()
if(string != ""):
    (string,locs) = main.redact_locs(string)
    assert string is not None
    assert len(locs) == 2
