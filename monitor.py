import psutil
import socket
import requests
import ipaddress
import threading
import time
from datetime import datetime
from typing import List, Dict, Optional

class Connection:
    """Data class to represent a network connection"""
    def __init__(self, conn_info):
        self.timestamp = datetime.now()
        self.process_name = self._get_process_name(conn_info.pid)
        self.pid = conn_info.pid if conn_info.pid else "N/A"
        self.protocol = "TCP" if conn_info.type == socket.SOCK_STREAM else "UDP"
        self.local_address = self._format_address(conn_info.laddr)
        self.remote_address = self._format_address(conn_info.raddr)
        self.remote_ip = conn_info.raddr.ip if conn_info.raddr else ""
        self.status = getattr(conn_info, 'status', 'Unknown')
        self.geo_data = None
        
    def _get_process_name(self, pid: Optional[int]) -> str:
        """Get process name from PID"""
        if not pid:
            return "System"
        try:
            process = psutil.Process(pid)
            return process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return "Unknown"
            
    def _format_address(self, addr_tuple) -> str:
        """Format address tuple to string"""
        if addr_tuple:
            return f"{addr_tuple.ip}:{addr_tuple.port}"
        return ""

class NetworkMonitor:
    """Main network monitoring class"""
    
    def __init__(self):
        self.geo_cache: Dict[str, Dict] = {}
        self.monitoring = False
        self.monitor_thread = None
        self.callback = None
        
    def set_update_callback(self, callback):
        """Set callback function for GUI updates"""
        self.callback = callback
        
    def is_private_ip(self, ip: str) -> bool:
        """Check if IP address is private/local"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
        except ValueError:
            return True
            
    def get_geolocation(self, ip: str) -> Dict[str, str]:
        """Get geolocation data for IP address with caching"""
        if ip in self.geo_cache:
            return self.geo_cache[ip]
            
        if self.is_private_ip(ip):
            geo_data = {
                "country": "Local",
                "city": "Local", 
                "org": "Local Network",
                "flag": "🏠"
            }
            self.geo_cache[ip] = geo_data
            return geo_data
            
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
            if response.status_code == 200:
                data = response.json()
                geo_data = {
                    "country": data.get("country_name", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "org": data.get("org", "Unknown ISP"),
                    "flag": self._get_country_flag(data.get("country_code", ""))
                }
                self.geo_cache[ip] = geo_data
                return geo_data
        except requests.RequestException as e:
            print(f"Error getting geolocation for {ip}: {e}")
            
        geo_data = {
            "country": "Unknown", 
            "city": "Unknown", 
            "org": "Unknown ISP",
            "flag": "❓"
        }
        self.geo_cache[ip] = geo_data
        return geo_data
        
    def _get_country_flag(self, country_code: str) -> str:
        """Convert country code to flag emoji"""
        if not country_code or len(country_code) != 2:
            return "🌍"
        
        flag = ""
        for char in country_code.upper():
            flag += chr(ord(char) - ord('A') + ord('🇦'))
        return flag
        
    def get_active_connections(self) -> List[Connection]:
        """Get all active network connections"""
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):

                if conn.raddr and not self.is_private_ip(conn.raddr.ip):
                    connection = Connection(conn)
                    connection.geo_data = self.get_geolocation(connection.remote_ip)
                    connections.append(connection)
                    
        except psutil.AccessDenied:
            print("Access denied. Run as administrator for full functionality.")
        except Exception as e:
            print(f"Error getting connections: {e}")
            
        return connections
        
    def start_monitoring(self, update_interval: int = 2):
        """Start continuous monitoring"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(update_interval,), 
            daemon=True
        )
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
            
    def _monitor_loop(self, update_interval: int):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                connections = self.get_active_connections()
                if self.callback:
                    self.callback(connections)
                time.sleep(update_interval)
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1)
                
    def get_connection_stats(self) -> Dict[str, int]:
        """Get statistics about current connections"""
        connections = self.get_active_connections()
        
        stats = {
            "total": len(connections),
            "tcp": sum(1 for c in connections if c.protocol == "TCP"),
            "udp": sum(1 for c in connections if c.protocol == "UDP"),
            "established": sum(1 for c in connections if c.status == "ESTABLISHED"),
            "unique_ips": len(set(c.remote_ip for c in connections)),
            "unique_countries": len(set(c.geo_data["country"] for c in connections if c.geo_data))
        }
        
        return stats
        
    def clear_cache(self):
        """Clear the geolocation cache"""
        self.geo_cache.clear()
        
    def export_connections(self, filename: str = None) -> str:
        """Export current connections to JSON format"""
        if not filename:
            filename = f"connections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        connections = self.get_active_connections()
        data = []
        
        for conn in connections:
            data.append({
                "timestamp": conn.timestamp.isoformat(),
                "process": conn.process_name,
                "pid": conn.pid,
                "protocol": conn.protocol,
                "local_address": conn.local_address,
                "remote_address": conn.remote_address,
                "status": conn.status,
                "country": conn.geo_data["country"] if conn.geo_data else "Unknown",
                "city": conn.geo_data["city"] if conn.geo_data else "Unknown",
                "isp": conn.geo_data["org"] if conn.geo_data else "Unknown"
            })
            
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return filename