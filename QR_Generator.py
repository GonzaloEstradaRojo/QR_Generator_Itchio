from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
import qrcode
import time

#creation of new pdf
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle
from reportlab.lib.units import inch
import PIL.Image

############# VARIABLES #############
URL = "https://itch.io/jam/malagajam-weekend-16/entries"
PDFNAME = "Games Qrs"
QRSIZE = 180
FONTSIZE = 15
LOGONAME = "MJW LOGO.png"
ADDLOGO = True
#####################################


def Get_Itchio_Data(url):
    # Start Firefox session
    driver = webdriver.Firefox()
    try:
        # Open web application
        driver.get(URL)
        # driver.execute_script("window.scrollTo(0, 540)")
        driver.implicitly_wait(30)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, window.scrollMaxY)")
        time.sleep(3)
        # Run through all elements and return individual text
        elems = driver.find_elements(By.CSS_SELECTOR,".label [href]")
        data = [(elem.get_attribute('innerHTML'),elem.get_attribute('href')) for elem in elems]
        # Close browser window
        driver.quit()
        data.sort(key=lambda elem: elem[0])
        return data
    except Exception as error:
      print("An error occurred:", error)
      driver.quit()


def Refactor_Game_Name(nombre):
    # Regex expression for ilegal windows character in files
    expression = r'[<>:"/\\|?*\x00-\x1F]'
    return re.sub(expression, ' ', nombre).replace("&amp;","&")

def Create_QR_Images(data):
    qrs = []
    if not os.path.exists("Qrs"):
        os.mkdir("Qrs") 

    for i in range(len(data)):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(data[i][1])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        if(ADDLOGO):
            logo = PIL.Image.open(LOGONAME)
            logo = logo.resize((100,100))
            pos = ((img.size[0] - logo.size[0])//2,(img.size[1] - logo.size[1])//2)
            img.paste(logo, pos)
        refactor_Name = Refactor_Game_Name(data[i][0])
        img.save(f'Qrs\{refactor_Name}.png')
        qrs.append((refactor_Name,img))
    
    return qrs

def Create_PDF_With_Table(data):

    doc = SimpleDocTemplate(f"{PDFNAME}.pdf",
                        rightMargin=1,leftMargin=1,
                        topMargin=1,bottomMargin=1)
    elems = []
    rows = []
    tabStyle = [('ALIGN',(0,0),(-1,-1),'CENTER')] 
    for index, game in enumerate(data):
        print(index, game[0])
        image = Image(f"Qrs/{game[0]}.png",QRSIZE,QRSIZE)
        if index % 2 == 0:
            rows.append([Truncate_Large_Names(game[0])])
            rows.append([image])
            tabStyle.append(('FONTSIZE',(0,index),(1,index),FONTSIZE))
            tabStyle.append(('VALIGN',(0,index),(1,index),"BOTTOM"))
        else:
            rows[-2].append(Truncate_Large_Names(game[0]))
            rows[-1].append(image)

    table = Table(rows, colWidths=inch*4)
    table.setStyle(TableStyle(tabStyle))
    elems.append(table)
    doc.build(elems)

def Truncate_Large_Names(name: str) -> str:
    if(len(name) > 28):    
        return name[:25]+"..."
    return name

if __name__ == "__main__":    
    try:
        games_data = Get_Itchio_Data(URL)
        qrs = Create_QR_Images(games_data)
        Create_PDF_With_Table(qrs)

    except Exception as error:
      print("An error occurred:", error) 