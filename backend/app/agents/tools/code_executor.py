"""
Agent Tools - Code Executor
Simple and safe code execution for agents.
"""
import sys
import io
import contextlib
from typing import Dict, Any


class CodeExecutor:
    """
    Simple code executor for agents.
    Executes Python code in a restricted environment.
    """

    def __init__(self):
        self.max_execution_time = 10  # seconds
        self.allowed_imports = [
            'json', 'math', 'datetime', 'collections', 're', 
            'itertools', 'functools', 'typing'
        ]

    def execute(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute Python code and return the result.
        
        Args:
            code: Python code to execute
            context: Variables to make available in the execution context
            
        Returns:
            Dict with 'success', 'output', 'error', 'result'
        """
        # Create execution context
        exec_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'reversed': reversed,
                'isinstance': isinstance,
                'type': type,
            }
        }
        
        # Add allowed imports
        for module_name in self.allowed_imports:
            try:
                exec_globals[module_name] = __import__(module_name)
            except ImportError:
                pass
        
        # Add context variables
        if context:
            exec_globals.update(context)
        
        # Capture stdout
        stdout = io.StringIO()
        result = None
        error = None
        
        try:
            with contextlib.redirect_stdout(stdout):
                # Execute code
                exec_result = exec(code, exec_globals)
                
                # Try to get the result from the last expression
                if 'result' in exec_globals:
                    result = exec_globals['result']
                    
            success = True
            output = stdout.getvalue()
            
        except Exception as e:
            success = False
            output = stdout.getvalue()
            error = f"{type(e).__name__}: {str(e)}"
        
        return {
            'success': success,
            'output': output,
            'error': error,
            'result': result
        }

    def validate_code(self, code: str) -> Dict[str, Any]:
        """
        Validate code without executing it.
        
        Returns:
            Dict with 'valid', 'errors'
        """
        try:
            compile(code, '<string>', 'exec')
            return {'valid': True, 'errors': []}
        except SyntaxError as e:
            return {
                'valid': False,
                'errors': [f"Syntax error at line {e.lineno}: {e.msg}"]
            }


# Global instance
code_executor = CodeExecutor()
