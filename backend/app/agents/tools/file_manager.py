"""
Agent Tools - File Manager
Simple file operations for agents.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional


class FileManager:
    """
    Simple file manager for agents.
    Provides safe file operations within a workspace.
    """

    def __init__(self, workspace_root: str = "/tmp/aiworkos"):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def _get_safe_path(self, file_path: str) -> Path:
        """
        Get a safe path within the workspace.
        Prevents directory traversal attacks.
        """
        full_path = (self.workspace_root / file_path).resolve()
        if not str(full_path).startswith(str(self.workspace_root)):
            raise ValueError("Path outside workspace")
        return full_path

    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file.
        
        Args:
            file_path: Relative path within workspace
            content: File content
            
        Returns:
            Dict with 'success', 'path', 'error'
        """
        try:
            safe_path = self._get_safe_path(file_path)
            safe_path.parent.mkdir(parents=True, exist_ok=True)
            
            safe_path.write_text(content, encoding='utf-8')
            
            return {
                'success': True,
                'path': str(safe_path),
                'size': len(content),
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'path': file_path,
                'size': 0,
                'error': str(e)
            }

    def read_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read content from a file.
        
        Args:
            file_path: Relative path within workspace
            
        Returns:
            Dict with 'success', 'content', 'error'
        """
        try:
            safe_path = self._get_safe_path(file_path)
            
            if not safe_path.exists():
                return {
                    'success': False,
                    'content': None,
                    'error': 'File not found'
                }
            
            content = safe_path.read_text(encoding='utf-8')
            
            return {
                'success': True,
                'content': content,
                'size': len(content),
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'content': None,
                'error': str(e)
            }

    def list_files(self, directory: str = ".") -> Dict[str, Any]:
        """
        List files in a directory.
        
        Args:
            directory: Relative directory path
            
        Returns:
            Dict with 'success', 'files', 'error'
        """
        try:
            safe_path = self._get_safe_path(directory)
            
            if not safe_path.exists():
                return {
                    'success': False,
                    'files': [],
                    'error': 'Directory not found'
                }
            
            files = []
            for item in safe_path.iterdir():
                files.append({
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else 0
                })
            
            return {
                'success': True,
                'files': files,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'files': [],
                'error': str(e)
            }

    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """
        Delete a file.
        
        Args:
            file_path: Relative path within workspace
            
        Returns:
            Dict with 'success', 'error'
        """
        try:
            safe_path = self._get_safe_path(file_path)
            
            if not safe_path.exists():
                return {
                    'success': False,
                    'error': 'File not found'
                }
            
            safe_path.unlink()
            
            return {
                'success': True,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Global instance
file_manager = FileManager()
