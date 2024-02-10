from selenium import webdriver
from selenium.webdriver.common.by import By

############# VARIABLES #############

URL = "https://itch.io/jam/malagajam-weekend-17/entries"

#####################################

def Get_Itchio_Data(url):
    # Start Firefox session
    driver = webdriver.Firefox()
    driver.maximize_window()
    # Open web application
    driver.get(URL)
    # driver.execute_script("window.scrollTo(0, 540)")
    driver.execute_script("window.scrollTo(0, window.scrollMaxY)")
    driver.implicitly_wait(30)
    # Run through all elements and return individual text
    elems = driver.find_elements(By.CSS_SELECTOR,".label [href]")
    data = {elem.get_attribute('innerHTML'):elem.get_attribute('href') for elem in elems}
    # Close browser window
    driver.quit()

    return data

if __name__ == "__main__":
    games_data = Get_Itchio_Data(URL)