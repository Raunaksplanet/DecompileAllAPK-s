#!/usr/bin/env python3
import os
import sys
import subprocess
from multiprocessing import Pool
from pathlib import Path

def decompile_apk(apk_path):
    """Decompile a single APK file using apktool"""
    apk_path = Path(apk_path)
    output_dir = apk_path.parent / f"{apk_path.stem}_decompiled"
    
    try:
        # Run apktool (make sure it's in your PATH or provide full path)
        result = subprocess.run(
            ["apktool", "d", str(apk_path), "-o", str(output_dir), "-f"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Successfully decompiled: {apk_path.name}")
            return True
        else:
            print(f"❌ Failed to decompile {apk_path.name}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error decompiling {apk_path.name}: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python apk_decompiler.py <folder_with_apks>")
        sys.exit(1)
    
    folder_path = Path(sys.argv[1])
    if not folder_path.is_dir():
        print(f"Error: {folder_path} is not a valid directory")
        sys.exit(1)
    
    # Find all APK files in the directory
    apk_files = list(folder_path.glob("*.apk"))
    if not apk_files:
        print(f"No APK files found in {folder_path}")
        sys.exit(0)
    
    print(f"Found {len(apk_files)} APK files to decompile")
    
    # Set fixed number of parallel processes (32 in this case)
    num_processes = 128
    print(f"Decompiling with {num_processes} parallel processes...")
    
    # Create a pool of workers and process the files
    with Pool(processes=num_processes) as pool:
        results = pool.map(decompile_apk, apk_files)
    
    # Print summary
    success_count = sum(results)
    print(f"\nDecompilation complete! Success: {success_count}/{len(apk_files)}")

if __name__ == "__main__":
    main()
