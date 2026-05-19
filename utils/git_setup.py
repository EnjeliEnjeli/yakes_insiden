"""
Git Configuration Utility
Handles automatic setup of .gitignore and removal of tracked files from git
"""

import os
import subprocess
import sys


def run_git_command(cmd, cwd=None):
    """
    Run git command safely and return result
    
    Args:
        cmd: List of command parts (e.g., ['git', 'status'])
        cwd: Working directory
        
    Returns:
        Tuple of (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, '', 'Command timeout'
    except Exception as e:
        return 1, '', str(e)


def is_git_repo(path):
    """Check if path is inside a git repository"""
    code, _, _ = run_git_command(['git', 'rev-parse', '--git-dir'], cwd=path)
    return code == 0


def is_path_tracked_in_git(repo_root, path_relative):
    """
    Check if a path is tracked in git
    
    Args:
        repo_root: Root directory of git repository
        path_relative: Relative path to check (e.g., 'uploads/pdf')
        
    Returns:
        Boolean: True if path is tracked
    """
    code, stdout, _ = run_git_command(
        ['git', 'ls-files', '--others', '--exclude-standard', path_relative],
        cwd=repo_root
    )
    
    # If the path appears in ls-files output, it's tracked
    return code == 0 and path_relative not in stdout


def untrack_from_git(repo_root, path_relative):
    """
    Remove a directory from git tracking without deleting files
    
    Args:
        repo_root: Root directory of git repository
        path_relative: Relative path to untrack
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    print(f"⏳ Untracking '{path_relative}' from git...")
    
    code, stdout, stderr = run_git_command(
        ['git', 'rm', '--cached', '-r', '--force', path_relative],
        cwd=repo_root
    )
    
    if code == 0:
        # Stage the removal
        run_git_command(['git', 'add', path_relative], cwd=repo_root)
        message = f"✅ Successfully untracked '{path_relative}' from git\n   (Files remain in your local computer)"
        return True, message
    else:
        # If error is "did not match any files", it means folder wasn't tracked
        if 'did not match any files' in stderr:
            message = f"ℹ️  Folder '{path_relative}' is not currently tracked in git"
            return True, message
        else:
            message = f"⚠️  Error untracking: {stderr}"
            return False, message


def setup_pdf_folder_gitignore(project_root):
    """
    Main setup function to configure .gitignore and remove tracked PDF folders
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        Tuple of (success: bool, messages: list)
    """
    messages = []
    pdf_relative_path = 'uploads/pdf'
    
    # 1. Check if it's a git repo
    if not is_git_repo(project_root):
        messages.append("ℹ️  Not a git repository. Skipping git cleanup.")
        return True, messages
    
    messages.append("🔍 Checking Git status...")
    
    # 2. Check if uploads/pdf is tracked in git
    if is_path_tracked_in_git(project_root, pdf_relative_path):
        success, msg = untrack_from_git(project_root, pdf_relative_path)
        messages.append(msg)
        if not success:
            return False, messages
    else:
        messages.append(f"✅ Folder '{pdf_relative_path}' is already not tracked")
    
    # 3. Ensure .gitignore exists and contains the pattern
    gitignore_path = os.path.join(project_root, '.gitignore')
    pdf_ignore_pattern = 'uploads/pdf/'
    
    # Read current .gitignore
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
    else:
        gitignore_content = ''
    
    # Check if pattern already exists
    if pdf_ignore_pattern not in gitignore_content:
        with open(gitignore_path, 'a') as f:
            if gitignore_content and not gitignore_content.endswith('\n'):
                f.write('\n')
            f.write(f"{pdf_ignore_pattern}\n")
        messages.append(f"✅ Updated .gitignore to exclude '{pdf_relative_path}'")
    else:
        messages.append(f"✅ .gitignore already configured for '{pdf_relative_path}'")
    
    return True, messages


def main():
    """Entry point when script is run directly"""
    # Get project root (assumes this script is in utils/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print("=" * 60)
    print("PDF Folder Git Setup")
    print("=" * 60)
    
    success, messages = setup_pdf_folder_gitignore(project_root)
    
    for msg in messages:
        print(msg)
    
    print("=" * 60)
    
    if success:
        print("✅ Setup completed successfully!")
        print("\n📋 Summary:")
        print("   • PDF files are stored in: uploads/pdf/")
        print("   • Folder is excluded from GitHub commits")
        print("   • Local files are preserved (no files deleted)")
        return 0
    else:
        print("❌ Setup encountered errors!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
