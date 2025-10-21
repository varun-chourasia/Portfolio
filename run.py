#!/usr/bin/env python
"""
Portfolio Website Launcher
Quick start script for development
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✓ Python version OK")
    
    # Check if .env exists
    env_path = Path(".env")
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("Please create .env file")
        return False
    print("✓ .env file found")
    
    return True

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting server...")
    print("=" * 50)
    print("Portfolio website is running!")
    print("Open: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    os.system("python app.py")

def main():
    """Main execution"""
    print("=" * 50)
    print("Portfolio Website Launcher")
    print("=" * 50)
    
    if not check_requirements():
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)
    
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
