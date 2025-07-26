import psutil
import socket
import requests
import json
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress

class NetworkConnectionMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CyberWatch - Network Connection Monitor")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        self.connections = {}
        self.geo_cache = {}
        self.monitoring = False
        
        self.setup_gui()
        
        self.monitor_thread = None
        
    def setup_gui(self):

        title_label = tk.Label(self.root, text="CyberWatch - Network Connection Monitor", 
                              font=('Arial', 16, 'bold'), fg='#00ff00', bg='#2b2b2b')
        title_label.pack(pady=10)
        
        control_frame = tk.Frame(self.root, bg='#2b2b2b')
        control_frame.pack(pady=5)
        
        self.start_btn = tk.Button(control_frame, text="Start Monitoring", 
                                  command=self.toggle_monitoring, bg='#4CAF50', fg='white',
                                  font=('Arial', 10, 'bold'))
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(control_frame, text="Refresh", 
                               command=self.refresh_connections, bg='#2196F3', fg='white',
                               font=('Arial', 10, 'bold'))
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(control_frame, text="Clear", 
                             command=self.clear_connections, bg='#f44336', fg='white',
                             font=('Arial', 10, 'bold'))
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self.root, text="Status: Stopped", 
                                    fg='#ffff00', bg='#2b2b2b', font=('Arial', 10))
        self.status_label.pack(pady=5)
        
        columns = ('Time', 'Process', 'PID', 'Protocol', 'Local Address', 
                  'Remote Address', 'Status', 'Country', 'City', 'ISP')
        
        self.tree_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'Time':
                self.tree.column(col, width=80)
            elif col in ['PID', 'Protocol', 'Status']:
                self.tree.column(col, width=70)
            elif col in ['Country', 'City']:
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=150)
        
        v_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        info_label = tk.Label(self.root, 
                             text="Shows active network connections with geolocation data. Green = Established, Yellow = Listening", 
                             fg='#cccccc', bg='#2b2b2b', font=('Arial', 9))
        info_label.pack(pady=5)
        
    def is_private_ip(self, ip):
        """Check if IP address is private/local"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
        except:
            return True
            
    def get_geolocation(self, ip):
        """Get geolocation data for IP address"""
        if ip in self.geo_cache:
            return self.geo_cache[ip]
            
        if self.is_private_ip(ip):
            geo_data = {"country": "Local", "city": "Local", "org": "Local Network"}
            self.geo_cache[ip] = geo_data
            return geo_data
            
        try:

            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                geo_data = {
                    "country": data.get("country_name", "Unknown"),
                    "city": data.get("city", "Unknown"), 
                    "org": data.get("org", "Unknown")
                }
                self.geo_cache[ip] = geo_data
                return geo_data
        except Exception as e:
            print(f"Error getting geolocation for {ip}: {e}")
            
        geo_data = {"country": "Unknown", "city": "Unknown", "org": "Unknown"}
        self.geo_cache[ip] = geo_data
        return geo_data
        
    def get_process_name(self, pid):
        """Get process name from PID"""
        try:
            process = psutil.Process(pid)
            return process.name()
        except:
            return "Unknown"
            
    def get_connections(self):
        """Get all network connections"""
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.raddr: 
                    connections.append(conn)
        except psutil.AccessDenied:
            messagebox.showerror("Error", "Access denied. Run as administrator for full functionality.")
        except Exception as e:
            print(f"Error getting connections: {e}")
            
        return connections
        
    def format_address(self, addr_tuple):
        """Format address tuple to string"""
        if addr_tuple:
            return f"{addr_tuple.ip}:{addr_tuple.port}"
        return ""
        
    def update_display(self):
        """Update the GUI with current connections"""
        current_connections = self.get_connections()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for conn in current_connections:
            if conn.raddr:  
                remote_ip = conn.raddr.ip
                
                process_name = self.get_process_name(conn.pid) if conn.pid else "System"
                pid = conn.pid if conn.pid else "N/A"
                
                geo_data = self.get_geolocation(remote_ip)
                
                current_time = datetime.now().strftime("%H:%M:%S")
                protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                local_addr = self.format_address(conn.laddr)
                remote_addr = self.format_address(conn.raddr)
                status = conn.status if hasattr(conn, 'status') else "Unknown"
                
                item = self.tree.insert('', 'end', values=(
                    current_time,
                    process_name,
                    pid,
                    protocol,
                    local_addr,
                    remote_addr,
                    status,
                    geo_data["country"],
                    geo_data["city"],
                    geo_data["org"]
                ))
                
                if status == "ESTABLISHED":
                    self.tree.item(item, tags=('established',))
                elif status == "LISTEN":
                    self.tree.item(item, tags=('listening',))
                    
        self.tree.tag_configure('established', background='#90EE90')
        self.tree.tag_configure('listening', background='#FFFFE0')
        
        connection_count = len(current_connections)
        self.status_label.config(text=f"Status: {'Monitoring' if self.monitoring else 'Stopped'} - {connection_count} connections")
        
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            self.update_display()
            time.sleep(2)
            
    def toggle_monitoring(self):
        """Start/stop monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.start_btn.config(text="Stop Monitoring", bg='#f44336')
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
        else:
            self.monitoring = False
            self.start_btn.config(text="Start Monitoring", bg='#4CAF50')
            
    def refresh_connections(self):
        """Manual refresh"""
        self.update_display()
        
    def clear_connections(self):
        """Clear the display"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.status_label.config(text="Status: Cleared")
        
    def run(self):
        """Start the application"""
        self.refresh_connections()
        
        self.root.mainloop()

if __name__ == "__main__":
    print("CyberWatch - Network Connection Monitor")
    print("Created by CyberNilsen")
    print("Starting application...")
    
    app = NetworkConnectionMonitor()
    app.run()