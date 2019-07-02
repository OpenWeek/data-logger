import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

def test_travis():
    assert True

#TODO apres shibboleth
def test_selenium_register():
    options = Options()
    options.add_argument('-headless')
    firefox = Firefox(executable_path="./geckodriver", options=options)
    firefox.get("http://localhost:8080/app.py/")
    firefox.close()

#TODO apres shibboleth
def test_selenium_login():
    options = Options()
    options.add_argument('-headless')
    firefox = Firefox(executable_path="./geckodriver", options=options)
    firefox.get("http://localhost:8080/app.py/")
    firefox.close()

def test_selenium_addProject():
    options = Options()
    options.add_argument('-headless')
    firefox = Firefox(executable_path="./geckodriver", options=options)
    firefox.get("http://localhost:8080/app.py/")
    firefox.close()

def test_selenium_addSensor():
    options = Options()
    options.add_argument('-headless')
    firefox = Firefox(executable_path="./geckodriver", options=options)
    firefox.get("http://localhost:8080/app.py/")

    projects_button = firefox.find_element_by_id("sideBarProjects")
    projects_button.click()

    # The project must be in the database
    project_name = 'project-Test'

    """
    We must add a project here
    """

    testProjet_button = firefox.find_element_by_id(project_name)
    testProjet_button.click()

    firefox.close()


def test_selenium_accessProfil():
    options = Options()
    options.add_argument('-headless')
    firefox = Firefox(executable_path="./geckodriver", options=options)
    firefox.get("http://localhost:8080/app.py/")
    profile_button = firefox.find_element_by_name("sidebarBarProfile")
    profile_button.click()

    newName = "Kim"
    newFirstName = "Mens"
    newEmail = "kimmens@uclouvain.be"

    userName = firefox.find_element_by_id("username")
    userFirstName = firefox.find_element_by_id("userFirstName")
    userEmail = firefox.find_element_by_id("inputEmail")
    userAdminLevel = firefox.find_element_by_id("userAdminLevel")
    confirm_button = firefox.find_element_by_id("confirmButton")

    userName.clear()
    userFirstName.clear()
    userEmail.clear()

    userName.send_keys(newName)
    userFirstName.send_keys(newFirstName)
    userEmail.send_keys(newEmail)

    confirm_button.click()

    # Now check if the values in the fields are the desired values

    userName = firefox.find_element_by_id("username")
    userFirstName = firefox.find_element_by_id("userFirstName")
    userEmail = firefox.find_element_by_id("inputEmail")
    userAdminLevel = firefox.find_element_by_id("userAdminLevel")
    confirm_button = firefox.find_element_by_id("confirmButton")

    newUserName = userName.get_attribute('value')
    newUserFirstName = userFirstName.get_attribute('value')
    newUserEmail = userEmail.get_attribute('value')

    firefox.close()

    assert(newUserName = newName and newUserFirstName == newFirstName and newEmail == newUserEmail)
