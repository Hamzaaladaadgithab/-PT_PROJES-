from tkinter import *
import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox, ttk
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re  # Regex modülü

import self

from ogrenciclassfile import *

from ogretmenclass import *

from hesapolusturclassfile import *



# Toplevel, Tkinter'de ana pencerenin dışında yeni bir pencere oluşturmak için kullanılır.
# master parametresi, yeni Toplevel penceresinin hangi ana pencereye ait olduğunu belirtir. master=None varsayılan değeri, eğer bir ana pencere belirtilmezse, None olarak ayarlanmasını sağlar.




class anagirissecmeclass(Tk):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("ÖĞRENCİ YÖNETİM SİSTEMİ")
        self.geometry("900x700")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")

    # image eklemek icin

        # Başlık
        titlelog = Label(self, text="GİRİŞ SAYFASI", font=('Bold', 15), bg='#273b7a', fg='white')
        titlelog.pack(fill=X)

 #------------       image eklemek icin-------------------------------


        photostudent = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\student64.png")

        phototeacher = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\teacher64.png")

        photoaccount = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\account64.png")





# -----------Frame oluşturma -------------------



        framesecme = Frame(self,highlightbackground='#273b7a',highlightthickness=3)
        framesecme.pack(pady=30)
        framesecme.pack_propagate(False)
        framesecme.configure(width=500, height=490)

        lbl_frame=Label(framesecme, text='ÖYS’NE  HOŞ GELDİNİZ...',bg='#273b7a',fg='white',font=('Bold' , 18))
        lbl_frame.place(x=0,y=0,width=500)



        studentgiris_but=Button(framesecme, text='ÖĞRENCİ GİRİŞ' ,bg='#273b7a', fg='white' , font=('Bold',15),bd=0,command=self.ogrencicagirmaclass)
        studentgiris_but.place(x=150,y=100,width=200)

        studengiris_img=Button(framesecme,image=photostudent,bd=0)
        studengiris_img.place(x=60,y=70)



        admingiris_but=Button(framesecme, text='ÖĞRETMEN GİRİŞ' ,bg='#273b7a', fg='white' , font=('Bold' , 15),bd=0, command=self.ogretmenclasscagirma)
        admingiris_but.place(x=150,y=230,width=200)

        admingiris_img=Button(framesecme,image=phototeacher,bd=0)
        admingiris_img.place(x=60,y=200)


#, self.kayitolmafonk()


        acuontgiris_but=Button(framesecme, text='HESAB OLUŞTUR' ,bg='#273b7a', fg='white' , font=('Bold' , 15),bd=0,command=self.hesapolusturmacagirma)
        acuontgiris_but.place(x=150,y=350,width=200)

        acountgiris_img=Button(framesecme,image=photoaccount,bd=0)
        acountgiris_img.place(x=60,y=335)






    def ogrencicagirmaclass(self):

        self.withdraw()

        ogrencigirisclass(self)
        ogrenciislemlericlass(self)




    def ogretmenclasscagirma(self):

        self.withdraw()

        LoginClass(self)
        student(self)
        SifreGuncelleme(self)
        EmailGonderme(self)

    def hesapolusturmacagirma(self):

        self.withdraw()
        hesapolusturclass()




















if __name__ == "__main__":

   app=anagirissecmeclass()
   app.mainloop()
