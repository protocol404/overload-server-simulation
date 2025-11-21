import os
import sys
import socket
import time
import threading
import random
import argparse
import math
import json
from datetime import datetime

# =============================================================
# Created By Protocol404 Team
# Members: Zaidaan Ali Wirayudha, Leon Pratama Agustian Rachmad
# =============================================================

# Konfigurasi standar
DEFAULT_THREADS = 10
DEFAULT_PACKET_SIZE = 1024  
DEFAULT_REQUESTS = 100
DEFAULT_TIMEOUT = 3
MAX_THREADS = 999999
MAX_PACKET_SIZE = 10 * 1024 * 1024  

# Protokol jaringan
PROTOCOLS = {
    'tcp': socket.SOCK_STREAM,
    'udp': socket.SOCK_DGRAM,
    'icmp': socket.SOCK_RAW
}

# Warna terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                  OVERLOAD SERVER SIMULATOR                   ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║   Alat Pengujian Beban Jaringan dengan Multi-Protokol        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

def print_menu():
    print("\n" + "="*60)
    print(f"{Colors.BOLD}MENU UTAMA:{Colors.ENDC}")
    print("="*60)
    print(f"1. {Colors.OKBLUE}Mulai Pengujian TCP{Colors.ENDC}")
    print(f"2. {Colors.OKBLUE}Mulai Pengujian UDP{Colors.ENDC}")
    print(f"3. {Colors.OKBLUE}Mulai Pengujian ICMP (Ping Flood){Colors.ENDC}")
    print(f"4. {Colors.WARNING}Konfigurasi Pengujian{Colors.ENDC}")
    print(f"5. {Colors.FAIL}Keluar{Colors.ENDC}")
    print("="*60)
    return input("Pilih opsi (1-5): ")

def generate_packet(size):
    return os.urandom(size)

def tcp_test(target_ip, target_port, packet_size, num_requests, timeout, results):
    try:
        # Buat socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Hubungkan ke target
        sock.connect((target_ip, target_port))
        
        # Buat paket data
        data = generate_packet(packet_size)
        
        start_time = time.time()
        sock.sendall(data)
        
        # Tunggu respons (jika ada)
        try:
            response = sock.recv(1024)
        except socket.timeout:
            response = b''
        
        latency = (time.time() - start_time) * 1000  # ms
        sock.close()
        
        return {
            'status': 'SUCCESS',
            'latency': latency,
            'response_size': len(response),
            'error': None
        }
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'latency': 0,
            'response_size': 0,
            'error': str(e)
        }

def udp_test(target_ip, target_port, packet_size, num_requests, timeout, results):
    try:
        # UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        
        # Buat paket
        data = generate_packet(packet_size)
        
        start_time = time.time()
        sock.sendto(data, (target_ip, target_port))
        
        # Respons
        try:
            response, _ = sock.recvfrom(1024)
        except socket.timeout:
            response = b''
        
        latency = (time.time() - start_time) * 1000  # ms
        sock.close()
        
        return {
            'status': 'SUCCESS',
            'latency': latency,
            'response_size': len(response),
            'error': None
        }
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'latency': 0,
            'response_size': 0,
            'error': str(e)
        }

def icmp_test(target_ip, packet_size, num_requests, timeout, results):
    try:
        # ICMP
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(timeout)
        
        # Buat paket
        header = struct.pack("!BBHHH", 8, 0, 0, random.randint(0, 65535), 1)
        data = generate_packet(packet_size)
        packet = header + data
        
        # Checksum
        checksum = calculate_checksum(packet)
        header = struct.pack("!BBHHH", 8, 0, checksum, header[4], header[5])
        packet = header + data
        
        start_time = time.time()
        sock.sendto(packet, (target_ip, 0))
        
        # Respons
        try:
            response, _ = sock.recvfrom(1024)
        except socket.timeout:
            response = b''
        
        latency = (time.time() - start_time) * 1000  # ms
        sock.close()
        
        return {
            'status': 'SUCCESS' if response else 'TIMEOUT',
            'latency': latency,
            'response_size': len(response),
            'error': None
        }
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'latency': 0,
            'response_size': 0,
            'error': str(e)
        }

def calculate_checksum(data):
    if len(data) % 2:
        data += b'\x00'
    
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        checksum += word
        checksum = (checksum & 0xffff) + (checksum >> 16)
    
    return ~checksum & 0xffff

def run_test(protocol, target_ip, target_port, packet_size, num_requests, num_threads, timeout):
    
    # Inisialisasi hasil
    results = {
        'start_time': time.time(),
        'protocol': protocol,
        'target_ip': target_ip,
        'target_port': target_port,
        'packet_size': packet_size,
        'num_requests': num_requests,
        'num_threads': num_threads,
        'timeout': timeout,
        'requests': []
    }
    
    # Tampilkan header pengujian
    print_banner()
    print(f"\n{Colors.BOLD}🚀 MEMULAI PENGUJIAN {protocol.upper()}{Colors.ENDC}")
    print("="*60)
    print(f"Target    : {target_ip}:{target_port}")
    print(f"Protokol  : {protocol.upper()}")
    print(f"Ukuran Paket: {packet_size} bytes ({packet_size/1024:.2f} KB)")
    print(f"Jumlah Request: {num_requests}")
    print(f"Thread    : {num_threads}")
    print(f"Timeout   : {timeout}s")
    print("="*60)
    
    # Hitung paket per thread
    requests_per_thread = [num_requests // num_threads] * num_threads
    remainder = num_requests % num_threads
    for i in range(remainder):
        requests_per_thread[i] += 1
    
    # Buat dan jalankan thread
    threads = []
    for i in range(num_threads):
        if protocol == 'tcp':
            t = threading.Thread(
                target=run_thread, 
                args=(tcp_test, target_ip, target_port, packet_size, 
                     requests_per_thread[i], timeout, results)
            )
        elif protocol == 'udp':
            t = threading.Thread(
                target=run_thread, 
                args=(udp_test, target_ip, target_port, packet_size, 
                     requests_per_thread[i], timeout, results)
            )
        elif protocol == 'icmp':
            t = threading.Thread(
                target=run_thread, 
                args=(icmp_test, target_ip, None, packet_size, 
                     requests_per_thread[i], timeout, results)
            )
        
        t.start()
        threads.append(t)
    
    # Tampilkan progress
    completed = 0
    start_time = time.time()
    while completed < num_requests:
        with threading.Lock():
            completed = len(results['requests'])
        
        elapsed = time.time() - start_time
        progress = min(100, (completed / num_requests) * 100)
        rps = completed / elapsed if elapsed > 0 else 0
        
        # Hitung statistik
        success_count = sum(1 for r in results['requests'] if r['status'] == 'SUCCESS')
        error_count = completed - success_count
        success_rate = (success_count / completed * 100) if completed > 0 else 0
        
        # Tampilkan progress
        print(f"\r📈 Progress: {progress:.1f}% | ✅: {success_count} | ❌: {error_count} | ⏱ RPS: {rps:.1f} | 💯 Success: {success_rate:.1f}%", end='')
        time.sleep(0.1)
    
    # Tunggu semua thread selesai
    for t in threads:
        t.join()
    
    # Hitung statistik akhir
    results['end_time'] = time.time()
    results['duration'] = results['end_time'] - results['start_time']
    results['total_bytes_sent'] = packet_size * num_requests
    results['total_bytes_received'] = sum(r['response_size'] for r in results['requests'])
    
    success_requests = [r for r in results['requests'] if r['status'] == 'SUCCESS']
    results['success_count'] = len(success_requests)
    results['error_count'] = num_requests - results['success_count']
    results['success_rate'] = (results['success_count'] / num_requests) * 100
    
    if success_requests:
        results['min_latency'] = min(r['latency'] for r in success_requests)
        results['max_latency'] = max(r['latency'] for r in success_requests)
        results['avg_latency'] = sum(r['latency'] for r in success_requests) / len(success_requests)
    else:
        results['min_latency'] = 0
        results['max_latency'] = 0
        results['avg_latency'] = 0
    
    
    # Tampilkan ringkasan
    print("\n\n" + "="*60)
    print(f"{Colors.BOLD}📊 HASIL PENGUJIAN{Colors.ENDC}")
    print("="*60)
    print(f"Durasi     : {results['duration']:.2f} detik")
    print(f"Data Dikirim : {results['total_bytes_sent']/1024/1024:.2f} MB")
    print(f"Data Diterima: {results['total_bytes_received']/1024:.2f} KB")
    print(f"Request Berhasil: {results['success_count']}/{num_requests}")
    print(f"Tingkat Keberhasilan: {results['success_rate']:.2f}%")
    print(f"Latensi    : Min={results['min_latency']:.2f}ms, Avg={results['avg_latency']:.2f}ms, Max={results['max_latency']:.2f}ms")
    print(f"RPS        : {num_requests/results['duration']:.2f} (Requests per Second)")
    print("="*60)
    
    input("\nTekan Enter untuk kembali ke menu...")
    return results

def run_thread(test_func, ip, port, size, count, timeout, results):
    """Menjalankan pengujian dalam thread"""
    for _ in range(count):
        if port:
            result = test_func(ip, port, size, 1, timeout, results)
        else:
            result = test_func(ip, size, 1, timeout, results)
        
        with threading.Lock():
            results['requests'].append(result)

def configuration_menu(config):
    while True:
        print_banner()
        print(f"\n{Colors.BOLD}⚙️ KONFIGURASI PENGUJIAN{Colors.ENDC}")
        print("="*60)
        print(f"1. Target IP       : {config['target_ip']}")
        print(f"2. Target Port     : {config['target_port']}")
        print(f"3. Ukuran Paket    : {config['packet_size']} bytes ({config['packet_size']/1024:.2f} KB)")
        print(f"4. Jumlah Request  : {config['num_requests']}")
        print(f"5. Jumlah Thread   : {config['num_threads']}")
        print(f"6. Timeout         : {config['timeout']}s")
        print(f"7. Kembali ke Menu Utama")
        print("="*60)
        
        choice = input("Pilih opsi untuk mengubah (1-7): ")
        
        if choice == '1':
            config['target_ip'] = input("Masukkan Target IP: ")
        elif choice == '2':
            try:
                config['target_port'] = int(input("Masukkan Target Port: "))
            except ValueError:
                print(f"{Colors.FAIL}Port harus berupa angka!{Colors.ENDC}")
                time.sleep(1)
        elif choice == '3':
            try:
                size = int(input("Masukkan Ukuran Paket (bytes): "))
                if size > MAX_PACKET_SIZE:
                    print(f"{Colors.WARNING}Ukuran paket terlalu besar, menggunakan maksimal {MAX_PACKET_SIZE} bytes{Colors.ENDC}")
                    size = MAX_PACKET_SIZE
                config['packet_size'] = size
            except ValueError:
                print(f"{Colors.FAIL}Ukuran harus berupa angka!{Colors.ENDC}")
                time.sleep(1)
        elif choice == '4':
            try:
                config['num_requests'] = int(input("Masukkan Jumlah Request: "))
            except ValueError:
                print(f"{Colors.FAIL}Jumlah harus berupa angka!{Colors.ENDC}")
                time.sleep(1)
        elif choice == '5':
            try:
                threads = int(input("Masukkan Jumlah Thread: "))
                if threads > MAX_THREADS:
                    print(f"{Colors.WARNING}Jumlah thread terlalu besar, menggunakan maksimal {MAX_THREADS}{Colors.ENDC}")
                    threads = MAX_THREADS
                config['num_threads'] = threads
            except ValueError:
                print(f"{Colors.FAIL}Jumlah harus berupa angka!{Colors.ENDC}")
                time.sleep(1)
        elif choice == '6':
            try:
                config['timeout'] = float(input("Masukkan Timeout (detik): "))
            except ValueError:
                print(f"{Colors.FAIL}Timeout harus berupa angka!{Colors.ENDC}")
                time.sleep(1)
        elif choice == '7':
            return
        else:
            print(f"{Colors.FAIL}Pilihan tidak valid!{Colors.ENDC}")
            time.sleep(1)

def main():
    # Konfigurasi default
    config = {
        'target_ip': '127.0.0.1',
        'target_port': 80,
        'packet_size': DEFAULT_PACKET_SIZE,
        'num_requests': DEFAULT_REQUESTS,
        'num_threads': DEFAULT_THREADS,
        'timeout': DEFAULT_TIMEOUT
    }
    
    # Periksa platform untuk dukungan ICMP
    global struct
    if os.name == 'nt':
        import struct
    else:
        import ctypes
        import struct
        # Untuk sistem non-Windows, perlu akses raw socket
        if os.geteuid() != 0:
            print(f"{Colors.WARNING}Perhatian: Pengujian ICMP memerlukan hak akses root{Colors.ENDC}")
    
    while True:
        print_banner()
        choice = print_menu()
        
        if choice == '1':
            run_test('tcp', config['target_ip'], config['target_port'], 
                    config['packet_size'], config['num_requests'], 
                    config['num_threads'], config['timeout'])
        elif choice == '2':
            run_test('udp', config['target_ip'], config['target_port'], 
                    config['packet_size'], config['num_requests'], 
                    config['num_threads'], config['timeout'])
        elif choice == '3':
            run_test('icmp', config['target_ip'], None, 
                    config['packet_size'], config['num_requests'], 
                    config['num_threads'], config['timeout'])
        elif choice == '4':
            configuration_menu(config)
        elif choice == '5':
            print(f"\n{Colors.OKGREEN}Terima kasih telah menggunakan Overload Server Sim!{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"{Colors.FAIL}Pilihan tidak valid! Silakan coba lagi.{Colors.ENDC}")
            time.sleep(1)

if __name__ == '__main__':
    main()