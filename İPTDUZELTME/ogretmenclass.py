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





# EmailGonderme sınıfı Toplevel sınıfından miras alır
class EmailGonderme(Toplevel):

    def __init__(self, master=None):

        super().__init__(master)
        self.title("OGRENCİ YONETİM SİSTEMİ")
        self.geometry("850x600")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")

        # Başlık
        titlelog = Label(self, text="ŞİFRE HATIRLATMA  SİSTEMİ",font=('Bold', 15), bg='#273b7a', fg='white')
        titlelog.pack(fill=X)

        self.label_kullaniciadi = Label(self, text="KULLANICI ADI:",font=('Bold',15),fg='#273b7a')
        self.label_kullaniciadi.place(x=15, y=140)

        self.txt_kullaniciadi = Entry(self,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.txt_kullaniciadi.place(x=168, y=140, width=330)

        self.label_eposta = Label(self, text=" E-POSTA: ",font=('Bold',15),fg='#273b7a')
        self.label_eposta.place(x=50, y=260)

        self.txt_eposta = Entry(self,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.txt_eposta.place(x=168, y=260, width=330)

        self.butgonder = Button(self, text="GÖNDER", font=('Bold',15),bg='#273b7a',fg='white', command=self.butgonder_click)
        self.butgonder.place(x=225, y=350,width=240)

        butdon = Button(self, text="GİRİŞ SAYFASİNA DÖN", font=('Bold',15),bg='#273b7a',fg='white', command=self.return_to_login)
        butdon.place(x=225, y=430)

        # image eklemek icin    //  fg= parametresi, butonun metin rengini ayarlar.


        photo = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\mailgonder.png")
        panel = Label(self, image=photo)
        panel.photo = photo  # Keep a reference to avoid garbage collection
        panel.place(x=600, y=105)

        user_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\profile-user.png")

        mail_img= PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\mail.png")



        userimg_label = Label(self, image=user_img, bd=0)
        userimg_label.place(x=504, y=140)


        mail_img_label = Label(self, image=mail_img, bd=0)
        mail_img_label.place(x=502, y=260)



        # # mainloop() çağrısı, Tkinter uygulamasının penceresini görüntülemek,
        # #kullanıcı etkileşimini beklemek ve olayları işlemek için gereklidir.

        self.mainloop()



    def butgonder_click(self):
        kullaniciadi = self.txt_kullaniciadi.get()
        eposta = self.txt_eposta.get()

        # E-posta adresi doğrulama regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not kullaniciadi or not eposta:
            messagebox.showwarning("Uyarı", "Lütfen kullanıcı adı ve e-posta adresinizi giriniz.")
            return

        if not re.match(email_regex, eposta):
            messagebox.showwarning("Uyarı", "Lütfen geçerli bir e-posta adresi giriniz.")
            return

        try:
            con = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="ogrenci"
            )
            cursor = con.cursor()
            sql = "SELECT * FROM email WHERE kullaniciadi=%s AND eposta=%s"
            cursor.execute(sql, (kullaniciadi, eposta))
            result = cursor.fetchone()

            if result:
                self.send_mail(result[1], result[2])
                messagebox.showinfo("Bilgi", "Şifreniz mail adresinize gönderilmiştir.")
                self.destroy()
            else:
                messagebox.showwarning("Uyarı", "Böyle bir kullanıcı bulunmamaktadır.")
        except Exception as e:
            messagebox.showerror("Hata", f"Mail gönderme hatası: {e}")

        finally:
           if 'con' in locals():
              con.close()



    def send_mail(self, eposta, sifre):
        # E-posta gönderme ayarlari
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        mail_adres = "aladaada5105390@gmail.com"
        mail_sifre = "hodoqltynriynbar"

        konu = "Şifre Hatırlatma Mail"
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # E-posta icerigi
        yaz = f"Sayın : \n\nBizden {formatted_datetime} tarihinde şifre hatırlatma talep ettiniz.\nŞifreniz: {sifre}\n\nİyi günler..."

        msg = MIMEMultipart()
        msg['From'] = mail_adres
        msg['To'] = eposta
        msg['Subject'] = konu
        msg.attach(MIMEText(yaz, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(mail_adres, mail_sifre)
                server.sendmail(mail_adres, eposta, msg.as_string())
        except Exception as e:
            messagebox.showerror("Hata", f"E-posta gönderme hatası: {e}")

    def return_to_login(self):
        self.master.master.deiconify()  # LoginClass penceresini yeniden göster
        self.destroy()  # EmailGonderme penceresini kapat


# ------------------------------------------------------------------------------------------------------

# üst sınıfın (superclass) yapıcı yöntemini çağırmak için kullanılır.
# alt sınıf bir Tkinter penceresi oluştururken, super().__init__() ifadesi,
# Tk sınıfının yapıcı yöntemini çağırarak alt sınıfın bir Tkinter penceresi olarak başlatılmasını sağlar.
# master parametresi, Tkinter'daki birçok widget ve pencere için ana (parent) widget veya pencereyi belirtmek için kullanılır


class SifreGuncelleme(Toplevel):

    def __init__(self, master=None):
        super().__init__(master)  # # Üst sınıfın (Toplevel) __init__ metodunu çağır ve master parametresini geçir
        self.title("OGRENCİ YONETİM SİSTEMİ")
        self.geometry("900x550")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")

        sifre_goster_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\hidden.png")
        user_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\profile-user.png")

        titlelog = Label(self, text="ŞİFRE GÜNCELLEME SİSTEMİ",  font=('Bold', 15), bg='#273b7a', fg='white')
        titlelog.pack(fill=X)

        lbl1 = Label(self, text=" KULLANICI ADI:  ", font=('Bold',15),fg='#273b7a')
        lbl1.place(x=8, y=130)

        lbl2 = Label(self, text=" YENİ ŞİFRE :",font=('Bold',15),fg='#273b7a')
        lbl2.place(x=30, y=238)




        lbl1 = Label(self,image=user_img, font=('Bold',15),fg='#273b7a')
        lbl1.place(x=520, y=127)

        lbl2 = Label(self,image=sifre_goster_img,font=('Bold',15),fg='#273b7a')
        lbl2.place(x=520, y=235)







        self.entrynewusername = Entry(self,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.entrynewusername.place(x=180, y=130, width=330)

        self.entrynewpassword = Entry(self,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.entrynewpassword.place(x=180, y=236, width=330)

        butguncelle = Button(self, text=" ŞİFREYİ  GÜNCELLE  ",font=('Bold',15),bg='#273b7a',fg='white', command=self.sifre_guncelle_onayla)
        butguncelle.place(x=230, y=320)

        butdon = Button(self, text="GİRİŞ SAYFASİNA DÖN",font=('Bold',15),bg='#273b7a',fg='white', command=self.geri_to_login)
        butdon.place(x=640, y=505)

        buthatirlatma = Button(self, text=" Beni E-posta İle Hatırlat",font=('Bold',15),bg='#273b7a',fg='white',
                               command=lambda: [self.withdraw(), self.emailhatirfonk()])
        buthatirlatma.place(x = 230, y = 400)

       # x = 230, y = 400


        # image eklemek icin

        photo = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\private-account.png")
        panel = Label(self, image=photo)
        panel.photo = photo  # Keep a reference to avoid garbage collection
        panel.place(x=630, y=120)


        # # mainloop() çağrısı, Tkinter uygulamasının penceresini görüntülemek,
        # #kullanıcı etkileşimini beklemek ve olayları işlemek için gereklidir.

        self.mainloop()






    def sifre_guncelle_onayla(self):
        try:
            kullaniciadi = self.entrynewusername.get()
            sifre = self.entrynewpassword.get()

            if not kullaniciadi or not sifre:
                messagebox.showerror("Hata", "Kullanıcı adı ve yeni şifre alanları boş bırakılamaz!")
                return

            con = pymysql.connect(host="localhost", user="root", password="", database="ogrenci")
            cursor = con.cursor()
            sql = "UPDATE email SET sifre=%s WHERE kullaniciadi=%s"

            cursor.execute(sql, (sifre, kullaniciadi))
            con.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Başarılı", "Şifre başarıyla güncellendi!")
            else:
                messagebox.showerror("Hata", "Kullanıcı adı bulunamadı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")


        finally:
           if 'con' in locals():
              con.close()






    def emailhatirfonk(self):
        EmailGonderme(self)

    def geri_to_login(self):
        self.master.deiconify()  # LoginClass penceresini yeniden göster
        self.destroy()  # Şifre Güncelleme penceresini kapat


# --------------------------------------------------------------------------------------------------------------------





class student(Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.geometry('1350x690+1+1')
        self.title('OGRENCİ YONETİM SİSTEMİ')
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")
        self.configure(background="silver")
        self.resizable(False, False)

        title = Label(self, text='/--OGRENCİ KAYİT SİSTEMİ--/', bg='#273b7a', font=('Bold', 15), fg='white')
        title.pack(fill=X)

        # -------bu variaballar entrydeki yazdığımız veriler saklanır

        self.ogrencino_var = StringVar()

        self.sifre_var = StringVar()

        self.name_var = StringVar()

        self.cinsiyet_var = StringVar()

        self.mail_var = StringVar()

        self.telefon_var = StringVar()

        self.yas_var = StringVar()

        self.class_var = StringVar()

        self.silme_var = StringVar()

        self.arama_var = StringVar()

        self.arama_by_id_name_var = StringVar()




        # (frame olusturma  labels and entrys bolumu yani ogrenci bilgileri icin yani ana window  bolumleri yada kısımları )

        manage_frame = Frame(self, bg='white', highlightbackground='#273b7a', highlightthickness=2)
        manage_frame.place(x=1137, y=30, width=210, height=440)

        title = Label(manage_frame, text='OGRENCİ BİLGİLERİ : ', bg='#273b7a', fg='white')
        title.pack()

        lbl_ogrno = Label(manage_frame, text='ÖĞRENCİ NO:', bg='white')
        lbl_ogrno.pack()

        ogrno_entry = Entry(manage_frame, textvariable=self.ogrencino_var, bd='2')
        ogrno_entry.pack()

        lbl_sifre = Label(manage_frame, text='ŞİFRE :', bg='white')
        lbl_sifre.pack()

        sifre_entry = Entry(manage_frame, textvariable=self.sifre_var, bd='2')
        sifre_entry.pack()

        lbl_name = Label(manage_frame, bg='white', text='ADI VE SOYADI:')
        lbl_name.pack()
        name_entry = Entry(manage_frame, textvariable=self.name_var, bd='2')
        name_entry.pack()

        lbl_cinsiyet = Label(manage_frame, text='CİNSİYET:', bg='white')
        lbl_cinsiyet.pack()

        combobox_cinsiyet = ttk.Combobox(manage_frame, textvariable=self.cinsiyet_var)
        combobox_cinsiyet['values'] = ('Kadın', 'Erkek')
        combobox_cinsiyet.pack()


        lbl_mail = Label(manage_frame, bg='white', text='E-Posta:')
        lbl_mail.pack()
        mail_entry = Entry(manage_frame, textvariable=self.mail_var, bd='2')
        mail_entry.pack()

        lbl_telefon = Label(manage_frame, bg='white', text='TELEFON NO:')
        lbl_telefon.pack()
        telefon_entry = Entry(manage_frame, textvariable=self.telefon_var, bd='2')
        telefon_entry.pack()

        lbl_yas = Label(manage_frame, bg='white', text='YAŞ:')
        lbl_yas.pack()
        yas_entry = Entry(manage_frame, textvariable=self.yas_var, bd='2')
        yas_entry.pack()

        lbl_class = Label(manage_frame, bg='white', text='ÖĞRENCİ SINIFI:')
        lbl_class.pack()

        class_entry = Entry(manage_frame, textvariable=self.class_var, bd='2')
        class_entry.pack()

        lbl_silme = Label(manage_frame, fg='red', bg='white', text='OGRENCİ NAME İLE SİL')
        lbl_silme.pack()

        silme_entry = Entry(manage_frame, textvariable=self.silme_var, bd='2')
        silme_entry.pack()

        # buttons olusturma

        button_frame = Frame(self, bg='white', highlightbackground='#273b7a', highlightthickness=2)
        button_frame.place(x=1137, y=434, width=210, height=2560)

        title2 = Label(button_frame, text='--KONTROL PANELİ--', fg='white', bg='#273b7a')
        title2.pack()
        title2.pack(fill=X)

        add_btn = Button(button_frame, text='OGRENCİ EKLEME', bg='#273b7a', fg='white', command=self.conveekle)
        add_btn.place(x=33, y=30, width=170, height=30)

        udate_btn = Button(button_frame, text='OGRENCİ BİLGİLERİ DUZELTME', bg='#273b7a', fg='white',command=self.update)
        udate_btn.place(x=33, y=70, width=170, height=30)

        delete_btn = Button(button_frame, text='OGRENCİ SİL ', bg='#273b7a', fg='white', command=self.delete)
        delete_btn.place(x=33, y=110, width=170, height=30)

        clear_btn = Button(button_frame, text='GİRİŞ ALANDAKİ VERİLER SİL', bg='#273b7a', fg='white', command=self.clear)
        clear_btn.place(x=33, y=150, width=170, height=30)

        exit_btn = Button(button_frame, text='ÇIKIŞ YAP', bg='#273b7a', fg='white', command=self.exit_fonk)
        exit_btn.place(x=33, y=185, width=170, height=30)



        donme_btn = Button(button_frame, text='GİRİŞ SAYFASINA DÖN', bg='#273b7a', fg='white', command=self.donmefonk)
        donme_btn.place(x=33, y=220, width=170, height=30)













        # search işlemleri  ve arama ici fream(yani ana window den ayrı bir kısım olusturma ) olusturma

        search_frame = Frame(self, bg='white', highlightbackground='#273b7a', highlightthickness=3)
        search_frame.place(x=1, y=30, width=1134, height=50)

        # -------------------------tarih ve saat icin ------------------

        current_datetime = datetime.now()

        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        tarih_label = Label(search_frame, text='Tarih ve Saat:', font=('Arial', 15))
        tarih_label.place(x=4, y=12)

        datetime_label = Label(search_frame, text=formatted_datetime, font=('Arial', 15))
        datetime_label.place(x=130, y=12)

        # -----------------------------------------------------------------------------------------------------------

        lbl_search = Label(search_frame, text='ÖĞRENCİ ARAMAK İCİN', bg='white')
        lbl_search.place(x=999, y=12)

        combo_search = ttk.Combobox(search_frame, textvariable=self.arama_by_id_name_var, justify='right')
        combo_search['value'] = ('ogrencino', 'name')
        combo_search.place(x=850, y=12)

        search_Entry = Entry(search_frame, textvariable=self.arama_var, bd='2')  # bu entry name ve id veriler tutuyor aramak için
        search_Entry.place(x=700, y=12)

        search_btn = Button(search_frame, text='arama', bg='#273b7a', fg='white', command=self.aramafonk_ogrno_name)
        search_btn.place(x=580, y=12, width=100, height=25)





        # verileri gosterme icin kod satırları
        #  Dietals_frame   ana window den bır kısımdır yani bu kısımı olan  temsil eder  yani veriler gostermek ve diğer işlemler goruntulemek icin

        Dietals_frame = Frame(self, bg='#273b7a')

        Dietals_frame.place(x=1, y=84, width=1134, height=600)

        scroll_x = Scrollbar(Dietals_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Dietals_frame, orient=VERTICAL)


        # student_table  bu varibal Dietals_frame deki   detayıleri ve  işlemleri emsil eder  yani deiğişikleri vs.
        # Treeview bileşeninin oluşturulması


        self.student_table = ttk.Treeview(Dietals_frame, columns=(
            'ogrencino', 'sifre', 'name', 'cinsiyet', 'mail', 'telefon', 'yas', 'class'),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        self.student_table.place(x=18, y=4, width=1130, height=582)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table['show'] = 'headings'  # headings yani label yada adres gibi
        self.student_table.heading('ogrencino', text='ÖĞRENCİ NO')
        self.student_table.heading('sifre', text='ŞİFRE')
        self.student_table.heading('name', text='ADI VE SOYADI')
        self.student_table.heading('cinsiyet', text='CİNSİYET')
        self.student_table.heading('mail', text='E-POSTA')
        self.student_table.heading('telefon', text='TELEFON')
        self.student_table.heading('yas', text='YAŞ')
        self.student_table.heading('class', text='SINIF')

        self.student_table.column('ogrencino', width=50)
        self.student_table.column('sifre', width=20)
        self.student_table.column('name', width=100)
        self.student_table.column('cinsiyet', width=50)
        self.student_table.column('mail', width=100)
        self.student_table.column('telefon', width=70)
        self.student_table.column('yas', width=70)
        self.student_table.column('class', width=100)

        self.student_table.bind("<ButtonRelease-1>", self.get_goster)



        # --------------database olusturma--------------------------
        self.getveriler_all()  # verileri ugulamada gostermek için bu çagırma  ile yani genclleme gibi


        self.mainloop()








    # bu method mysql bağlanır ve entrydeki yazdğımız veriler tadabase yani ogrencitabluna eklenir

    def donmefonk(self):

        self.master.deiconify()  # LoginClass penceresini yeniden göster
        self.destroy()  # Şifre Güncelleme penceresini kapat

    def conveekle(self):

        try:

            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')

            cur = con.cursor()
            cur.execute("insert into ogrencidata values(%s,%s,%s,%s,%s,%s,%s,%s)", (

                self.ogrencino_var.get(),
                self.sifre_var.get(),
                self.name_var.get(),
                self.cinsiyet_var.get(),
                self.mail_var.get(),
                self.telefon_var.get(),
                self.yas_var.get(),
                self.class_var.get(),

            ))

            con.commit()

            self.getveriler_all()  # bu cağırma  veriler gostermek icin kullanılır yani  veriler databaseye sakladıktan sonra ana widow yani  ugulamda gosterir
            self.clear()



        except Exception as error:
            messagebox.showerror("Hata:", f"conveekle methodunda  bir hata oluştu: {error}")

        finally:
           if 'con' in locals():
               con.close()

    # -------- bu method databasedeki verileri getirmek  için ugulamada gostermek için yani sutdunet_table kısımında yani variler gostermek kısımında -----------------

    def getveriler_all(self):

        try:

            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')
            cur = con.cursor()

            cur.execute('select * from ogrencidata')

            rows = cur.fetchall()

            if len(rows) != 0:

                self.student_table.delete(*self.student_table.get_children())

                for row in rows:
                    self.student_table.insert("", 'end', values=row)

                con.commit()



        except Exception as error:
            messagebox.showerror("Hata:", f"getveriler_all methodunda  bir hata oluştu: {error}")




        finally:
            if 'con' in locals():
                 con.close()

            # bu method silme adı ile entryde  yazdığımız nameye  gore silme yapılır  hem ana window= pencerye yani ugulamada hemde databesa deki verileri siler

    def delete(self):

        try:
            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')

            cur = con.cursor()
            cur.execute('delete from   ogrencidata where name = %s', self.silme_var.get())

            con.commit()
            self.getveriler_all()





        except Exception as error:
            messagebox.showerror("Hata:", f" delete methodunda  bir hata oluştu: {error}")



        finally:
            if 'con' in locals():
                con.close()

            # -----------------------Entrydeki verileri boşaltmak için bu method -----------------------

    def clear(self):

        self.ogrencino_var.set('')
        self.sifre_var.set('')
        self.name_var.set('')
        self.cinsiyet_var.set('')
        self.mail_var.set('')
        self.telefon_var.set('')
        self.yas_var.set('')
        self.class_var.set('')

    # bu methode student_table kısmında veriler antrydeki gostermek için  satırlara gore

    def get_goster(self, ev):  # ev = event = bind bir olay

         try:

                    goster_row = self.student_table.focus()
                    contents = self.student_table.item(goster_row)

                    # student_table kısmında veriler entry'deki göstermek için satırlara göre satıra bastığımda
                    row = contents.get('values', [])

                    # row'un boş olup olmadığını ve yeterli sayıda öğe içerip içermediğini kontrol edin
                    if not row or len(row) < 8:
                        messagebox.showerror("Hata", "Seçilen satırda eksik veya geçersiz veri var!")
                        return

                    self.ogrencino_var.set(row[0])
                    self.sifre_var.set(row[1])
                    self.name_var.set(row[2])
                    self.cinsiyet_var.set(row[3])
                    self.mail_var.set(row[4])
                    self.telefon_var.set(row[5])
                    self.yas_var.set(row[6])
                    self.class_var.set(row[7])


         except Exception as error:
            messagebox.showerror("Hata:", f"get_goster  bir hata oluştu: {error}")



    # ogrenciler bilgileri guncellemek için yani duzeltme

    # where  ogrencino guncellenmez cunku buna gore belgileri guncelliyouruz eğer onu guncelemek istiyorsak id  ile yaparız


    def update(self):

            try:
                con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')
                cur = con.cursor()
                cur.execute("update ogrencidata set sifre=%s, name=%s, cinsiyet=%s, mail=%s, telefon=%s, yas=%s,class=%s where ogrencino=%s",(

                        self.sifre_var.get(),
                        self.name_var.get(),
                        self.cinsiyet_var.get(),
                        self.mail_var.get(),
                        self.telefon_var.get(),
                        self.yas_var.get(),
                        self.class_var.get(),
                        self.ogrencino_var.get()   #son yada where sonraki verigul yazmıyoruz
                    ))
                con.commit()

                self.getveriler_all()  # bu çağırma veriler göstermek için kullanılır, yani veriler databaseye sakladıktan sonra ana window'da yani uygulamada gösterir
                self.clear()

            except Exception as error:
                print("Hata:", error)
                messagebox.showerror("Hata:", "Bir hata oluştu, güncelleme yapılamadı.")

            finally:
                if 'con' in locals():
                    con.close()






# bu method id veya name ile aramak için

    def aramafonk_ogrno_name(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')
            cur = con.cursor()

            # Kullanıcıdan alınan sütun adını kontrol et
            valid_columns = ['ogrencino', 'sifre', 'name', 'cinsiyet', 'mail', 'telefon', 'yas', 'class']
            column_name = self.arama_by_id_name_var.get()

            if column_name not in valid_columns:
                messagebox.showerror("Hata", "Geçersiz sütun adı!")
                return

            # SQL sorgusunu parametreler aracılığıyla oluştur
            query = "SELECT * FROM ogrencidata WHERE {} LIKE %s".format(column_name)

            # Kullanıcı girişini parametre olarak ekleyerek sorguyu çalıştır
            cur.execute(query, ('%' + self.arama_var.get() + '%',))

            rows = cur.fetchall()

            if len(rows) != 0:
                self.student_table.delete(*self.student_table.get_children())

                for row in rows:
                    self.student_table.insert("", 'end', values=row)
                con.commit()
            else:
                messagebox.showinfo("Arama Sonucu", "Bu kullanıcı bulunamadı...")


        except Exception as error:
            messagebox.showerror("Hata", f"aramafonk_ogrno_name methodunda bir hata oluştu: {error}")
        finally:
            if 'con' in locals():
                con.close()

    def exit_fonk(self):

        isYesNoCancel = messagebox.askyesnocancel("---Çikiş---", "Uygulamayi kapatmak istiyor musunuz?")
        if isYesNoCancel is not None:
            if isYesNoCancel:
                # Evet seçeneği seçildiyse uygulamayı kapat
                self.destroy()
            else:
                # Hayır seçeneği seçildiyse hiçbir işlem yapma
                pass












# ----------------------------- ana classs ------------------------------------------------
# Tk sınıfı ana pencereyi oluşturmak için kullanılır.

# LoginClass sınıfı, Tk sınıfından miras alır. Bu, LoginClass sınıfının bir Tkinter ana penceresi gibi davranmasını sağlar.

class LoginClass(Toplevel):

    def __init__(self , master=None):
        super().__init__(master)
        self.geometry("900x650")
        self.title("OGRENCİ YONETİM SİSTEMİ")
        self.resizable(False, False)
        self.config(background='#D5DBDB')
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")

        titlelog = Label(self, text="ÖĞRETMEN GİRİŞ SAYFASI", font=('Bold', 15), bg='#273b7a', fg='white')
        titlelog.pack(fill=X)

        self.fr1 = Frame(self, width=560, height=580,highlightbackground='#273b7a', highlightthickness=3)
        self.fr1.pack(pady=20)


#-------------image ekleme-----------------------------------------

        photo = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\teacher64.png")

        panel = Label(self, image=photo,bg='#273b7a', fg='white' , font=('Bold',15))
        panel.place(x=440, y=100)

        sifre_goster_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\hidden.png")

        user_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\profile-user.png")


 # ------------ icon yada image ekelme şifre gizlemek ve gostermek icin ve user img ve sifre gosterme methosu  --------------------

        show_hide_but = Button(self.fr1, image=sifre_goster_img, bd=0,command=self.showhide_sifre)
        show_hide_but.place(x=468, y=236)

        userimg_label = Label(self.fr1, image=user_img, bd=0)
        userimg_label.place(x=468, y=165)

        lbl1 = Label(self.fr1, text="KULLANICI ADI:",font=('Bold',15),fg='#273b7a')
        lbl1.place(x=5, y=165)

        lbl2 = Label(self.fr1, text="ŞİFRE:",font=('Bold',15),fg='#273b7a')
        lbl2.place(x=80, y=234)

        self.entryusername = Entry(self.fr1,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.entryusername.place(x=160, y=166,width=300)

        self.entrypassword = Entry(self.fr1,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2, show='*')
        self.entrypassword.place(x=160, y=236, width=300)



        # Buttons
        butlogin = Button(self.fr1, text="GİRİŞ YAP",font=('Bold',15),bg='#273b7a',fg='white', command=self.girisfonk)
        butlogin.place(x=220, y=320,width=200, height=40)



        butsifre = Button(self.fr1, text="ŞİFRE UNUTTUM", font=('Bold', 15), fg="#273b7a", bd=0,command=lambda: [self.withdraw(), self.sifreguncellefonk()])
        butsifre.place(x=380, y=530)

        butiptal = Button(self.fr1, text="UYGULAMA KAPAT", font=('Bold',15),bg='#273b7a',fg='white', command=self.destroy)
        butiptal.place(x=220, y=400,width=200, height=40)



        giris_btu=Button(self.fr1,text='GİRİŞ SAYFASINA DÖN', font=('Bold',15),bg='#273b7a',fg='white',command=self.geri_to_GİRİSCLASS)
        giris_btu.place(x=10,y=520, width=300, height=40)




#self.mainloop() satırını silerseniz, ana döngü (main loop) çağrılmamış olur ve Tkinter uygulamanız çalışmaz.
# mainloop() çağrısı, Tkinter uygulamasının penceresini görüntülemek,
#kullanıcı etkileşimini beklemek ve olayları işlemek için gereklidir.

        self.mainloop()

    def geri_to_GİRİSCLASS(self):

        self.master.deiconify()  # LoginClass penceresini yeniden göster
        self.destroy()  # Şifre Güncelleme penceresini kapat

    def girisfonk(self):

        try:
            kullaniciadi = self.entryusername.get()
            sifre = self.entrypassword.get()


            # Eğer herhangi bir alan boşsa hata mesajı göster ve metodu sonlandır  return ile sonlandırılır

            if not kullaniciadi or not sifre:
                messagebox.showerror("Hata", "Kullanıcı adı veya şifre alanları boş olamaz!")
                return

            # Doluysa Devam Et: Eğer tüm alanlar doluysa, veritabanı bağlantısını aç, SQL sorgusunu çalıştır ve işlem yapılır.

            con = pymysql.connect(host="localhost", user="root", password="", database="ogrenci")
            cursor = con.cursor()

            sql = "SELECT * FROM email WHERE kullaniciadi=%s AND sifre=%s"
            cursor.execute(sql, (kullaniciadi, sifre))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Başarılı", "Giriş başarılı!")
                # Burada ana formu açabilirsin


                self.withdraw()

                self.studentfonk()



            else:
                messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")

        finally:
           if 'con' in locals():
               con.close()


    def showhide_sifre(self):
          if self.entrypassword['show'] == '*':

            self.entrypassword.config(show='')
          else:
            self.entrypassword.config(show='*')


    def sifreguncellefonk(self):
        SifreGuncelleme(self)

    def studentfonk(self):
        student(self)









# app.mainloop() komutu, Tkinter uygulamasının ana olay döngüsünü başlatır.
# Tkinter'de, bir GUI (Grafiksel Kullanıcı Arayüzü) uygulaması başlatıldığında, kullanıcının etkileşimde bulunabileceği pencere ve widget'lar oluşturulur.
# Ancak, uygulamanın etkileşim beklemesi ve kullanıcı girdilerini işlemesi için bir döngüye ihtiyacı vardır. İşte mainloop() bu noktada devreye girer.







