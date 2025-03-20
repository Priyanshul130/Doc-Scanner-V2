#import modules 
from tkinter import *
from PIL import ImageTk, Image
import pytesseract
import cv2
import playsound
from tkinter import filedialog
from googletrans import Translator, LANGUAGES
from tkinter import messagebox
from tkinter import ttk

lang={"Hindi":"hin",
      "English":"eng",
      "Bengali":"ben",
      "Malayalam":"mal"
      }

mainWin = Tk()
mainWin.geometry("1200x600")
mainWin.title("My Scanner")
mainWin.configure(bg='turquoise')
mainWin.resizable(0,0)


img = cv2.imread("background.jpg")


def displayImage(img):
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)    
    img = img.resize((400, 400))
    dispImage = ImageTk.PhotoImage(img)
    panel.configure(image=dispImage)
    panel.image=dispImage


def OpenImg():
    global img
    imgName=filedialog.askopenfilename(title='open')
    if imgName:
        img = cv2.imread(imgName)
        displayImage(img)
        txt.delete("1.0",END)

def ScanImg():
    global img
    
    if src_lang.get()=='Source Language':
        messagebox.showwarning("Warning", "Select a source language")
    else:
        playsound.playsound('scanner.mp3')
        text = pytesseract.image_to_string(img, lang = lang[src_lang.get()])
        txt.delete(1.0,END)
        txt.insert(1.0, text)

   
def Translate():
    
    if dest_lang.get()=='Destination Language' or src_lang.get()=='Source Language':
        messagebox.showwarning("Warning", "Select language")
    else:
        scannedText=txt.get(1.0,END)
        if len(scannedText)==1:
            messagebox.showwarning("Warning", "Nothing to translate")
        else:
            srcLanguage=src_lang.get().lower()
            destLanguage=dest_lang.get()
  
            translator = Translator()
         
            translated=translator.translate(text=scannedText ,
                                            src =srcLanguage, dest =destLanguage)
            txt.delete(1.0,END)
            txt.insert(1.0, translated.text)    
    

def SaveTxt():
 
    filepath = filedialog.asksaveasfilename(defaultextension="txt")
    if not filepath:
        return
    with open(filepath, "wb") as output_file:
        text = txt.get(1.0,END)
        encoded_unicode = text.encode("utf8")
        output_file.write(encoded_unicode)
    
panel = Label(mainWin,bg="BLACK")
panel.grid(row=0,rowspan=12,padx=40,pady=30)
displayImage(img)

btnOpen = Button(mainWin, text='Open',width=25,command=OpenImg,bg='dodger blue',fg="white")
btnOpen.grid(row=13)

btnScan = Button(mainWin, text='Text Scan',width=25,command=ScanImg,bg='dodger blue',fg="white")
btnScan.grid(row=13,column=2)

btnSave = Button(mainWin, text='Save',command=SaveTxt,bg='dodger blue',fg="white",width=50)
btnSave.grid(row=15,column=1,columnspan=2)

txt = Text(mainWin,bg="white",)
txt.grid(row=0,column=1,columnspan=2,rowspan=12,padx=40,pady=30)

#--------------------------------------------------------------------
btnTranslate = Button(mainWin, text='Translate',width=25,command=Translate,bg='dodger blue',fg="white")
btnTranslate.grid(row=14,column=2)

#COMBOBOX

srclang = list(lang.keys())
src_lang = ttk.Combobox(mainWin, values= srclang, width =25)
src_lang.set('Source Language')
src_lang.grid(row=13,column=1,pady=10)

language = list(LANGUAGES.values())
dest_lang = ttk.Combobox(mainWin, values= language, width =25)
dest_lang.set('Destination Language')
dest_lang.grid(row=14,column=1,pady=10)

mainWin.mainloop()
