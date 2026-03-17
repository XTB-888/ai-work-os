"""
Unit tests for Agent Tools
"""
import pytest
from app.agents.tools.code_executor import CodeExecutor
from app.agents.tools.file_manager import FileManager


class TestCodeExecutor:
    """Test CodeExecutor tool."""

    def test_execute_simple_code(self):
        """Test executing simple Python code."""
        executor = CodeExecutor()
        result = executor.execute("result = 2 + 2")
        
        assert result['success'] is True
        assert result['result'] == 4
        assert result['error'] is None

    def test_execute_with_print(self):
        """Test code with print statements."""
        executor = CodeExecutor()
        result = executor.execute("print('Hello, World!')")
        
        assert result['success'] is True
        assert 'Hello, World!' in result['output']

    def test_execute_with_context(self):
        """Test code execution with context variables."""
        executor = CodeExecutor()
        result = executor.execute(
            "result = x + y",
            context={'x': 10, 'y': 20}
        )
        
        assert result['success'] is True
        assert result['result'] == 30

    def test_execute_with_error(self):
        """Test code execution with syntax error."""
        executor = CodeExecutor()
        result = executor.execute("result = 1 / 0")
        
        assert result['success'] is False
        assert 'ZeroDivisionError' in result['error']

    def test_validate_code_valid(self):
        """Test code validation with valid code."""
        executor = CodeExecutor()
        result = executor.validate_code("x = 1 + 1")
        
        assert result['valid'] is True
        assert len(result['errors']) == 0

    def test_validate_code_invalid(self):
        """Test code validation with invalid code."""
        executor = CodeExecutor()
        result = executor.validate_code("x = 1 +")
        
        assert result['valid'] is False
        assert len(result['errors']) > 0


class TestFileManager:
    """Test FileManager tool."""

    def test_write_and_read_file(self, tmp_path):
        """Test writing and reading a file."""
        fm = FileManager(workspace_root=str(tmp_path))
        
        # Write file
        write_result = fm.write_file("test.txt", "Hello, World!")
        assert write_result['success'] is True
        
        # Read file
        read_result = fm.read_file("test.txt")
        assert read_result['success'] is True
        assert read_result['content'] == "Hello, World!"

    def test_list_files(self, tmp_path):
        """Test listing files in a directory."""
        fm = FileManager(workspace_root=str(tmp_path))
        
        # Create some files
        fm.write_file("file1.txt", "content1")
        fm.write_file("file2.txt", "content2")
        
        # List files
        result = fm.list_files(".")
        assert result['success'] is True
        assert len(result['files']) == 2

    def test_delete_file(self, tmp_path):
        """Test deleting a file."""
        fm = FileManager(workspace_root=str(tmp_path))
        
        # Create and delete file
        fm.write_file("test.txt", "content")
        delete_result = fm.delete_file("test.txt")
        
        assert delete_result['success'] is True
        
        # Verify file is deleted
        read_result = fm.read_file("test.txt")
        assert read_result['success'] is False

    def test_path_traversal_prevention(self, tmp_path):
        """Test that path traversal is prevented."""
        fm = FileManager(workspace_root=str(tmp_path))
        
        # Try to access parent directory
        with pytest.raises(ValueError):
            fm._get_safe_path("../etc/passwd")
