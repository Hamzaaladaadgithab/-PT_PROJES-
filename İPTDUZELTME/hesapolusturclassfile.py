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


# Toplevel, Tkinter'de ana pencerenin dışında yeni bir pencere oluşturmak için kullanılır.
# master parametresi, yeni Toplevel penceresinin hangi ana pencereye ait olduğunu belirtir. master=None varsayılan değeri, eğer bir ana pencere belirtilmezse, None olarak ayarlanmasını sağlar.




class hesapolusturclass(Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("ÖĞRENCİ YÖNETİM SİSTEMİ")
        self.geometry("800x650")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")


        # Başlık
        titlelog = Label(self, text="HESAP OLUŞTURMA SİSTEMİ",  font=('Bold', 15), bg='#273b7a', fg='white')
        titlelog.pack(fill=X)


    # image eklemek icin
    # Böylece, PhotoImage  nesnesi     artık    grçici  değil   ve  çöp  toplayıcı  tarafından   temizlenmez. =

    # Keep a reference to avoid garbage collection


#-----------------frame oluşturma ------------------------

        framehesap = Frame(self,highlightbackground='#273b7a',highlightthickness=3)
        framehesap.pack(pady=30)
        framehesap.pack_propagate(False)
        framehesap.configure(width=580, height=590)





        photoaccount = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\account64.png")

        sifre_goster_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\hidden.png")

        user_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\profile-user.png")

        mail_img= PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\mail.png")

        acountgiris_img=Label(framehesap,image=photoaccount,bd=0)
        acountgiris_img.place(x=280,y=5)

        # ------------methods---------------------------------------

        def showhide_sifre():
             if self.txt_sifre['show'] == '*':

                self.txt_sifre.config(show='')
             else:
                 self.txt_sifre.config(show='*')

        # ------------ icon yada image ekelme şifre gizlemek ve gostermek icin ve user img --------------------

        show_hide_but = Button(framehesap, image=sifre_goster_img, bd=0, command=showhide_sifre)
        show_hide_but.place(x=475, y=290)

        userimg_label = Label(framehesap, image=user_img, bd=0)
        userimg_label.place(x=478, y=100)


        mail_img_label = Label(framehesap, image=mail_img, bd=0)
        mail_img_label.place(x=478, y=190)



        self.label_kullaniciadi = Label(framehesap, text="KULLANICI ADI:" ,font=('Bold',15),fg='#273b7a')
        self.label_kullaniciadi.place(x=10, y=100)

        self.txt_kullaniciadi = Entry(framehesap,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.txt_kullaniciadi.place(x=170, y=100, width=300)



        self.label_eposta = Label(framehesap, text="E-POSTA:",font=('Bold',15),fg='#273b7a')
        self.label_eposta.place(x=60, y=190)

        self.txt_eposta = Entry(framehesap,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.txt_eposta.place(x=170, y=190, width=300)




        self.label_sifre = Label(framehesap, text="ŞİFRE:",font=('Bold',15),fg='#273b7a')
        self.label_sifre.place(x=90, y=290)

        self.txt_sifre = Entry(framehesap,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2,show='*')
        self.txt_sifre.place(x=170, y=290, width=300)




        self.butgonder = Button(framehesap, text="KAYIT ET", font=('Bold',15),bg='#273b7a',fg='white', command=self.kayitol)
        self.butgonder.place(x=210, y=370, width=250, height=40)

        self.butdon = Button(framehesap, text="GİRİŞ SAYFASINA DÖN",  font=('Bold',15),bg='#273b7a',fg='white', command=self.giris_sayfasina_don)
        self.butdon.place(x=210, y=500, width=250, height=40)



        # # mainloop() çağrısı, Tkinter uygulamasının penceresini görüntülemek,
# #kullanıcı etkileşimini beklemek ve olayları işlemek için gereklidir.

        self.mainloop()

    def giris_sayfasina_don(self):
        self.master.deiconify()  # LoginClass penceresini yeniden göster
        self.destroy()  # Şifre Güncelleme penceresini kapat

    def kayitol(self):
        try:
            kullaniciadi = self.txt_kullaniciadi.get()
            eposta = self.txt_eposta.get()
            sifre = self.txt_sifre.get()

            # Eğer herhangi bir alan boşsa hata mesajı göster ve metodu sonlandır  return ile sonlandırılır

            if not kullaniciadi or not eposta or not sifre:
                messagebox.showerror("Hata", "Kullanıcı adı, e-posta ve şifre alanları boş olamaz!")
                return


           #Doluysa Devam Et: Eğer tüm alanlar doluysa, veritabanı bağlantısını aç, SQL sorgusunu çalıştır ve veriyi ekle.


            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')
            cur = con.cursor()
            cur.execute("INSERT INTO email (kullaniciadi, eposta, sifre) VALUES (%s, %s, %s)", (kullaniciadi, eposta, sifre))
            con.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi!")

        except Exception as error:
            messagebox.showerror("Hata", f"Veritabanına kayıt eklenirken bir hata oluştu: {error}")

        finally:
           if 'con' in locals():
              con.close()







# if __name__== "__main__":
#
#     objhesp=hesapolusturclass()