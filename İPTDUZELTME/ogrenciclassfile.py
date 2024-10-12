
from tkinter import *
import tkinter as tk
from tkinter import Toplevel, filedialog
from tkinter import messagebox, ttk
import pymysql
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from self import self




class ogrencigirisclass(Toplevel):

    def __init__(self, master=None):
        super().__init__(master)


        self.title("ÖĞRENCİ YÖNETİM SİSTEMİ")
        self.geometry("800x600")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")

        # image eklemek icin

        self.photostudent = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\student64.png")
        self.sifre_goster_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\hidden.png")
        self.user_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\profile-user.png")



        # Başlık
        titlelog = Label(self, text="ÖĞRENCİ GİRİŞ SAYFASI", font=('Bold', 15), bg='#273b7a', fg='white')
        titlelog.pack(fill=X)

        # -----------Frame oluşturma -------------------

        self.frame_ogrenci = Frame(self, highlightbackground='#273b7a', highlightthickness=3)
        self.frame_ogrenci.pack(pady=30)
        self.frame_ogrenci.pack_propagate(False)
        self.frame_ogrenci.configure(width=500, height=490)




#-----------İCON olusturma ----------------------------

        ogrenciicon=Label(self.frame_ogrenci, image=self.photostudent,bg='#273b7a', fg='white' , font=('Bold',15))
        ogrenciicon.place(x=240,y=30)

        # ------------methods---------------------------------------

        def showhide_sifre():
            if self.ogrenci_sifre_entry['show'] == '*':

                self.ogrenci_sifre_entry.config(show='')
            else:
                self.ogrenci_sifre_entry.config(show='*')





#  ---------------Label VE entry  olusturma -----------------

        self.ogrenci_no_lb= Label(self.frame_ogrenci,text='ÖĞRENCİ NO :',font=('Bold',15),fg='#273b7a')
        self.ogrenci_no_lb.place(x=20,y=150)

        self.ogrenci_no_entry = Entry(self.frame_ogrenci,font=('Bold',15),justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.ogrenci_no_entry.place(x=180,y=150)



        ogrenci_sifre_lb= Label(self.frame_ogrenci,text='ŞİFRE :',font=('Bold',15),fg='#273b7a')
        ogrenci_sifre_lb.place(x=82,y=250)

        self.ogrenci_sifre_entry = Entry(self.frame_ogrenci, font=('Bold', 15), justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2,show='*')
        self.ogrenci_sifre_entry.place(x=180, y=250)



#---------------Buttons olusturma----------------------------------


        giris_btu=Button(self.frame_ogrenci,text='GİRİŞ YAP', font=('Bold',15),bg='#273b7a',fg='white',command=self.ogrenci_girisfonk)
        giris_btu.place(x=200,y=350, width=170, height=40)


        giris_btu=Button(self.frame_ogrenci,text='GİRİŞ SAYFASINA DÖN', font=('Bold',15),bg='#273b7a',fg='white',command=self.geri_to_GİRİSCLASS)
        giris_btu.place(x=10,y=438, width=300, height=40)








#---------------şifre unutum olusturma-----------------


        sifre_unutum_but= Button(self.frame_ogrenci,text='ŞİFRE UNUTUM', fg='#273b7a',bd=0,command=lambda: [self.withdraw(), self.ogrenci_sifre_fonk()])
        sifre_unutum_but.place(x=380,y=450)



#------------ icon yada image ekelme şifre gizlemek ve gostermek icin ve user img --------------------

        show_hide_but=Button(self.frame_ogrenci,image=self.sifre_goster_img,bd=0,command= showhide_sifre)
        show_hide_but.place(x=420,y=250)

        userimg_label=Label(self.frame_ogrenci,image=self.user_img,bd=0)
        userimg_label.place(x=420,y=150)

        self.mainloop()

    def geri_to_GİRİSCLASS(self):
        self.master.deiconify()  # LoginClass penceresini yeniden göster
        self.destroy()  # Şifre Güncelleme penceresini kapat

    def ogrenci_girisfonk(self):
            try:
                ogrencino = self.ogrenci_no_entry.get()
                sifre = self.ogrenci_sifre_entry.get()

                if not ogrencino or not sifre:
                    messagebox.showerror("Hata", "Öğrenci no veya şifre alanları boş olamaz!")
                    return

                con = pymysql.connect(host="localhost", user="root", password="", database="ogrenci")
                cursor = con.cursor()

                sql = "SELECT * FROM ogrencidata WHERE ogrencino=%s AND sifre=%s"
                cursor.execute(sql, (ogrencino, sifre))
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Başarılı", "Giriş başarılı!")

                    self.withdraw()

                    print(f"Oluşturulan öğrenci_islemleri nesnesi class dan : {ogrencino}")
                    self.ogrenci_islemleri = ogrenciislemlericlass(ogrencino,master=self)  #  ogrenciislemlericlass  nesnesini oluştururken parametreleri geçiyoruz





                else:
                    messagebox.showerror("Hata", "Öğrenci no veya şifre yanlış!")
            except Exception as e:
                messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
            finally:
                if 'con' in locals():
                    con.close()

    def ogrenci_sifre_fonk(self):

        ogrenci_sifre(self)






class ogrenci_sifre(Toplevel):

    def __init__(self, master=None):
        super().__init__(master)  # # Üst sınıfın (Toplevel) __init__ metodunu çağır ve master parametresini geçir
        self.title("OGRENCİ YONETİM SİSTEMİ")
        self.geometry("900x550")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")

        sifre_goster_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\hidden.png")
        user_img = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\profile-user.png")

        # image eklemek icin

        photo = PhotoImage(file=r"C:\Users\alada\Desktop\ogrenciipt\private-account.png")
        panel = Label(self, image=photo)
        panel.photo = photo  # Keep a reference to avoid garbage collection
        panel.place(x=630, y=120)


        titlelog = Label(self, text="ŞİFRE GÜNCELLEME SİSTEMİ",  font=('Bold', 15), bg='#273b7a', fg='white')
        titlelog.pack(fill=X)

        lbl1 = Label(self, text="ÖĞRENCİ NO :  ", font=('Bold',15),fg='#273b7a')
        lbl1.place(x=12, y=138)

        lbl2 = Label(self, text=" YENİ ŞİFRE :",font=('Bold',15),fg='#273b7a')
        lbl2.place(x=30, y=238)




        lbl1 = Label(self,image=user_img, font=('Bold',15),fg='#273b7a')
        lbl1.place(x=520, y=137)

        lbl2 = Label(self,image=sifre_goster_img,font=('Bold',15),fg='#273b7a')
        lbl2.place(x=520, y=235)




        self.ogrenci_no_entry = Entry(self, font=('Bold', 15), justify=CENTER, highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
        self.ogrenci_no_entry.place(x=170, y=140,width=340)


        self.ogrenci_sifre_entry = Entry(self, font=('Bold', 15), justify=CENTER,highlightcolor='#273b7a',highlightbackground='gray',highlightthickness=2)
        self.ogrenci_sifre_entry.place(x=170, y=240,width=340)




        butguncelle = Button(self, text=" ŞİFREYİ  GÜNCELLE  ",font=('Bold',15),bg='#273b7a',fg='white', command=self.sifre_guncelle_onayla)
        butguncelle.place(x=230, y=320)

        butdon = Button(self, text="GİRİŞ SAYFASİNA DÖN",font=('Bold',15),bg='#273b7a',fg='white', command=self.geri_to_login)
        butdon.place(x=640, y=505)




        # # mainloop() çağrısı, Tkinter uygulamasının penceresini görüntülemek,
        # #kullanıcı etkileşimini beklemek ve olayları işlemek için gereklidir.

        self.mainloop()






    def sifre_guncelle_onayla(self):
        try:
            ogrencino = self.ogrenci_no_entry.get()
            sifre = self.ogrenci_sifre_entry.get()

            if not ogrencino or not sifre:
                messagebox.showerror("Hata", "Oğrenci no ve yeni şifre alanları boş bırakılamaz!")
                return

            con = pymysql.connect(host="localhost", user="root", password="", database="ogrenci")
            cursor = con.cursor()
            sql = "UPDATE ogrencinotablo SET sifre=%s WHERE ogrencino=%s"

            cursor.execute(sql, (sifre,ogrencino))
            con.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Başarılı", "Şifre başarıyla güncellendi!")
            else:
                messagebox.showerror("Hata", "öğrenci no  bulunamadı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")


        finally:
           if 'con' in locals():
              con.close()






    def geri_to_login(self):
        self.master.deiconify()  # LoginClass penceresini yeniden göster
        self.destroy()  # Şifre Güncelleme penceresini kapat










class ogrenciislemlericlass(Toplevel):

# paramatre değer aktarılırkrn uyani ogrencino constructor ile diarekte class değildir

    def __init__(self, ogrencino, master=None):
        super().__init__(master)
        self.ogrencino = ogrencino  # Öğrenci numarasını özellik olarak tanımla



        self.geometry('1350x690+1+1')
        self.title('OGRENCİ YONETİM SİSTEMİ')
        self.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")
        self.configure(background="silver")
        self.resizable(False, False)

        self.ogrencino_var = StringVar()
        self.name_var = StringVar()
        self.cinsiyet_var = StringVar()
        self.mail_var = StringVar()
        self.telefon_var = StringVar()
        self.yas_var = StringVar()
        self.class_var = StringVar()
        self.image_path_var = StringVar()

        title = Label(self, text='/--ÖĞRENCİ İŞLEMLERİ SİSTEMİ--/', bg='#273b7a', font=('Bold', 15), fg='white')
        title.pack(fill=X)

        # Yönetici tarafından giriş alanı
        manage_frame = Frame(self, bg='white', highlightbackground='#273b7a', highlightthickness=2)
        manage_frame.place(x=1137, y=30, width=210, height=440)
        title = Label(manage_frame, text='OGRENCİ BİLGİLERİ : ', bg='#273b7a', fg='white')
        title.pack()

        lbl_ogrno = Label(manage_frame, text='ÖĞRENCİ NO:', bg='white')
        lbl_ogrno.pack()
        ogrno_entry = Entry(manage_frame, textvariable=self.ogrencino_var, bd='2')
        ogrno_entry.pack()

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

        btn_select_image = Button(manage_frame, text="Görüntü Seç", command=self.select_image)
        btn_select_image.pack()

        self.image_label = Label(manage_frame, text="", bg="white")
        self.image_label.pack()

        # Butonlar için çerçeve
        button_frame = Frame(self, bg='white', highlightbackground='#273b7a', highlightthickness=2)
        button_frame.place(x=1137, y=434, width=210, height=2560)
        title2 = Label(button_frame, text='--KONTROL PANELİ--', fg='white', bg='#273b7a')
        title2.pack()
        title2.pack(fill=X)

        clear_btn = Button(button_frame, text='GİRİŞ ALANDAKİ VERİLERİ SİL', bg='#273b7a', fg='white',
                           command=self.clear)
        clear_btn.place(x=33, y=150, width=170, height=30)

        exit_btn = Button(button_frame, text=' ÇIKIŞ YAP ', bg='#273b7a', fg='white', command=self.exit_fonk)
        exit_btn.place(x=33, y=190, width=170, height=30)

        print_card_btn = Button(button_frame, text='ÖĞRENCİ KARTI YAZDIR', bg='#273b7a', fg='white',
                                command=self.print_student_card)
        print_card_btn.place(x=33, y=115, width=170, height=30)

        save_btn = Button(button_frame, text=' KAYET ET ', bg='#273b7a', fg='white', command=self.conveekle)
        save_btn.place(x=33, y=28, width=170, height=30)

        giris_btn = Button(button_frame, text='GİRİS SAYFASINA DÖN', bg='#273b7a', fg='white', command=self. geri_fonk)
        giris_btn.place(x=33, y=70, width=170, height=30)

        # Arama çerçevesi
        search_frame = Frame(self, bg='white', highlightbackground='#273b7a', highlightthickness=3)
        search_frame.place(x=1, y=30, width=1134, height=50)

        # Detay çerçevesi
        Dietals_frame = Frame(self, bg='#273b7a')
        Dietals_frame.place(x=1, y=84, width=1134, height=600)

        # Tablo ve kaydırıcılar
        scroll_x = Scrollbar(Dietals_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Dietals_frame, orient=VERTICAL)
        self.student_table = ttk.Treeview(Dietals_frame, columns=(
            'ogrencino', 'sifre', 'name', 'cinsiyet', 'mail', 'telefon', 'yas', 'class'),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        self.student_table.place(x=18, y=4, width=1130, height=582)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

# bu tabloda veriler görünüyor ve bu ilk satır yani sütun isimleri yani başlik = geading  olarak
        self.student_table['show'] = 'headings'
        self.student_table.heading('ogrencino', text='ÖĞRENCİ NO')
        self.student_table.heading('sifre', text='ÖĞRENCİ ŞİFRESİ')
        self.student_table.heading('name', text='ADI VE SOYADI')
        self.student_table.heading('cinsiyet', text='CİNSİYET')
        self.student_table.heading('mail', text='E-POSTA')
        self.student_table.heading('telefon', text='TELEFON')
        self.student_table.heading('yas', text='YAŞ')
        self.student_table.heading('class', text='SINIF')

# Tablo sütunları
        self.student_table.column('ogrencino', width=50)
        self.student_table.column('sifre', width=50)
        self.student_table.column('name', width=100)
        self.student_table.column('cinsiyet', width=50)
        self.student_table.column('mail', width=100)
        self.student_table.column('telefon', width=70)
        self.student_table.column('yas', width=70)
        self.student_table.column('class', width=100)

        self.student_table.bind("<ButtonRelease-1>", self.get_goster)

        # Öğrenci verilerini getirme
        self.getveriler_all()




    def geri_fonk(self):

         self.master.deiconify()  # LoginClass penceresini yeniden göster
         self.destroy()  # Şifre Güncelleme penceresini kapat





# Görüntü seçme işlevi

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.image_path_var.set(file_path)
            self.image_label.config(text=file_path)

    # Öğrenci bilgilerini veritabanına ekleme işlevi
    def conveekle(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')
            cur = con.cursor()
            with open(self.image_path_var.get(), 'rb') as image_file:
                binary_image = image_file.read()
            cur.execute(
                "INSERT INTO ogrencikisiseldata (ogrencino, name, cinsiyet, mail, telefon, yas, class, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    self.ogrencino_var.get(),
                    self.name_var.get(),
                    self.cinsiyet_var.get(),
                    self.mail_var.get(),
                    self.telefon_var.get(),
                    self.yas_var.get(),
                    self.class_var.get(),
                    binary_image
                ))
            con.commit()
            self.getveriler_all()
            self.clear()
        except Exception as error:
            messagebox.showerror("Hata:", f"conveekle methodunda  bir hata oluştu: {error}")
        finally:
            if 'con' in locals():
                con.close()

    # belirli öğrenci no göre verilerini getirme işlevi
    def getveriler_all(self):

        try:
            print(f"Öğrenci numarası getveriler_all dan : {self.ogrencino}")

            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')
            cur = con.cursor()
            query = 'SELECT ogrencino, sifre, name, cinsiyet, mail, telefon, yas, class FROM ogrencidata WHERE ogrencino = %s'
            cur.execute(query, (self.ogrencino))
            rows = cur.fetchall()
            if len(rows) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert("", 'end', values=row)
                con.commit()
            else:
                messagebox.showinfo("Bilgi", "Bu öğrenci numarasına ait kayıt bulunamadı.")
        except Exception as error:
            messagebox.showerror("Hata", f"getveriler_all methodunda bir hata oluştu: {error}")
        finally:
            if 'con' in locals():
                con.close()


    # Giriş alanlarını temizleme işlevi
    def clear(self):
        self.ogrencino_var.set('')
        self.name_var.set('')
        self.cinsiyet_var.set('')
        self.mail_var.set('')
        self.telefon_var.set('')
        self.yas_var.set('')
        self.class_var.set('')
        self.image_path_var.set('')
        self.image_label.config(text='')

    # Öğrenci seçildiğinde öğrenci bilgilerini getirme işlevi
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
                    self.name_var.set(row[2])
                    self.cinsiyet_var.set(row[3])
                    self.mail_var.set(row[4])
                    self.telefon_var.set(row[5])
                    self.yas_var.set(row[6])
                    self.class_var.set(row[7])


         except Exception as error:
            messagebox.showerror("Hata:", f"get_goster  bir hata oluştu: {error}")


    # Öğrenci kartını yazdırma işlevi
    def print_student_card(self):
        try:
            ogrno = self.ogrencino_var.get()
            if not ogrno:
                messagebox.showerror("Hata", "Öğrenci numarası boş olamaz!")
                return
            con = pymysql.connect(host='localhost', user='root', password='', database='ogrenci')
            cur = con.cursor()
            cur.execute("SELECT * FROM ogrencikisiseldata WHERE ogrencino=%s", ogrno)
            student = cur.fetchone()
            if student:

                window = Toplevel(self)
                window.title("ÖĞRENCİ KAARTI")
                window.geometry("500x350")
                window.resizable(False, False)
                window.iconbitmap(r"C:\Users\alada\Desktop\ogrenciipt\okul.ico")

                titlelog = Label(window, text="ÖĞRENCİ KARTI OLUŞTURMA", font=('Bold', 15), bg='#273b7a', fg='white')
                titlelog.pack(fill=X)

                Label(window, text=f"Öğrenci No: {student[0]}").pack()
                Label(window, text=f"Adı Soyadı: {student[1]}").pack()
                Label(window, text=f"Cinsiyet: {student[2]}").pack()
                Label(window, text=f"E-Posta: {student[3]}").pack()
                Label(window, text=f"Telefon: {student[4]}").pack()
                Label(window, text=f"Yaş: {student[5]}").pack()
                Label(window, text=f"Sınıf: {student[6]}").pack()

                image_label = Label(window)
                image_label.pack()


                if student[7]:
                    import io
                    from PIL import Image, ImageTk
                    image = Image.open(io.BytesIO(student[7]))
                    photo = ImageTk.PhotoImage(image)
                    image_label.config(image=photo)
                    image_label.image = photo

            con.commit()
        except Exception as error:
            messagebox.showerror("Hata:", f"print_student_card methodunda bir hata oluştu: {error}")
        finally:
            if 'con' in locals():
                con.close()

    # Çıkış fonksiyonu
    def exit_fonk(self):

        isYesNoCancel = messagebox.askyesnocancel("---Çikiş---", "Uygulamayi kapatmak istiyor musunuz?")
        if isYesNoCancel is not None:
            if isYesNoCancel:
                # Evet seçeneği seçildiyse uygulamayı kapat
                self.destroy()
            else:
                # Hayır seçeneği seçildiyse hiçbir işlem yapma
                pass


