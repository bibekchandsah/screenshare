#!/usr/bin/env python3
"""
Test script for threaded cloudflare output capture
"""

import sys
import time
from cloudflare_helper import start_cloudflare_tunnel, stop_cloudflare_tunnel

def test_threaded_tunnel():
    print("🧪 Testing Threaded Cloudflare Tunnel Output Capture")
    print("="*60)
    
    # Test the threaded approach
    print("\n1. Starting tunnel with threaded output capture...")
    success, url, process = start_cloudflare_tunnel(port=5000, protocol='http')
    
    if success and url:
        print(f"\n✅ SUCCESS! URL detected: {url}")
        
        # Let it run for 10 seconds to verify it's working
        print("\n🔄 Testing tunnel for 10 seconds...")
        time.sleep(10)
        
        # Stop the tunnel
        print("\n🛑 Stopping tunnel...")
        stop_cloudflare_tunnel(process)
        
    else:
        print("\n❌ FAILED - URL not detected")
        if process and process.poll() is None:
            print("   Process is still running, stopping it...")
            stop_cloudflare_tunnel(process)

if __name__ == "__main__":
    test_threaded_tunnel()