import tkinter as tk
import socket
import geocoder
import pytz
import uuid

def export_ip_info():
    ip_info_text = ip_info_label.cget("text")
    if ip_info_text:
        with open("ip_info.txt", "w") as file:
            file.write(ip_info_text)
            print("Ma'lumotlar faylga yozildi: ip_info.txt")
    else:
        print("Export qilinadigan ma'lumotlar yo'q")

def get_ip_info():
    ip_address = ip_entry.get()
    ports = port_entry.get().split(',')  # Kiritilgan portlarni bo'shliqlar orqali ajratib olish

    try:
        # IP manzilining qaysi davlatga tegishli ekanligini aniqlash
        g = geocoder.ip(ip_address)
        country = g.country

        # Vaqt zonasini aniqlash
        timezone = pytz.country_timezones(country)[0]

        # MAC manzilini olish
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)])

        # Portlarni tekshirish va natijalarni to'plash
        port_results = []
        for port_number in ports:
            port_number = int(port_number.strip())  # Port raqamini olish
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # 1 sekundga to'xtatish
                result = s.connect_ex((ip_address, port_number))
                if result == 0:
                    port_status = "ochiq"
                else:
                    port_status = "yopiq"
                port_results.append(f"Port {port_number}: {port_status}")

        ip_info_text = f"IP manzil: {ip_address}\nDavlat: {country}\nVaqt zona: {timezone}\nMAC manzil: {mac_address}\n" + "\n".join(port_results)
        ip_info_label.config(text=ip_info_text)
    except:
        ip_info_label.config(text="Noma'lum IP manzil")

# GUI yaratish
root = tk.Tk()
root.title("IP Ma'lumotlarini Olish")

# IP manzilini kiritish uchun kiritish maydoni
ip_label = tk.Label(root, text="IP Manzil:")
ip_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

# Portlarni kiritish uchun kiritish maydoni
port_label = tk.Label(root, text="Portlar (vergul bilan ajratilgan):")
port_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=10, pady=10)

# Ma'lumotlarni chiqarish uchun tugma
info_button = tk.Button(root, text="Ma'lumotlarni Olish", command=get_ip_info)
info_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Export tugmasi
export_button = tk.Button(root, text="Export", command=export_ip_info)
export_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Chiqariladigan ma'lumotlar uchun etiket
ip_info_label = tk.Label(root, text="")
ip_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
