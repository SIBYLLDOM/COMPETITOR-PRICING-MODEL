# check_file_locks.py
"""
Helper script to check if output CSV files are locked by other processes.
Run this before running the main script to avoid PermissionError.
"""

import os
import sys

def check_file_locks():
    """Check if critical CSV files can be written to."""
    
    files_to_check = [
        "data/processed/filtered_company.csv",
        "data/processed/company_check.csv"
    ]
    
    print("=" * 60)
    print("FILE LOCK CHECKER")
    print("=" * 60)
    print("\nChecking if files can be written to...\n")
    
    all_ok = True
    
    for filepath in files_to_check:
        print(f"Checking: {filepath}")
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"  [INFO] File doesn't exist yet (will be created)")
            continue
        
        # Try to open for writing
        try:
            # Attempt to open in append mode (less destructive)
            with open(filepath, 'a') as f:
                pass
            print(f"  [OK] File is writable")
        except PermissionError:
            print(f"  [ERROR] File is LOCKED by another process!")
            print(f"         Close Excel or any program viewing this file.")
            all_ok = False
        except Exception as e:
            print(f"  [ERROR] Unexpected error: {e}")
            all_ok = False
    
    print("\n" + "=" * 60)
    
    if all_ok:
        print("[SUCCESS] All files are ready!")
        print("=" * 60)
        print("\nYou can now run: python run.py")
        return 0
    else:
        print("[FAILED] Some files are locked!")
        print("=" * 60)
        print("\n[ACTION REQUIRED]")
        print("1. Close Excel or any CSV viewer")
        print("2. Close any text editors with these files open")
        print("3. Run this checker again")
        print("\nThen run: python run.py")
        return 1

if __name__ == "__main__":
    exit_code = check_file_locks()
    sys.exit(exit_code)
