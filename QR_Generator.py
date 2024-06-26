import os
import qrcode
import re
import shutil
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle
from reportlab.lib.units import inch
import PIL.Image

class QRGenerator:
    def __init__(self) -> None:
        self.URL = None
        self.LOGOPATH = None
        self.WEBDRIVER = None
        self.SAVEDIRECTORY = os.getcwd()        

        self.PDFName = "Games Qrs"
        self.AddLogo = False
        self.DeleteQRFolder = False
        self.QRSIZE = 180
        self.FONTSIZE = 15
        self.PROGRESS = 0
        self.PROGRESS_MSG = "Initiating process"

    def Create_PDF(self):
        try:
            self.Change_Working_Directory()
            games_data = self.Get_Itchio_Data()
            qrs = self.Create_QR_Images(games_data)
            self.Create_PDF_With_Table(qrs)
            if(self.DeleteQRFolder):
                self.Delete_QR_Folders()
            self.PROGRESS = 100
            self.PROGRESS_MSG = "PDF with QRs created"
            
        except Exception as error:
            print("An error occurred:", error) 
            raise error

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

    def Set_Save_Directory(self, saveDirectory):
        self.SAVEDIRECTORY = saveDirectory
    
    def Get_Progress_Number(self):
        return self.PROGRESS
    
    def Get_Progress_Message(self):
        return self.PROGRESS_MSG

    def Change_Working_Directory(self):
        os.chdir(self.SAVEDIRECTORY)
        if not os.path.exists("Games QR"):
            os.mkdir("Games QR") 
        os.chdir(os.path.join(self.SAVEDIRECTORY,"Games QR"))
        print(f'New directory: {os.path.join(self.SAVEDIRECTORY,"Games QR")}')
        self.Set_Save_Directory(os.path.join(self.SAVEDIRECTORY,"Games QR"))

    def Get_Total_Entries(self, driver):
        parsed_url = urlparse(self.URL)
        parte_href = parsed_url.path
        numEntries = driver.find_elements(By.CSS_SELECTOR,f'a[href="{parte_href}"] .stat_value')[0]        
        return int(numEntries.text)

    def Get_Itchio_Data(self):
        self.PROGRESS = 10
        self.PROGRESS_MSG = f"Opening browser {self.WEBDRIVER}."
        match self.WEBDRIVER:
            case "Firefox":
                driver = webdriver.Firefox()
                scrollScript = "window.scrollTo(0, window.scrollMaxY)"
            case "Chrome":
                driver = webdriver.Chrome()
                scrollScript = "window.scrollTo(0, document.body.scrollHeight)"
            case "Microsoft Edge":
                driver = webdriver.Edge()
                scrollScript = "window.scrollTo(0, document.body.scrollHeight)"

        try:
            driver.get(self.URL)
            # driver.implicitly_wait(30)
            time.sleep(1)
            driver.execute_script(scrollScript)
            time.sleep(1)
            self.PROGRESS = 20
            self.PROGRESS_MSG = "Downloading information of the games from website."
            elems = driver.find_elements(By.CSS_SELECTOR,".label [href]")
            data = [(elem.get_attribute('innerHTML'),elem.get_attribute('href')) for elem in elems]
            lengthData = len(data)
            totalEntries = self.Get_Total_Entries(driver)
            if(totalEntries != lengthData):
                raise Exception(f"Games not retrieved correctly. Expected {totalEntries} games. Only {lengthData} obtained")

            data.sort(key=lambda elem: elem[0])
            self.PROGRESS = 30
            return data
        
        except Exception as error:
            print("An error occurred: ", error)
            raise error
        finally:
            driver.quit()


    def Refactor_Game_Name(self, name):
        # Regex expression for ilegal windows character in files
        expression = r'[<>:"/\\|?*\x00-\x1F]'
        return re.sub(expression, ' ', name).replace("&amp;","&")

    def Create_QR_Images(self, data):
        qrs = []
        if not os.path.exists("Qrs"):
            os.mkdir("Qrs") 
        self.PROGRESS = 40
        self.PROGRESS_MSG = "Creating Qrs images."

        list_len = len(data)
        for i in range(list_len):
            if( i % list_len == 0):
                self.PROGRESS += 10
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=2,
            )
            qr.add_data(data[i][1])
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            if(self.AddLogo):
                logo = PIL.Image.open(self.LOGOPATH)
                logo = logo.resize((100,100))
                pos = ((img.size[0] - logo.size[0])//2,(img.size[1] - logo.size[1])//2)
                img.paste(logo, pos)
            refactor_Name = self.Refactor_Game_Name(data[i][0])
            img.save(f'Qrs\{refactor_Name}.png')
            qrs.append((refactor_Name,img))
        
        self.PROGRESS = 80
        self.PROGRESS_MSG = f"Creating PDF with {list_len} QRs."
        return qrs

    def Create_PDF_With_Table(self, data):

        doc = SimpleDocTemplate(f"{self.PDFName}.pdf",
                            rightMargin=1,leftMargin=1,
                            topMargin=1,bottomMargin=1)
        elems = []
        rows = []
        tabStyle = [('ALIGN',(0,0),(-1,-1),'CENTER')] 
        for index, game in enumerate(data):
            image = Image(f"Qrs/{game[0]}.png",self.QRSIZE,self.QRSIZE)
            if index % 2 == 0:
                rows.append([self.Truncate_Large_Names(game[0])])
                rows.append([image])
                tabStyle.append(('FONTSIZE',(0,index),(1,index),self.FONTSIZE))
                tabStyle.append(('VALIGN',(0,index),(1,index),"BOTTOM"))
            else:
                rows[-2].append(self.Truncate_Large_Names(game[0]))
                rows[-1].append(image)
        
        
        self.PROGRESS = 90
        time.sleep(3)
        table = Table(rows, colWidths=inch*4)
        table.setStyle(TableStyle(tabStyle))
        elems.append(table)
        doc.build(elems)

    def Truncate_Large_Names(self, name: str) -> str:
        if(len(name) > 28):    
            return name[:25]+"..."
        return name

    def Delete_QR_Folders(self):
        folderPath = os.path.join(self.SAVEDIRECTORY, "Qrs")
        if os.path.isdir(folderPath):
            shutil.rmtree(folderPath)
  
if __name__ == "__main__":    
    try:
        generator = QRGenerator()
        generator.Set_Url("https://itch.io/jam/malagajam-weekend-17/entries")
        generator.Set_Logo_Path("G:\My Drive\Sincronizacion\Programacion\Python\QR_Generator_Itchio\MJW LOGO.png")
        generator.Set_Webdriver("Chrome")
        generator.Set_Delete_QR_Folder(False)
        generator.Set_Save_Directory(os.getcwd())
        generator.Create_PDF()

    except Exception as error:
      print("An error occurred: ", error) 