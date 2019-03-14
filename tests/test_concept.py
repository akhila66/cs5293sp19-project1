from project1 import main
import pytest
file = "tests/sample.txt"
concept = "tried"
fileopen = open(file, "r") 
string =  fileopen.read() 
if(string != ""):
    (string,similar_words,red_s) = main.redact_concept(string,concept)
    assert string is not None
    assert len(similar_words) == 4
