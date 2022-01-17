from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
import easygui
import os


# Do I do array of dictionaries or array of account objects?
# accountsEx = {  'username':'NotADevGuy', 'password':'pass', 'email':'bob@gmail.com'  }
# Then do an array of these dicts
# account


# class Account:
#     # username, password, email, currentSkin = '', '', '', ''
#     info = {'username': '', 'password': '', 'email': '', 'currentSkin': ''}
#
#     def __init__(self, password='', email='', username='', currentSkin=''):
#         self.info['password'] = password
#         self.info['email'] = email
#         self.info['username'] = username
#         self.info['currentSkin'] = currentSkin
#         # self.password = str(password)
#         # self.email = str(email)
#
#     # def __del__(self):
#     #     print("HEY?")
#
#     def updateInfo(self, variable, value):
#         self.info[variable] = value


def main():
    accList = []

    # print("Please select your MC Alt text file!")
    # fileLoc = str(easygui.fileopenbox())
    fileLoc = "C:\\Users\\mattt\\PycharmProjects\\Minecraft-Alt-Renamer\\mc.txt"

    while not fileLoc.endswith(".txt"):
        print("Not a text file!")
        fileLoc = str(easygui.fileopenbox())

    # print("What is the format of each line?")
    # print("Example: email:password")
    # print("Available variables: email, password, username")
    # fileForm = input("Enter your format: ")
    fileForm = "email:password"

    tmp = ""
    for letter in fileForm:
        if not letter.isalpha():
            tmp += letter

    while not sameChars(tmp):
        print("What is the format of each line?")
        print("Example: email:password")
        print("Available variables: email, password, username")
        fileForm = input("Enter your format: ")

        tmp = ""
        for letter in fileForm:
            if not letter.isalpha():
                tmp += letter

    sep = tmp[0]

    fileForm = fileForm.split(sep)

    inc = 0
    with open(fileLoc, 'r') as file:
        for line in file:
            if sep in line:
                line = line.strip().split(sep)
                acc = {'username': '', 'password': '', 'email': '', 'currentSkin': ''}

                for i in range(len(fileForm)):
                    acc[fileForm[i]] = line[i]
                accList.append(acc)
                inc += 1

    selService = Service(str(os.getcwd() + "\\chromedriver.exe"))
    driver = webdriver.Chrome(service=selService)

    driver.get('https://www.minecraft.net/en-us/profile')
    delay = 5

    try:
        emailInput = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'emailField')))
        emailInput.click()
        emailInput.send_keys(Keys.CONTROL, 'a')
        emailInput.send_keys(accList[0]['email'])

        passInput = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'password')))
        passInput.click()
        passInput.send_keys(Keys.CONTROL, 'a')
        passInput.send_keys(accList[0]['password'])

        time.sleep(1)
        submitButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login']")))
        submitButton.click()

        userButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Change profile name')]")))
        userButton.click()
        while True:
            pass

        # passInput = driver.find_element(By.ID, 'password')
    except Exception as e:
        print("ERROR")
        print(e)
    # time.sleep(3)

    # emailInput.click()
    #


def sameChars(s):
    for inc in range(len(s)):
        if s[inc] != s[0]:
            return False
    return True


if __name__ == '__main__':
    main()
