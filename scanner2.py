#DEVELOPED BY <PRIYANSHUL SHARMA>
#WEBPAGE Priyanshul.is-a.dev
from tkinter import *
from PIL import ImageTk,Image
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
      "Malayanam":"mal"
      }


window=Tk()
window.geometry("1200x600")
window.title("my scanner")
window.configure(bg="turquoise")

#this revoes the maximixe button
window.resizable(0,0)

#load image
img=cv2.imread("background.jpg")

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
    #if source lang is not selected
    if src_lang.get()=="source language":
        messagebox.showwarning("warning","select a source language")
    else:
        playsound.playsound("scanner.mp3")
        text = pytesseract.image_to_string(img, lang = lang[src_lang.get()])
        txt.delete(1.0,END)
        txt.insert(1.0, text)


def Translate():
    #if language is not selected
    if dest_lang.get()=="destination language" or src_lang.get()=="source language":
        
        messagebox.showwarning("warning","selesct a language")
    else:
        scanned_text=txt.get(1.0,END)

        if len(scanned_text)==1:
            messagebox.showwarning("warning","nothing to Translate")

        else:
            source_lang=src_lang.get().lower()
        
            destination_lang=dest_lang.get()
        
            translator=Translator()
        
            translated=translator.translate(text=scanned_text , src = source_lang , des = destination_lang)
            txt.delete(1.0,END)
            txt.insert(1.0,translated.text)
            
        


def SaveTxt():
    #"""Save the current file as a new file."""
    filepath = filedialog.asksaveasfilename(defaultextension="txt")
    if not filepath:
        return
    with open(filepath, "wb") as output_file:
        text = txt.get("1.0",END)
        encoded_unicode = text.encode("utf8")
        output_file.write(encoded_unicode)





#gui
panel=Label(window,bg="BLACK")
panel.grid(row=0,rowspan=12,padx=40,pady=30)
displayImage(img)

button_open=Button(window,text="OPEN",width=25,command=OpenImg,bg="dodger blue",fg="white")
button_open.grid(row=13)

button_scan=Button(window,text="TEXT SCAN",width=25,command=ScanImg,bg="dodger blue",fg="white")
button_scan.grid(row=13,column=2)

button_trans=Button(window,text="TRANSLATE",width=25,command=Translate,bg="dodger blue",fg="white")
button_trans.grid(row=14,column=2)

button_save=Button(window,text="SAVE",width=50,command=SaveTxt,bg="dodger blue",fg="white")
button_save.grid(row=15,column=1,columnspan=2)

txt=Text(window,bg="white")
txt.grid(row=0,column=1,columnspan=2,rowspan=12,padx=40,pady=30)

#combobox
srclang=list(lang.keys())

src_lang=ttk.Combobox(window,values=srclang,width=25)
src_lang.set("source language")

src_lang.grid(row=13,column=1,pady=10)

destlang=list(LANGUAGES.values())
dest_lang=ttk.Combobox(window,values=destlang,width=25)
dest_lang.set("destination language")

dest_lang.grid(row=14,column=1,pady=10)


window.mainloop()














