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

    # Next 3 Lines for headless
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=selService, options=options)

    # For !headless
    # driver = webdriver.Chrome(service=selService)

    delay = 5

    for user in accList:
        try:
            # TODO figure out why every account has been migrated to microsoft even though they haven't
            driver.get('https://www.minecraft.net')  # en-us/login or en-us/profile
            driver.delete_all_cookies()

            loginbutton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//a[@href='https://www.minecraft.net/en-us/login']")))  # data-bi-name="log in"
            loginbutton.click()

            emailInput = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'emailField')))
            emailInput.click()
            emailInput.send_keys(Keys.CONTROL, 'a')
            emailInput.send_keys(user['email'])

            passInput = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'password')))
            passInput.click()
            passInput.send_keys(Keys.CONTROL, 'a')
            passInput.send_keys(user['password'])

            time.sleep(1)
            submitButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login']")))
            submitButton.click()

            userButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Change profile name')]")))
            userButton.click()
            print(user['email'] + " was successful\n")

        except Exception as e:
            print(user['email'] + " ERROR")
            print()


def sameChars(s):
    for inc in range(len(s)):
        if s[inc] != s[0]:
            return False
    return True


if __name__ == '__main__':
    main()
