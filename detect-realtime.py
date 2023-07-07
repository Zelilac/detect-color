import cv2
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk

def detect_red_objects():
    cap = cv2.VideoCapture(0)  # Inisialisasi video stream
    root = Tk()  # Inisialisasi objek Tkinter
    root.title("Deteksi Objek Warna Merah")
    
    # Buat label untuk menampilkan gambar
    label = Label(root)
    label.pack()

    def video_stream():
        _, frame = cap.read()  # Membaca frame dari video stream
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Konversi frame ke ruang warna HSV

        # Filter warna merah dalam range HSV
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([160, 100, 100])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        # Gabungkan dua mask menjadi satu
        mask = cv2.bitwise_or(mask1, mask2)

        # Hapus noise menggunakan operasi morfologi
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Temukan kontur objek
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Gambar persegi panjang di sekitar objek yang terdeteksi
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Hanya menggambar kotak jika luas kontur melebihi batas
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Konversi frame OpenCV ke format yang dapat ditampilkan di Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        label.img_tk = img_tk  # Simpan referensi agar tidak terhapus oleh garbage collector
        label.config(image=img_tk)  # Tampilkan gambar di Tkinter label
        label.after(10, video_stream)  # Panggil kembali fungsi video_stream setiap 10 milidetik

    video_stream()
    root.mainloop()

detect_red_objects()
