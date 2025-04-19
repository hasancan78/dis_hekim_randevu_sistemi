
import pandas as pd
import os

veri_dosyasi = "veriler.csv"

if not os.path.exists(veri_dosyasi):
    df = pd.DataFrame(columns=[
        "isim", "soyisim", "dogum_tarihi", "telefon",
        "randevu_tarihi", "randevu_saati", "aciklama"
    ])
    df.to_csv(veri_dosyasi, index=False)

def veri_ekle(isim, soyisim, dogum_tarihi, telefon, randevu_tarihi, randevu_saati, aciklama):
    yeni_veri = {
        "isim": isim,
        "soyisim": soyisim,
        "dogum_tarihi": dogum_tarihi,
        "telefon": telefon,
        "randevu_tarihi": randevu_tarihi,
        "randevu_saati": randevu_saati,
        "aciklama": aciklama
    }
    df = pd.read_csv(veri_dosyasi)
    df = pd.concat([df, pd.DataFrame([yeni_veri])], ignore_index=True)
    df.to_csv(veri_dosyasi, index=False)

def tum_verileri_getir():
    return pd.read_csv(veri_dosyasi)

def tarihe_gore_filtrele(tarih):
    df = pd.read_csv(veri_dosyasi)
    return df[df["randevu_tarihi"] == tarih]

def isme_gore_filtrele(isim):
    df = pd.read_csv(veri_dosyasi)
    return df[df["isim"].str.contains(isim, case=False)]

def randevu_sil(index_no):
    df = pd.read_csv(veri_dosyasi)
    df = df.drop(index=index_no)
    df.to_csv(veri_dosyasi, index=False)
