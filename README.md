# Overload Server Simulator 🔥

## Deskripsi
**Overload Server Simulator** adalah alat pengujian beban jaringan yang dikembangkan oleh **Protocol404 Team**. Program ini dirancang untuk mensimulasikan berbagai jenis traffic jaringan guna menguji ketahanan server terhadap serangan beban tinggi dengan multi-protokol.

## 🚀 Fitur Utama

### **Multi-Protokol Support**
- **TCP Flood** - Pengujian koneksi TCP dengan three-way handshake
- **UDP Flood** - Pengujian paket UDP connectionless
- **ICMP Flood** - Pengujian ping flood dengan raw socket

### **Advanced Features**
- **Multi-threading** - Menjalankan ribuan request secara paralel
- **Real-time Monitoring** - Progress bar dengan statistik live
- **Konfigurasi Fleksibel** - Customizable packet size, threads, timeout
- **Detailed Analytics** - Latency, success rate, throughput analysis
- **User-friendly Interface** - Menu berbasis terminal dengan warna

## 📊 Metrik yang Diukur

- **Latency** (min, avg, max response time)
- **Success Rate** (persentase request berhasil)
- **Throughput** (requests per second)
- **Data Transfer** (bytes sent/received)
- **Error Tracking** (detailed error reporting)

## 🛠️ Teknologi yang Digunakan

```python
# Core Technologies
- Socket Programming (TCP/UDP/ICMP)
- Multi-threading dengan Threading.Lock
- Raw Socket untuk ICMP
- Custom Checksum Calculation
- Cross-platform Compatibility
```

## ⚙️ Konfigurasi Default

| Parameter | Default Value | Maximum |
|-----------|---------------|---------|
| Threads | 10 | 999,999 |
| Packet Size | 1 KB | 10 MB |
| Requests | 100 | Unlimited |
| Timeout | 3 seconds | Custom |

## 🎯 Penggunaan

```bash
# Menjalankan program
python ddos.py

# Menu yang tersedia:
1. Mulai Pengujian TCP
2. Mulai Pengujian UDP  
3. Mulai Pengujian ICMP (Ping Flood)
4. Konfigurasi Pengujian
5. Keluar
```

## 📈 Contoh Output
```
🚀 MEMULAI PENGUJIAN TCP
============================================================
Target    : 192.168.1.1:80
Protokol  : TCP
Ukuran Paket: 1024 bytes (1.00 KB)
Jumlah Request: 1000
Thread    : 50
Timeout   : 3s
============================================================

📈 Progress: 100.0% | ✅: 987 | ❌: 13 | ⏱ RPS: 156.7 | 💯 Success: 98.7%
```

## ⚠️ Peringatan Keamanan

**Hanya untuk tujuan edukasi dan pengujian sah!**
- Gunakan hanya pada sistem yang Anda miliki
- Dapatkan izin sebelum melakukan pengujian
- ICMP memerlukan hak akses root pada Linux
- Patuhi hukum setempat mengenai pengujian keamanan

## 👥 Tim Pengembang
**Protocol404 Team**
- Zaidaan Ali Wirayudha
- Leon Pratama Agustian Rachmad

## 📝 Lisensi
Program ini ditujukan untuk tujuan edukasi dalam bidang keamanan jaringan dan pengujian penetrasi.

---

**🔐 Remember: With Great Power Comes Great Responsibility!**
