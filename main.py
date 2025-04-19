
import tkinter as tk
from tkinter import ttk, messagebox
import veritabani

pencere = tk.Tk()
pencere.title("Dis Hekimi Otomasyon Sistemi")
pencere.geometry("400x300")

def ana_menu():
    for widget in pencere.winfo_children():
        widget.destroy()

    baslik = tk.Label(pencere, text="Dis Hekimi Otomasyon Sistemi", font=("Arial", 16))
    baslik.pack(pady=20)

    btn_kayit = tk.Button(pencere, text="Yeni Hasta Kaydi", width=25, command=kayit_penceresi)
    btn_kayit.pack(pady=5)

    btn_listele = tk.Button(pencere, text="Randevulari Goruntule", width=25, command=listeleme_penceresi)
    btn_listele.pack(pady=5)

    btn_cikis = tk.Button(pencere, text="Uygulamadan Cik", width=25, command=pencere.quit)
    btn_cikis.pack(pady=5)

def kayit_penceresi():
    pencere_kayit = tk.Toplevel(pencere)
    pencere_kayit.title("Yeni Kayit")
    pencere_kayit.geometry("400x400")

    tk.Label(pencere_kayit, text="Isim").pack()
    giris_isim = tk.Entry(pencere_kayit)
    giris_isim.pack()

    tk.Label(pencere_kayit, text="Soyisim").pack()
    giris_soyisim = tk.Entry(pencere_kayit)
    giris_soyisim.pack()

    tk.Label(pencere_kayit, text="Dogum Tarihi (GG/AA/YYYY)").pack()
    giris_dogum = tk.Entry(pencere_kayit)
    giris_dogum.pack()

    tk.Label(pencere_kayit, text="Telefon").pack()
    giris_telefon = tk.Entry(pencere_kayit)
    giris_telefon.pack()

    tk.Label(pencere_kayit, text="Randevu Tarihi (GG/AA/YYYY)").pack()
    giris_randevu_tarihi = tk.Entry(pencere_kayit)
    giris_randevu_tarihi.pack()

    tk.Label(pencere_kayit, text="Randevu Saati (SS:dd)").pack()
    giris_randevu_saati = tk.Entry(pencere_kayit)
    giris_randevu_saati.pack()

    tk.Label(pencere_kayit, text="Aciklama").pack()
    giris_aciklama = tk.Text(pencere_kayit, height=3)
    giris_aciklama.pack()

    def kaydet():
        try:
            veritabani.veri_ekle(
                giris_isim.get(),
                giris_soyisim.get(),
                giris_dogum.get(),
                giris_telefon.get(),
                giris_randevu_tarihi.get(),
                giris_randevu_saati.get(),
                giris_aciklama.get("1.0", "end").strip()
            )
            messagebox.showinfo("Basarili", "Kayit basariyla eklendi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kayit eklenemedi.\n{e}")

    tk.Button(pencere_kayit, text="Kaydet", command=kaydet).pack(pady=5)
    tk.Button(pencere_kayit, text="Temizle", command=lambda: [giris_isim.delete(0, 'end'),
                                                               giris_soyisim.delete(0, 'end'),
                                                               giris_dogum.delete(0, 'end'),
                                                               giris_telefon.delete(0, 'end'),
                                                               giris_randevu_tarihi.delete(0, 'end'),
                                                               giris_randevu_saati.delete(0, 'end'),
                                                               giris_aciklama.delete("1.0", "end")]).pack()
    tk.Button(pencere_kayit, text="Geri Don", command=pencere_kayit.destroy).pack(pady=5)

def listeleme_penceresi():
    pencere_liste = tk.Toplevel(pencere)
    pencere_liste.title("Randevular")
    pencere_liste.geometry("800x400")

    tk.Label(pencere_liste, text="Tarih ile Filtrele (GG/AA/YYYY)").pack()
    tarih_entry = tk.Entry(pencere_liste)
    tarih_entry.pack()

    tk.Label(pencere_liste, text="Isim ile Filtrele").pack()
    isim_entry = tk.Entry(pencere_liste)
    isim_entry.pack()

    tablo = ttk.Treeview(pencere_liste, columns=("isim", "soyisim", "telefon", "tarih", "saat", "aciklama"), show='headings')
    for col in tablo["columns"]:
        tablo.heading(col, text=col)
    tablo.pack(fill=tk.BOTH, expand=True)

    def verileri_goster(df):
        for satir in tablo.get_children():
            tablo.delete(satir)
        for i, row in df.iterrows():
            tablo.insert("", "end", iid=i, values=(row["isim"], row["soyisim"], row["telefon"],
                                                   row["randevu_tarihi"], row["randevu_saati"], row["aciklama"]))

    def tumunu_goster():
        df = veritabani.tum_verileri_getir()
        verileri_goster(df)

    def filtrele_tarih():
        df = veritabani.tarihe_gore_filtrele(tarih_entry.get())
        verileri_goster(df)

    def filtrele_isim():
        df = veritabani.isme_gore_filtrele(isim_entry.get())
        verileri_goster(df)

    def secileni_sil():
        secili = tablo.selection()
        if secili:
            index = int(secili[0])
            veritabani.randevu_sil(index)
            tumunu_goster()

    tk.Button(pencere_liste, text="Tumu", command=tumunu_goster).pack(pady=5)
    tk.Button(pencere_liste, text="Tarihe Gore Filtrele", command=filtrele_tarih).pack()
    tk.Button(pencere_liste, text="Isme Gore Filtrele", command=filtrele_isim).pack()
    tk.Button(pencere_liste, text="Secilen Randevuyu Sil", command=secileni_sil).pack()
    tk.Button(pencere_liste, text="Geri Don", command=pencere_liste.destroy).pack(pady=5)

    tumunu_goster()

ana_menu()
pencere.mainloop()
