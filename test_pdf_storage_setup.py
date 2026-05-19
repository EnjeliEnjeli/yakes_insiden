#!/usr/bin/env python
"""
Test Script - PDF Storage Git Setup Verification
Run this to verify the PDF storage system is working correctly
"""

import os
import sys
import subprocess
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def check_file_exists(path, name):
    """Check if file exists"""
    if os.path.exists(path):
        print_success(f"{name} exists at {path}")
        return True
    else:
        print_error(f"{name} NOT FOUND at {path}")
        return False

def check_gitignore_content(project_root):
    """Check if .gitignore contains PDF exclusion"""
    gitignore_path = os.path.join(project_root, '.gitignore')
    
    if not os.path.exists(gitignore_path):
        print_error(".gitignore does not exist")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    # Check for uploads/pdf pattern
    if 'uploads/pdf' in content:
        print_success(".gitignore contains 'uploads/pdf' exclusion rule")
        return True
    else:
        print_error(".gitignore does NOT contain 'uploads/pdf' exclusion")
        return False

def check_git_repo(project_root):
    """Check if project is a git repository"""
    git_dir = os.path.join(project_root, '.git')
    if os.path.exists(git_dir):
        print_success("Project is a git repository")
        return True
    else:
        print_warning("Project is NOT a git repository")
        return False

def check_pdf_folder_tracked(project_root):
    """Check if uploads/pdf is tracked in git"""
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--others', '--exclude-standard', 'uploads/pdf'],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            if 'uploads/pdf' not in result.stdout:
                print_success("uploads/pdf is NOT tracked in git (good!)")
                return True
            else:
                print_warning("uploads/pdf appears to be tracked in git")
                return False
        else:
            print_warning("Could not check git tracking status")
            return False
    except Exception as e:
        print_warning(f"Error checking git status: {str(e)}")
        return False

def check_pdf_folder_permissions(project_root):
    """Check if uploads/pdf is readable/writable"""
    pdf_folder = os.path.join(project_root, 'uploads', 'pdf')
    
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder, exist_ok=True)
        print_info(f"Created {pdf_folder}")
    
    if os.access(pdf_folder, os.R_OK) and os.access(pdf_folder, os.W_OK):
        print_success(f"uploads/pdf folder has read/write permissions")
        return True
    else:
        print_error(f"uploads/pdf folder missing read/write permissions")
        return False

def check_utils_files(project_root):
    """Check if utility files exist"""
    utils_files = [
        'utils/__init__.py',
        'utils/git_setup.py',
        'utils/app_init.py',
    ]
    
    all_exist = True
    for file in utils_files:
        path = os.path.join(project_root, file)
        if os.path.exists(path):
            print_success(f"Utility file exists: {file}")
        else:
            print_error(f"Utility file MISSING: {file}")
            all_exist = False
    
    return all_exist

def check_app_py_imports(project_root):
    """Check if app.py has the initialize_app import"""
    app_py = os.path.join(project_root, 'app.py')
    
    if not os.path.exists(app_py):
        print_error("app.py not found")
        return False
    
    with open(app_py, 'r') as f:
        content = f.read()
    
    if 'from utils import initialize_app' in content:
        print_success("app.py imports initialize_app")
        return True
    else:
        print_error("app.py does NOT import initialize_app")
        return False

def main():
    print_header("🧪 PDF Storage Setup Verification Test")
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    print_info(f"Project root: {project_root}")
    print_info(f"Working directory: {os.getcwd()}")
    
    # Run checks
    checks = [
        ("Core Files", [
            ("app.py", lambda: check_file_exists(os.path.join(project_root, 'app.py'), "app.py")),
            (".gitignore", lambda: check_file_exists(os.path.join(project_root, '.gitignore'), ".gitignore")),
        ]),
        ("Git Configuration", [
            ("Is Git Repo", lambda: check_git_repo(project_root)),
            (".gitignore Content", lambda: check_gitignore_content(project_root)),
            ("Git Tracking Status", lambda: check_pdf_folder_tracked(project_root)),
        ]),
        ("Utility Files", [
            ("Utils Modules", lambda: check_utils_files(project_root)),
        ]),
        ("Application Setup", [
            ("app.py Imports", lambda: check_app_py_imports(project_root)),
        ]),
        ("Folder Permissions", [
            ("uploads/pdf Permissions", lambda: check_pdf_folder_permissions(project_root)),
        ]),
    ]
    
    total_checks = 0
    passed_checks = 0
    
    for category, category_checks in checks:
        print_header(f"📋 {category}")
        for check_name, check_func in category_checks:
            total_checks += 1
            try:
                result = check_func()
                if result:
                    passed_checks += 1
            except Exception as e:
                print_error(f"Exception in {check_name}: {str(e)}")
    
    # Summary
    print_header("📊 Test Summary")
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {Colors.GREEN}{passed_checks}{Colors.RESET}")
    print(f"Failed: {Colors.RED}{total_checks - passed_checks}{Colors.RESET}")
    
    if passed_checks == total_checks:
        print_success("\nAll checks passed! PDF Storage setup is configured correctly.")
        return 0
    else:
        print_error(f"\n{total_checks - passed_checks} check(s) failed. Please review above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
