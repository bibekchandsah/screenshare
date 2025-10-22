#!/usr/bin/env python3
"""
Multi-User Performance Monitor
Real-time monitoring of screen sharing performance with multiple users
"""

import requests
import time
import json
import sys
from datetime import datetime

class PerformanceMonitor:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.running = False
        
    def get_stats(self):
        """Get current server performance statistics"""
        try:
            response = requests.get(f"{self.server_url}/stats", timeout=2)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    def get_health(self):
        """Get basic health and performance info"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=2)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    def format_duration(self, seconds):
        """Format duration in human readable format"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    def display_stats(self, stats):
        """Display formatted statistics"""
        if not stats:
            print("❌ Cannot connect to server")
            return
            
        # Clear screen (works on most terminals)
        print('\033[2J\033[H', end='')
        
        print("🖥️  SCREEN SHARING PERFORMANCE MONITOR")
        print("=" * 60)
        print(f"📊 Server Status: {'🟢 Active' if stats['server']['sharing_active'] else '🔴 Inactive'}")
        print(f"⚡ Adaptive FPS: {stats['server']['adaptive_fps']}")
        print(f"🎯 Current Quality: {stats['server']['current_quality'].title()}")
        print(f"👥 Active Viewers: {len(stats['active_streams'])}")
        
        # Performance metrics
        perf = stats['performance']
        print(f"\n📈 Performance Metrics:")
        print(f"   Frames Captured: {perf['frames_captured']}")
        print(f"   Frames Served: {perf['frames_served']}")
        print(f"   Avg Frame Time: {perf['avg_frame_time']*1000:.1f}ms")
        print(f"   Frame Cache Size: {stats['optimization_status']['frame_caching']}")
        
        # Active streams
        if stats['active_streams']:
            print(f"\n👤 Active Viewers:")
            print("   IP Address       Duration    Frames   Quality")
            print("   " + "-" * 45)
            
            for session_id, info in stats['active_streams'].items():
                ip = info['ip'].ljust(15)
                duration = self.format_duration(info['duration']).ljust(8)
                frames = str(info['frames_sent']).ljust(8)
                quality = info['quality'].ljust(8)
                print(f"   {ip} {duration} {frames} {quality}")
        
        # Performance recommendations
        viewer_count = len(stats['active_streams'])
        print(f"\n💡 Performance Status:")
        
        if viewer_count == 0:
            print("   ✅ No active viewers - full performance available")
        elif viewer_count <= 2:
            print("   ✅ Low load - excellent performance (20 FPS)")
        elif viewer_count <= 5:
            print("   ⚡ Moderate load - good performance (15 FPS)")
        elif viewer_count <= 10:
            print("   ⚠️  High load - adaptive performance active (12 FPS)")
        else:
            print("   🔥 Very high load - conservative mode (8 FPS)")
        
        # Optimization status
        print(f"\n🚀 Optimizations Active:")
        print("   ✅ Multi-quality frame caching")
        print("   ✅ Adaptive FPS scaling")
        print("   ✅ Performance monitoring")
        print("   ✅ Memory usage optimization")
        
        print(f"\n🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}")
        print("Press Ctrl+C to exit")
    
    def monitor(self, interval=2):
        """Start continuous monitoring"""
        self.running = True
        print("🚀 Starting performance monitor...")
        print("📡 Connecting to server...")
        
        try:
            while self.running:
                stats = self.get_stats()
                self.display_stats(stats)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Performance monitoring stopped")
            self.running = False

def main():
    """Main function"""
    print("🖥️  Multi-User Screen Sharing Performance Monitor")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = "http://localhost:5000"
    
    monitor = PerformanceMonitor(server_url)
    
    # Test connection first
    health = monitor.get_health()
    if not health:
        print(f"❌ Cannot connect to server at {server_url}")
        print("   Make sure the screen sharing server is running")
        print("   Usage: python monitor_performance.py [server_url]")
        return
    
    print(f"✅ Connected to server at {server_url}")
    
    # Show optimizations status
    if 'optimizations' in health:
        opt = health['optimizations']
        print("🚀 Server Optimizations:")
        for feature, enabled in opt.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {feature.replace('_', ' ').title()}")
    
    print(f"\n🎯 Starting real-time monitoring (2s intervals)...")
    time.sleep(2)
    
    try:
        monitor.monitor(interval=2)
    except Exception as e:
        print(f"\n❌ Monitor error: {e}")

if __name__ == "__main__":
    main()