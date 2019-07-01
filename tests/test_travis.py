import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

def test_travis():
    assert True

def test_selenium():
    options = Options()
    options.add_argument('-headless')
    firefox = Firefox(executable_path="./geckodriver", options=options)
    firefox.get("http://www.example.org")
    firefox.close()
