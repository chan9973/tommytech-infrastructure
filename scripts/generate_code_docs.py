#!/usr/bin/env python3
"""
LLM-Wiki Code Analyzer - Auto-generates Obsidian Markdown documentation from Python projects.

Usage:
    python generate_code_docs.py <project_path> [--output output.md]
    
Example:
    python generate_code_docs.py /path/to/project --output PROJECT_DOCS.md
"""

import ast
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Set, Optional


@dataclass
class ParsedFunction:
    """Represents a parsed Python function"""
    name: str
    signature: str
    docstring: str
    line_number: int
    return_type: Optional[str] = None
    params: List[str] = field(default_factory=list)


@dataclass  
class ParsedClass:
    """Represents a parsed Python class"""
    name: str
    docstring: str
    line_number: int
    methods: List[ParsedFunction] = field(default_factory=list)
    inheritance: List[str] = field(default_factory=list)


@dataclass
class ParsedModule:
    """Represents a parsed Python module"""
    file_path: str
    module_name: str
    docstring: str
    imports: List[str] = field(default_factory=list)
    functions: List[ParsedFunction] = field(default_factory=list)
    classes: List[ParsedClass] = field(default_factory=list)


class CodeAnalyzer:
    """Analyzes Python source files and extracts structure"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.modules: Dict[str, ParsedModule] = {}
        self.all_functions: List[ParsedFunction] = []
        self.all_classes: List[ParsedClass] = []
    
    def analyze(self) -> None:
        """Analyze all Python files in project"""
        for py_file in self.project_path.rglob("*.py"):
            # Skip test files and migrations
            if any(skip in str(py_file) for skip in ['test_', '__pycache__', '.venv', '/docs/', '/venv/']):
                continue
            
            try:
                self._parse_file(py_file)
            except Exception as e:
                print(f"Warning: Could not parse {py_file}: {e}", file=sys.stderr)
    
    def _parse_file(self, file_path: Path) -> None:
        """Parse a single Python file"""
        content = file_path.read_text(encoding='utf-8')
        tree = ast.parse(content)
        
        module_name = file_path.stem
        
        # Extract docstring
        docstring = ast.get_docstring(tree) or "No description available"
        
        module = ParsedModule(
            file_path=str(file_path.relative_to(self.project_path)),
            module_name=module_name,
            docstring=docstring
        )
        
        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names = [alias.name for alias in node.names]
                    module.imports.append(f"{node.module}({' ,'.join(names)})")
        
        # Extract top-level functions and classes
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                func = self._parse_function(node)
                module.functions.append(func)
                self.all_functions.append(func)
            elif isinstance(node, ast.ClassDef):
                cls = self._parse_class(node)
                module.classes.append(cls)
                self.all_classes.append(cls)
        
        self.modules[module_name] = module
    
    def _parse_function(self, node: ast.FunctionDef) -> ParsedFunction:
        """Parse a function definition"""
        # Get parameters - use try/except for Python version compatibility
        params = []
        try:
            for arg in node.args.args:
                if arg.arg != 'self':
                    param_str = arg.arg
                    if arg.annotation is not None:
                        try:
                            annotation = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else ""
                            param_str += f": {annotation}"
                        except Exception:
                            pass
                    params.append(param_str)
            
            # Handle *args and **kwargs
            if node.args.vararg:
                params.append(f"*{node.args.vararg.arg}")
            if node.args.kwarg:
                params.append(f"**{node.args.kwarg.arg}")
        except Exception:
            pass
        
        # Get return type
        return_type = None
        if node.returns:
            try:
                return_type = ast.unparse(node.returns) if hasattr(ast, 'unparse') else ""
            except Exception:
                return_type = ""
        
        # Get docstring
        docstring = ast.get_docstring(node) or ""
        
        # Build signature
        signature = f"{node.name}({', '.join(params)})"
        if return_type:
            signature += f" -> {return_type}"
        
        return ParsedFunction(
            name=node.name,
            signature=signature,
            docstring=docstring,
            line_number=node.lineno,
            return_type=return_type,
            params=params
        )
    
    def _parse_class(self, node: ast.ClassDef) -> ParsedClass:
        """Parse a class definition"""
        docstring = ast.get_docstring(node) or "No description available"
        
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._parse_function(item))
        
        inheritance = [base.id for base in node.bases if isinstance(base, ast.Name)]
        
        return ParsedClass(
            name=node.name,
            docstring=docstring,
            line_number=node.lineno,
            methods=methods,
            inheritance=inheritance
        )


class ObsidianMarkdownGenerator:
    """Generates Obsidian-compatible Markdown documentation"""
    
    def __init__(self, analyzer: CodeAnalyzer):
        self.analyzer = analyzer
    
    def generate(self) -> str:
        """Generate full documentation markdown"""
        lines = [
            "---",
            f"created: {datetime.now().strftime('%Y-%m-%d')}",
            f"date: {datetime.now().strftime('%Y-%m-%d')}",
            "tags: [#code/architecture, #auto-generated, #documentation]",
            f"title: \"{self._extract_project_name()}\" Code Documentation",
            "status: draft",
            "---",
            "",
            f"# {self._extract_project_name()} - Code Documentation",
            "",
            f"> Auto-generated technical documentation with [[wikilink]] cross-references.",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## 📁 Module Index",
            "",
        ]
        
        # Module index table
        lines.extend([
            "| Module | Purpose | Interfaces |",
            "|--------|---------|------------|"
        ])
        
        for module_name, module in sorted(self.analyzer.modules.items()):
            purpose = module.docstring.split('\n')[0][:60] + "..." if len(module.docstring) > 60 else module.docstring
            interfaces = f"{len(module.functions)} funcs, {len(module.classes)} classes"
            lines.append(f"| [[{module_name}]] | {purpose} | {interfaces} |")
        
        lines.append("")
        lines.append("---")
        lines.append("## 🏗️ Module Details")
        lines.append("")
        
        # Module details
        for module_name, module in sorted(self.analyzer.modules.items()):
            lines.append(f"### [[{module_name}]]")
            lines.append("")
            
            # Module description
            lines.append(module.docstring)
            lines.append("")
            
            # Imports
            if module.imports:
                lines.append("**Imports:**")
                lines.append("```python")
                for imp in module.imports[:10]:  # Limit to 10
                    lines.append(f"import {imp}")
                if len(module.imports) > 10:
                    lines.append(f"... and {len(module.imports) - 10} more")
                lines.append("```")
                lines.append("")
            
            # Functions
            if module.functions:
                lines.append("#### Public Functions")
                lines.append("")
                lines.append("```python")
                for func in module.functions:
                    lines.append(f"# {func.signature}")
                    if func.docstring:
                        lines.append(f'#   """{func.docstring[:80]}"""')
                lines.append("```")
                lines.append("")
            
            # Classes
            if module.classes:
                lines.append("#### Classes")
                lines.append("")
                for cls in module.classes:
                    # Wikilink for inheritance
                    if cls.inheritance:
                        parents = ", ".join(f"[[{p}]]" for p in cls.inheritance)
                        lines.append(f"**{cls.name}** *extends*: {parents}")
                    else:
                        lines.append(f"**{cls.name}**")
                    
                    lines.append(f"{cls.docstring[:100]}")
                    if len(cls.docstring) > 100:
                        lines.append("...")
                    lines.append("")
                    
                    if cls.methods:
                        lines.append("  Methods:")
                        lines.append("  ```python")
                        for method in cls.methods[:5]:  # Limit to 5 methods
                            lines.append(f"  # {method.name}{method.signature.split('(')[1] if '(' in method.signature else '()'}")
                        if len(cls.methods) > 5:
                            lines.append(f"  # ... and {len(cls.methods) - 5} more")
                        lines.append("  ```")
                    lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # Cross-reference section
        lines.extend([
            "## 🔗 Wikilink Map",
            "",
            "Auto-generated [[wikilink]] connections to related concepts:",
            ""
        ])
        
        # Find common patterns for cross-references
        all_names = set()
        for module in self.analyzer.modules.values():
            all_names.update(f.name for f in module.functions)
            all_names.update(c.name for c in module.classes)
            all_names.update(module.module_name for module in self.analyzer.modules.values())
        
        for name in sorted(all_names)[:20]:  # Limit to 20
            lines.append(f"- [[{name}]]")
        
        lines.append("")
        lines.append("---")
        lines.append(f"<!-- Generated on {datetime.now().isoformat()} -->")
        lines.append(f"<!-- Total modules: {len(self.analyzer.modules)} -->")
        lines.append(f"<!-- Total functions: {len(self.analyzer.all_functions)} -->")
        lines.append(f"<!-- Total classes: {len(self.analyzer.all_classes)} -->")
        
        return "\n".join(lines)
    
    def _extract_project_name(self) -> str:
        """Extract project name from path"""
        name = self.analyzer.project_path.name
        name = name.replace('-', ' ').replace('_', ' ').title()
        return name


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM-Wiki Code Documentation Generator")
    parser.add_argument("project_path", help="Path to Python project to document")
    parser.add_argument("--output", "-o", help="Output markdown file path")
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)
    
    # Analyze code
    print(f"Analyzing {project_path}...")
    analyzer = CodeAnalyzer(str(project_path))
    analyzer.analyze()
    
    print(f"Found {len(analyzer.modules)} modules, {len(analyzer.all_functions)} functions, {len(analyzer.all_classes)} classes")
    
    # Generate documentation
    generator = ObsidianMarkdownGenerator(analyzer)
    markdown = generator.generate()
    
    # Write output
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = project_path / "docs" / f"{project_path.name}-documentation.md"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding='utf-8')
    
    print(f"Documentation written to: {output_path}")
    print(f"Generated {len(markdown)} characters of markdown")


if __name__ == "__main__":
    main()