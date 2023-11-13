# Mengimpor modul-modul yang diperlukan
import PySimpleGUI as sg
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Membuat fungsi untuk menghasilkan kunci publik dan kunci privat


def generate_key():
    # Membangkitkan kunci RSA dengan panjang 1024 bit
    key = RSA.generate(1024)
    # Mengembalikan kunci publik dan kunci privat dalam format PEM
    return key.publickey().export_key(), key.export_key()

# Membuat fungsi untuk menyimpan kunci ke file


def save_key(filename, key):
    # Membuka file dalam mode biner
    with open(filename, "wb") as f:
        # Menulis kunci ke file
        f.write(key)

# Membuat fungsi untuk memuat kunci dari file


def load_key(filename):
    # Membuka file dalam mode biner
    with open(filename, "rb") as f:
        # Membaca kunci dari file
        key = f.read()
    # Mengembalikan kunci dalam format PEM
    return key

# Membuat fungsi untuk enkripsi


def encrypt_photo(filename, public_key):
    # Membuka file txt  dalam mode biner
    with open(filename, "rb") as f:
        # Membaca data biner dari file txt
        data = f.read()
    # Membuat objek PKCS1_OAEP dengan kunci publik yang diberikan
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    # Mengenkripsi data dengan objek PKCS1_OAEP
    ciphertext = cipher.encrypt(data)
    # Mengembalikan ciphertext
    return ciphertext

# Membuat fungsi untuk dekripsi txt


def decrypt_photo(ciphertext, private_key):
    # Membuat objek PKCS1_OAEP dengan kunci privat yang diberikan
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    # Mendekripsi ciphertext dengan objek PKCS1_OAEP
    data = cipher.decrypt(ciphertext)
    # Mengembalikan data biner yang telah didekripsi
    return data


# Membuat layout GUI dengan PySimpleGUI
layout = [
    [sg.Text("Program Enkripsi dan Dekripsi file text")],
    [sg.Text("Pilih file txt yang ingin dienkripsi:")],
    [sg.Input(key="input_file"), sg.FileBrowse()],
    [sg.Text("Pilih file kunci publik untuk enkripsi:")],
    [sg.Input(key="public_key_file"), sg.FileBrowse()],
    [sg.Text("Pilih file kunci privat untuk dekripsi:")],
    [sg.Input(key="private_key_file"), sg.FileBrowse()],
    [sg.Button("Bangkitkan Kunci"), sg.Button("Enkripsi"),
     sg.Button("Dekripsi"), sg.Button("Keluar")],
    [sg.Output(key="output", size=(60, 10))]
]

# Membuat window GUI dengan layout yang telah dibuat
window = sg.Window("Program Enkripsi dan Dekripsi txt", layout)

# Membuat loop untuk menangani event dan value dari window GUI
while True:
    # Membaca event dan value dari window GUI
    event, values = window.read()

    # Jika event adalah "Bangkitkan Kunci"
    if event == "Bangkitkan Kunci":
        try:
            # Memanggil fungsi generate_key untuk mendapatkan kunci publik dan kunci privat
            public_key, private_key = generate_key()
            # Menyimpan kunci publik ke file public.pem
            save_key("public.pem", public_key)
            # Menyimpan kunci privat ke file private.pem
            save_key("private.pem", private_key)
            # Menampilkan pesan sukses ke output GUI
            print(f"Kunci publik dan kunci privat berhasil dibangkitkan dan disimpan ke file public.pem dan private.pem")
        except Exception as e:
            # Menampilkan pesan error ke output GUI jika terjadi exception
            print(f"Terjadi kesalahan: {e}")

    # Jika event adalah "Enkripsi"
    elif event == "Enkripsi":
        # Mendapatkan nilai input file dan public key file dari window GUI
        input_file = values["input_file"]
        public_key_file = values["public_key_file"]

        # Jika input file dan public key file tidak kosong
        if input_file and public_key_file:
            try:
                # Memuat kunci publik dari file yang dipilih
                public_key = load_key(public_key_file)
                # Memanggil fungsi encrypt_photo dengan input file dan kunci publik yang diberikan
                ciphertext = encrypt_photo(input_file, public_key)
                # Membuat nama output file dengan menambahkan ekstensi .enc ke input file
                output_file = input_file + ".enc"
                # Membuka output file dalam mode biner
                with open(output_file, "wb") as f:
                    # Menulis ciphertext ke output file
                    f.write(ciphertext)
                # Menampilkan pesan sukses ke output GUI
                print(
                    f"File {input_file} berhasil dienkripsi menjadi {output_file}")
            except Exception as e:
                # Menampilkan pesan error ke output GUI jika terjadi exception
                print(f"Terjadi kesalahan: {e}")
        else:
            # Menampilkan pesan peringatan ke output GUI jika input file atau public key file kosong
            print("Harap pilih file txt dan file kunci publik")

    # Jika event adalah "Dekripsi"
    elif event == "Dekripsi":
        # Mendapatkan nilai input file dan private key file dari window GUI
        input_file = values["input_file"]
        private_key_file = values["private_key_file"]

        # Jika input file dan private key file tidak kosong
        if input_file and private_key_file:
            try:
                # Memuat kunci privat dari file yang dipilih
                private_key = load_key(private_key_file)
                # Membuka input file dalam mode biner
                with open(input_file, "rb") as f:
                    # Membaca ciphertext dari input file
                    ciphertext = f.read()
                # Memanggil fungsi decrypt_photo dengan ciphertext dan kunci privat yang diberikan
                data = decrypt_photo(ciphertext, private_key)
                # Membuat nama output file dengan menghapus ekstensi .enc dari input file
                output_file = input_file.replace(".enc", "")
                # Membuka output file dalam mode biner
                with open(output_file, "wb") as f:
                    # Menulis data biner yang telah didekripsi ke output file
                    f.write(data)
                # Menampilkan pesan sukses ke output GUI
                print(
                    f"File {input_file} berhasil didekripsi menjadi {output_file}")
            except Exception as e:
                # Menampilkan pesan error ke output GUI jika terjadi exception
                print(f"Terjadi kesalahan: {e}")
        else:
            # Menampilkan pesan peringatan ke output GUI jika input file atau private key file kosong
            print("Harap pilih file txt dan file kunci privat")

    # Jika event adalah "Keluar" atau window ditutup
    elif event == "Keluar" or event == sg.WIN_CLOSED:
        # Keluar dari loop
        break

# Menutup window GUI
window.close()
