from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import qrcode
from PIL import Image 

############# VARIABLES #############
URL = "https://itch.io/jam/malagajam-weekend-17/entries"
#####################################

def Get_Itchio_Data(url):
    # Start Firefox session
    driver = webdriver.Firefox()
    try:
        # Open web application
        driver.get(URL)
        # driver.execute_script("window.scrollTo(0, 540)")
        driver.execute_script("window.scrollTo(0, window.scrollMaxY)")
        driver.implicitly_wait(30)
        # Run through all elements and return individual text
        elems = driver.find_elements(By.CSS_SELECTOR,".label [href]")
        data = [(elem.get_attribute('innerHTML'),elem.get_attribute('href')) for elem in elems]
        # Close browser window
        driver.quit()
        return data
    except Exception as error:
      print("An error occurred:", error)
      driver.quit()


def Refactor_Game_Name(nombre):
    # Regex expression for ilegal windows character in files
    expression = r'[<>:"/\\|?*\x00-\x1F]'
    return re.sub(expression, ' ', nombre)

if __name__ == "__main__":

    try:
        games_data = Get_Itchio_Data(URL)
        a = games_data[0][1]
        qrs = []
        for i in range(len(games_data)):
            print(games_data[i])
            refactor_Name = Refactor_Game_Name(games_data[i][0])
            img = qrcode.make(games_data[i][1])
            # img.save(f'Qrs\{refactor_Name}.png')
            qrs.append((refactor_Name,img))
        # img.show()
        print(a)
        print(img)
        print(qrs)

    except Exception as error:
      print("MAIN")
      print("An error occurred:", error) 