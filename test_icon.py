"""
Test script to verify window icon appears in both title bar and taskbar
"""
import cv2
import numpy as np
import os
import time
import ctypes

def test_window_icon():
    """Test window icon display"""
    print("="*60)
    print("       WINDOW ICON TEST")
    print("="*60)
    
    window_name = "Icon Test Window"
    
    # Create window
    print("\n1. Creating window...")
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    
    # Set window size
    print("2. Setting window size...")
    cv2.resizeWindow(window_name, 800, 600)
    
    # Set window icon (Windows only)
    if os.name == 'nt':
        print("3. Setting window icon...")
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, 'icon.ico')
            
            if os.path.exists(icon_path):
                print(f"   ✓ Found icon: {icon_path}")
                
                # Small delay to ensure window is fully created
                time.sleep(0.1)
                
                # Get window handle - try multiple times
                hwnd = None
                for attempt in range(5):
                    hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
                    if hwnd:
                        print(f"   ✓ Window handle found: {hwnd}")
                        break
                    time.sleep(0.05)
                
                if hwnd:
                    # Load icon using LoadImage
                    IMAGE_ICON = 1
                    LR_LOADFROMFILE = 0x0010
                    
                    # Load small icon (16x16) for title bar
                    hicon_small = ctypes.windll.user32.LoadImageW(
                        0, icon_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE
                    )
                    
                    # Load large icon (32x32) for taskbar
                    hicon_large = ctypes.windll.user32.LoadImageW(
                        0, icon_path, IMAGE_ICON, 32, 32, LR_LOADFROMFILE
                    )
                    
                    # Set both icons
                    WM_SETICON = 0x0080
                    ICON_SMALL = 0
                    ICON_BIG = 1
                    
                    if hicon_small:
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
                        print("   ✓ Small icon (title bar) set")
                    
                    if hicon_large:
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_large)
                        print("   ✓ Large icon (taskbar) set")
                    
                    # Force update
                    ctypes.windll.user32.UpdateWindow(hwnd)
                    print("   ✓ Window updated")
                else:
                    print("   ✗ Could not get window handle")
            else:
                print(f"   ✗ Icon file not found: {icon_path}")
        except Exception as e:
            print(f"   ✗ Error setting icon: {e}")
    else:
        print("3. Icon setting only works on Windows")
    
    # Create a test image
    print("\n4. Displaying test image...")
    img = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    text1 = "Window Icon Test"
    text2 = "Check the title bar and taskbar!"
    text3 = "Press any key to close"
    
    cv2.putText(img, text1, (150, 250), font, 1.5, (0, 255, 0), 3)
    cv2.putText(img, text2, (100, 320), font, 1, (255, 255, 255), 2)
    cv2.putText(img, text3, (180, 380), font, 0.8, (100, 200, 255), 2)
    
    cv2.imshow(window_name, img)
    
    print("\n" + "="*60)
    print("✓ Window created!")
    print("="*60)
    print("\nCheck:")
    print("  1. Title bar - Should show icon next to window title")
    print("  2. Taskbar - Should show icon in taskbar button")
    print("  3. Alt+Tab - Should show icon in task switcher")
    print("\nPress any key in the window to close...")
    print("="*60)
    
    # Wait for key press
    cv2.waitKey(0)
    
    # Cleanup
    cv2.destroyAllWindows()
    print("\n✓ Test completed!")

if __name__ == "__main__":
    test_window_icon()
