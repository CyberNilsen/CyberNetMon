import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
from monitor import NetworkMonitor, Connection
from typing import List

class CleanStyle:
    """Simplified, professional color scheme with fewer colors"""
    BG_PRIMARY = '#1a1a1a'      
    BG_SECONDARY = '#2d2d2d'    
    BG_CARD = '#353535'         
    
    ACCENT_BLUE = '#007acc'     
    ACCENT_GREEN = '#28a745'    
    ACCENT_RED = '#dc3545'      
    
    TEXT_PRIMARY = '#ffffff'    
    TEXT_SECONDARY = '#b0b0b0'  
    TEXT_MUTED = '#808080'      
    
    STATUS_ACTIVE = '#28a745'   
    STATUS_WARNING = '#ffc107'  
    STATUS_INACTIVE = '#6c757d' 

class AnimatedButton(tk.Button):
    """Simplified button with hover effect"""
    def __init__(self, parent, text, command=None, style_type="primary", **kwargs):
        color_map = {
            "primary": (CleanStyle.ACCENT_BLUE, '#005a9e'),
            "success": (CleanStyle.ACCENT_GREEN, '#1e7e34'),
            "danger": (CleanStyle.ACCENT_RED, '#bd2130')
        }
        
        self.normal_color, self.hover_color = color_map.get(style_type, color_map["primary"])
        
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=self.normal_color,
            fg=CleanStyle.TEXT_PRIMARY,
            font=('Arial', 10, 'bold'),
            padx=20, pady=12,
            relief='flat',
            cursor='hand2',
            bd=0,
            activebackground=self.hover_color,
            activeforeground=CleanStyle.TEXT_PRIMARY,
            **kwargs
        )
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, e):
        self.config(bg=self.hover_color)
        
    def _on_leave(self, e):
        self.config(bg=self.normal_color)

class SimpleFrame(tk.Frame):
    """Simplified frame with consistent styling"""
    def __init__(self, parent, bg_color=None, **kwargs):
        bg = bg_color or CleanStyle.BG_SECONDARY
        super().__init__(parent, bg=bg, relief='flat', bd=1, **kwargs)

class StatusIndicator(tk.Frame):
    """Simple status indicator without excessive animation"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=CleanStyle.BG_SECONDARY, **kwargs)
        
        self.indicator = tk.Label(
            self,
            text="●",
            font=('Arial', 16),
            bg=CleanStyle.BG_SECONDARY,
            fg=CleanStyle.STATUS_INACTIVE
        )
        self.indicator.pack()
        
        self.status_text = tk.Label(
            self,
            text="OFFLINE",
            font=('Arial', 8, 'bold'),
            bg=CleanStyle.BG_SECONDARY,
            fg=CleanStyle.TEXT_MUTED
        )
        self.status_text.pack()
        
    def set_status(self, status, text):
        color_map = {
            "online": CleanStyle.STATUS_ACTIVE,
            "connecting": CleanStyle.STATUS_WARNING,
            "offline": CleanStyle.STATUS_INACTIVE
        }
        
        color = color_map.get(status, CleanStyle.STATUS_INACTIVE)
        self.indicator.config(fg=color)
        self.status_text.config(text=text.upper(), fg=color)

class CyberWatchGUI:
    """Simplified GUI with clean, professional styling"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.monitor = NetworkMonitor()
        self.connections_data = []
        
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        self.monitor.set_update_callback(self.update_connections_display)
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("CyberWatch")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        self.root.configure(bg=CleanStyle.BG_PRIMARY)
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1400x800+{x}+{y}")
        
    def setup_styles(self):
        """Configure simplified ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(
            "Clean.Treeview",
            background=CleanStyle.BG_CARD,
            foreground=CleanStyle.TEXT_PRIMARY,
            fieldbackground=CleanStyle.BG_CARD,
            borderwidth=0,
            font=('Arial', 9),
            rowheight=25
        )
        
        style.configure(
            "Clean.Treeview.Heading",
            background=CleanStyle.BG_SECONDARY,
            foreground=CleanStyle.TEXT_PRIMARY,
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        
        style.map(
            "Clean.Treeview",
            background=[('selected', CleanStyle.ACCENT_BLUE)],
            foreground=[('selected', CleanStyle.TEXT_PRIMARY)]
        )
        
        style.configure(
            "Clean.Vertical.TScrollbar",
            background=CleanStyle.BG_SECONDARY,
            troughcolor=CleanStyle.BG_PRIMARY,
            borderwidth=0
        )
        
    def create_widgets(self):
        """Create all widgets with simplified styling"""
        self.create_header()
        self.create_control_panel()
        self.create_stats_panel()
        self.create_main_content()
        self.create_status_bar()
        
    def create_header(self):
        """Create simple header"""
        header_frame = SimpleFrame(self.root, CleanStyle.BG_SECONDARY, height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_frame = tk.Frame(header_frame, bg=CleanStyle.BG_SECONDARY)
        title_frame.pack(side='left', fill='both', expand=True, padx=30, pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🛡️ CyberWatch",
            font=('Arial', 24, 'bold'),
            bg=CleanStyle.BG_SECONDARY,
            fg=CleanStyle.TEXT_PRIMARY
        )
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(
            title_frame,
            text="Network Connection Monitor",
            font=('Arial', 11),
            bg=CleanStyle.BG_SECONDARY,
            fg=CleanStyle.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor='w', pady=(2, 0))
        
        status_frame = tk.Frame(header_frame, bg=CleanStyle.BG_SECONDARY)
        status_frame.pack(side='right', padx=30, pady=20)
        
        self.status_indicator = StatusIndicator(status_frame)
        self.status_indicator.pack()
        
    def create_control_panel(self):
        """Create control buttons"""
        panel_frame = SimpleFrame(self.root, CleanStyle.BG_SECONDARY, height=70)
        panel_frame.pack(fill='x', padx=20, pady=10)
        panel_frame.pack_propagate(False)
        
        controls_container = tk.Frame(panel_frame, bg=CleanStyle.BG_SECONDARY)
        controls_container.pack(expand=True, pady=15)
        
        self.monitor_btn = AnimatedButton(
            controls_container,
            text="START MONITORING",
            command=self.toggle_monitoring,
            style_type="success"
        )
        self.monitor_btn.pack(side='left', padx=(0, 15))
        
        refresh_btn = AnimatedButton(
            controls_container,
            text="REFRESH",
            command=self.manual_refresh,
            style_type="primary"
        )
        refresh_btn.pack(side='left', padx=(0, 15))
        
        export_btn = AnimatedButton(
            controls_container,
            text="EXPORT",
            command=self.export_data,
            style_type="primary"
        )
        export_btn.pack(side='left', padx=(0, 15))
        
        clear_btn = AnimatedButton(
            controls_container,
            text="CLEAR",
            command=self.clear_display,
            style_type="danger"
        )
        clear_btn.pack(side='left')
        
    def create_stats_panel(self):
        """Create simplified statistics panel"""
        stats_frame = SimpleFrame(self.root, CleanStyle.BG_PRIMARY)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.stats_cards = {}
        stats_config = [
            ("Total Connections", "total"),
            ("TCP", "tcp"),
            ("UDP", "udp"),
            ("Established", "established"),
            ("Unique IPs", "unique_ips"),
            ("Countries", "unique_countries")
        ]
        
        for i, (title, key) in enumerate(stats_config):
            card = self.create_stats_card(stats_frame, title, key)
            card.pack(side='left', fill='both', expand=True, padx=(0, 10 if i < len(stats_config)-1 else 0))
            
    def create_stats_card(self, parent, title, key):
        """Create individual stats card"""
        card_frame = SimpleFrame(parent, CleanStyle.BG_CARD)
        
        content_frame = tk.Frame(card_frame, bg=CleanStyle.BG_CARD)
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        value_label = tk.Label(
            content_frame,
            text="0",
            font=('Arial', 18, 'bold'),
            bg=CleanStyle.BG_CARD,
            fg=CleanStyle.TEXT_PRIMARY
        )
        value_label.pack()
        
        title_label = tk.Label(
            content_frame,
            text=title,
            font=('Arial', 9),
            bg=CleanStyle.BG_CARD,
            fg=CleanStyle.TEXT_SECONDARY
        )
        title_label.pack(pady=(5, 0))
        
        self.stats_cards[key] = value_label
        return card_frame
        
    def create_main_content(self):
        """Create main table area"""
        content_frame = SimpleFrame(self.root, CleanStyle.BG_PRIMARY)
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        table_container = SimpleFrame(content_frame, CleanStyle.BG_CARD)
        table_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('time', 'process', 'protocol', 'local', 'remote', 'status', 'location')
        column_names = ('Time', 'Process', 'Protocol', 'Local Address', 'Remote Address', 'Status', 'Location')
        
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show='headings',
            style="Clean.Treeview",
            height=20
        )
        
        column_widths = {
            'time': 80, 'process': 150, 'protocol': 80, 
            'local': 180, 'remote': 180, 'status': 100, 'location': 200
        }
        
        for col, name in zip(columns, column_names):
            self.tree.heading(col, text=name, anchor='w')
            self.tree.column(col, width=column_widths.get(col, 100), anchor='w')
            
        v_scroll = ttk.Scrollbar(table_container, orient='vertical', command=self.tree.yview, style="Clean.Vertical.TScrollbar")
        h_scroll = ttk.Scrollbar(table_container, orient='horizontal', command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
        self.tree.tag_configure('normal', background=CleanStyle.BG_CARD, foreground=CleanStyle.TEXT_PRIMARY)
        self.tree.tag_configure('established', background='#2d4a2d', foreground=CleanStyle.TEXT_PRIMARY)
        self.tree.tag_configure('warning', background='#4a2d2d', foreground=CleanStyle.TEXT_PRIMARY)
        
    def create_status_bar(self):
        """Create simple status bar"""
        status_frame = SimpleFrame(self.root, CleanStyle.BG_SECONDARY, height=40)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        status_container = tk.Frame(status_frame, bg=CleanStyle.BG_SECONDARY)
        status_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.main_status_label = tk.Label(
            status_container,
            text="Ready - Click START MONITORING to begin",
            font=('Arial', 10),
            bg=CleanStyle.BG_SECONDARY,
            fg=CleanStyle.TEXT_SECONDARY
        )
        self.main_status_label.pack(side='left')
        
        self.last_update_label = tk.Label(
            status_container,
            text="",
            font=('Arial', 10),
            bg=CleanStyle.BG_SECONDARY,
            fg=CleanStyle.TEXT_MUTED
        )
        self.last_update_label.pack(side='right')
        
    def assess_threat_level(self, connection):
        """Simple threat assessment"""
        if not connection.geo_data:
            return "normal"
            
        suspicious_countries = ['Unknown', 'CN', 'RU']
        if any(country in connection.geo_data.get('country', '') for country in suspicious_countries):
            return "warning"
        elif connection.status == "ESTABLISHED":
            return "established"
        else:
            return "normal"
            
    def toggle_monitoring(self):
        """Toggle monitoring with visual feedback"""
        if not self.monitor.monitoring:
            self.monitor.start_monitoring(update_interval=2)
            self.monitor_btn.config(text="STOP MONITORING")
            self.monitor_btn.normal_color = CleanStyle.ACCENT_RED
            self.monitor_btn.hover_color = '#bd2130'
            self.monitor_btn.config(bg=CleanStyle.ACCENT_RED)
            
            self.status_indicator.set_status("online", "ACTIVE")
            self.main_status_label.config(
                text="Monitoring active - Real-time network surveillance",
                fg=CleanStyle.STATUS_ACTIVE
            )
        else:
            self.monitor.stop_monitoring()
            self.monitor_btn.config(text="START MONITORING")
            self.monitor_btn.normal_color = CleanStyle.ACCENT_GREEN
            self.monitor_btn.hover_color = '#1e7e34'
            self.monitor_btn.config(bg=CleanStyle.ACCENT_GREEN)
            
            self.status_indicator.set_status("offline", "STOPPED")
            self.main_status_label.config(
                text="Monitoring stopped - Click START to resume",
                fg=CleanStyle.STATUS_INACTIVE
            )
            
    def manual_refresh(self):
        """Manual refresh"""
        def refresh_worker():
            connections = self.monitor.get_active_connections()
            self.root.after(0, lambda: self.update_connections_display(connections))
            
        threading.Thread(target=refresh_worker, daemon=True).start()
        self.main_status_label.config(
            text="Refreshing connections...",
            fg=CleanStyle.STATUS_WARNING
        )
        
    def update_connections_display(self, connections: List[Connection]):
        """Update display with connections"""
        self.connections_data = connections
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for conn in connections:
            threat_level = self.assess_threat_level(conn)
            
            values = (
                conn.timestamp.strftime("%H:%M:%S"),
                conn.process_name[:20] + "..." if len(conn.process_name) > 20 else conn.process_name,
                conn.protocol,
                conn.local_address,
                conn.remote_address,
                conn.status,
                f"{conn.geo_data.get('city', 'Unknown')}, {conn.geo_data.get('country', 'Unknown')}" if conn.geo_data else "Unknown"
            )
            
            self.tree.insert('', 'end', values=values, tags=(threat_level,))
            
        self.update_stats()
        self.last_update_label.config(
            text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
        )
        
    def update_stats(self):
        """Update statistics"""
        stats = self.monitor.get_connection_stats()
        for key, value in stats.items():
            if key in self.stats_cards:
                self.stats_cards[key].config(text=str(value))
                
    def export_data(self):
        """Export data functionality"""
        if not self.connections_data:
            messagebox.showwarning("No Data", "No connection data to export.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")],
            title="Export Connection Data"
        )
        
        if filename:
            try:
                exported_file = self.monitor.export_connections(filename)
                messagebox.showinfo("Export Successful", f"Data exported to:\n{exported_file}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
                
    def clear_display(self):
        """Clear display"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.connections_data = []
        
        for key in self.stats_cards:
            self.stats_cards[key].config(text="0")
            
        self.main_status_label.config(
            text="Display cleared - Ready for new data",
            fg=CleanStyle.TEXT_SECONDARY
        )
        
    def run(self):
        """Run the application"""
        self.manual_refresh()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.monitor.stop_monitoring()
            
if __name__ == "__main__":
    print("CyberWatch")
    print("=" * 40)
    print("Starting application...")
    
    try:
        app = CyberWatchGUI()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Application Error", f"Failed to start CyberWatch:\n{str(e)}")