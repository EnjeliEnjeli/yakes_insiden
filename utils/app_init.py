"""
Application Initialization Utilities
Handles automatic setup tasks on application startup
"""

import os
import sys
from pathlib import Path

# Import git setup utility
from utils.git_setup import setup_pdf_folder_gitignore


def ensure_upload_folders_exist(app):
    """
    Ensure all required upload folders exist
    
    Args:
        app: Flask application instance
    """
    folders = [
        app.config.get('PDF_FOLDER', 'uploads/pdf'),
        app.config.get('UPLOAD_FOLDER', 'uploads/guides'),
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def create_gitkeep_file(folder_path):
    """
    Create .gitkeep file in folder to preserve empty directory in git
    
    Args:
        folder_path: Path to the folder
    """
    gitkeep_path = os.path.join(folder_path, '.gitkeep')
    if not os.path.exists(gitkeep_path):
        Path(gitkeep_path).touch()


def initialize_git_setup(app):
    """
    Initialize Git setup for PDF folder exclusion
    
    This function:
    1. Ensures .gitignore is properly configured
    2. Removes uploads/pdf from git tracking if already tracked
    3. Preserves all local files (no deletion)
    
    Args:
        app: Flask application instance
    """
    basedir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(basedir)
    
    print("\n" + "=" * 70)
    print("🚀 Initializing PDF Storage Configuration")
    print("=" * 70)
    
    # Run git setup
    success, messages = setup_pdf_folder_gitignore(project_root)
    
    for msg in messages:
        print(msg)
    
    print("=" * 70 + "\n")
    
    return success


def initialize_app(app):
    """
    Main initialization function to be called during app startup
    
    Args:
        app: Flask application instance
        
    Returns:
        bool: True if all initialization succeeded
    """
    try:
        # Ensure folders exist
        ensure_upload_folders_exist(app)
        
        # Initialize git configuration
        git_success = initialize_git_setup(app)
        
        # Create .gitkeep files to preserve empty directories
        pdf_folder = app.config.get('PDF_FOLDER', 'uploads/pdf')
        if os.path.exists(pdf_folder):
            create_gitkeep_file(pdf_folder)
        
        return git_success
        
    except Exception as e:
        print(f"⚠️  Warning during initialization: {str(e)}")
        print("   Application will continue, but manual setup may be needed.")
        return False
