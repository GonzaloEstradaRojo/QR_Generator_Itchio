from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
import qrcode
import time
import shutil

#creation of new pdf
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle
from reportlab.lib.units import inch
import PIL.Image

############# VARIABLES #############
URL = "https://itch.io/jam/malagajam-weekend-17/entries"
PDFNAME = "Games Qrs"
QRSIZE = 180
FONTSIZE = 15
LOGONAME = "MJW LOGO.png"
ADDLOGO = True
#####################################

class QRGenerator:
    def __init__(self) -> None:
        self.URL = None
        self.LOGOPATH = None
        self.WEBDRIVER = None
        

        self.PDFName = "Games Qrs"
        self.AddLogo = False
        self.DeleteQRFolder = False
        self.QRSIZE = 180
        self.FONTSIZE = 15

    def Create_PDF(self):
        try:
            games_data = self.Get_Itchio_Data()
            qrs = self.Create_QR_Images(games_data)
            self.Create_PDF_With_Table(qrs)

        except Exception as error:
            print("An error occurred:", error) 

    def Set_Url(self, newUrl):
        self.URL = newUrl

    def Set_Logo_Path(self, newPath):
        self.LOGOPATH = newPath

    def Set_Webdriver(self, newdriver):
        self.WEBDRIVER = newdriver

    def Set_Add_Logo(self, addNewLogo, newPath):
        self.AddLogo = addNewLogo
        self.Set_Logo_Path(newPath)

    def Set_Delete_QR_Folder(self, deleteFolder):
        self.DeleteQRFolder = deleteFolder

    def Get_Itchio_Data(self):
        # Start Firefox session
        driver = webdriver.Firefox()
        try:
            driver.get(self.URL)
            driver.implicitly_wait(30)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, window.scrollMaxY)")
            time.sleep(3)

            elems = driver.find_elements(By.CSS_SELECTOR,".label [href]")
            data = [(elem.get_attribute('innerHTML'),elem.get_attribute('href')) for elem in elems]

            driver.quit()
            data.sort(key=lambda elem: elem[0])
            return data
        
        except Exception as error:
            print("An error occurred:", error)
            driver.quit()


    def Refactor_Game_Name(self, name):
        # Regex expression for ilegal windows character in files
        expression = r'[<>:"/\\|?*\x00-\x1F]'
        return re.sub(expression, ' ', name).replace("&amp;","&")

    def Create_QR_Images(self, data):
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
            refactor_Name = self.Refactor_Game_Name(data[i][0])
            img.save(f'Qrs\{refactor_Name}.png')
            qrs.append((refactor_Name,img))
        return qrs

    def Create_PDF_With_Table(self, data):

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
                rows.append([self.Truncate_Large_Names(game[0])])
                rows.append([image])
                tabStyle.append(('FONTSIZE',(0,index),(1,index),FONTSIZE))
                tabStyle.append(('VALIGN',(0,index),(1,index),"BOTTOM"))
            else:
                rows[-2].append(self.Truncate_Large_Names(game[0]))
                rows[-1].append(image)

        table = Table(rows, colWidths=inch*4)
        table.setStyle(TableStyle(tabStyle))
        elems.append(table)
        doc.build(elems)

    def Truncate_Large_Names(self, name: str) -> str:
        if(len(name) > 28):    
            return name[:25]+"..."
        return name


if __name__ == "__main__":    
    try:
        generator = QRGenerator()
        generator.Set_Url("https://itch.io/jam/malagajam-weekend-17/entries")
        generator.Set_Logo_Path("MJW LOGO.png")
        generator.Set_Webdriver("Firefox")
        generator.Create_PDF()
        print(generator.URL, generator.LOGOPATH, generator.WEBDRIVER)

    except Exception as error:
      print("An error occurred:", error) 