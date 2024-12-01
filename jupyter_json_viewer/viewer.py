# jupyter_json_viewer/viewer.py

from IPython.display import HTML, display
from typing import Any, Optional


def get_theme_colors(is_dark: bool) -> dict:
    """Returns color scheme based on dark/light mode preference."""
    return {
        'background': '#1e1e1e' if is_dark else '#f8f9fa',
        'text': '#d4d4d4' if is_dark else '#2c3e50',
        'string': '#6A9955' if is_dark else '#28a745',
        'number': '#569CD6' if is_dark else '#0066cc',
        'boolean': '#C586C0' if is_dark else '#e83e8c',
        'null': '#808080' if is_dark else '#6c757d',
        'key': '#4EC9B0' if is_dark else '#2c3e50',
        'line': '#404040' if is_dark else '#dee2e6',
        'collapsible_bg': '#2d2d2d' if is_dark else '#e9ecef',
        'collapsible_hover': '#383838' if is_dark else '#dee2e6',
        'collapsible_border': '#404040' if is_dark else '#ced4da',
        'property_hover': 'rgba(255,255,255,0.02)' if is_dark else 'rgba(0,0,0,0.02)',
        'shadow': 'rgba(0,0,0,0.2)' if is_dark else 'rgba(0,0,0,0.05)'
    }


def format_value(v: Any, depth: int = 0, path: str = '', max_depth: Optional[int] = None) -> str:
    """
    Formats a value into HTML with proper styling and structure.
    
    Args:
        v: The value to format
        depth: Current nesting depth
        path: Current path in the JSON structure
        max_depth: Maximum nesting depth
        
    Returns:
        Formatted HTML string
    """
    if max_depth is not None and depth >= max_depth:
        return '<span class="json-string">"..."</span>'

    if isinstance(v, dict):
        return format_dict(v, depth, path, max_depth)
    elif isinstance(v, list):
        return format_list(v, depth, path, max_depth)
    elif isinstance(v, str):
        return f'<span class="json-string">"{v}"</span>'
    elif isinstance(v, bool):
        return f'<span class="json-boolean">{str(v).lower()}</span>'
    elif v is None:
        return '<span class="json-null">null</span>'
    else:
        return f'<span class="json-number">{v}</span>'


def format_dict(d: dict, depth: int, path: str, max_depth: Optional[int]) -> str:
    """Formats dictionary values with proper indentation and styling."""
    if not d:
        return '<span class="json-bracket">{}</span>'

    result = [
        '<div class="collapsible" onclick="toggleCollapse(this)">▼</div>',
        '<div class="content"><div class="json-container">'
    ]

    for i, (k, v) in enumerate(d.items()):
        marker = "┌" if i == 0 else "└" if i == len(d) - 1 else "├"
        current_path = f"{path}.{k}" if path else k
        
        result.append(
            f'<div class="property">'
            f'<span class="depth-marker">{marker}</span>'
            f'<span class="json-key">"{k}"</span>'
            f'<span class="key-value-separator">:</span>'
            f'{format_value(v, depth + 1, current_path, max_depth)}'
            f'</div>'
        )

    result.append('</div></div>')
    return '\n'.join(result)


def format_list(lst: list, depth: int, path: str, max_depth: Optional[int]) -> str:
    """Formats list values with proper indentation and styling."""
    if not lst:
        return '<span class="json-bracket">[]</span>'

    result = [
        '<div class="collapsible" onclick="toggleCollapse(this)">▼</div>',
        '<div class="content"><div class="json-container">'
    ]

    for i, item in enumerate(lst):
        marker = "┌" if i == 0 else "└" if i == len(lst) - 1 else "├"
        current_path = f"{path}[{i}]"
        
        result.append(
            f'<div class="property">'
            f'<span class="depth-marker">{marker}</span>'
            f'{format_value(item, depth + 1, current_path, max_depth)}'
            f'</div>'
        )

    result.append('</div></div>')
    return '\n'.join(result)


def generate_css(theme: dict, indent_size: int) -> str:
    """Generates CSS styles for the JSON viewer."""
    return f"""
    <style>
    .json-viewer {{
        font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
        font-size: 10px;
        background-color: {theme['background']};
        color: {theme['text']};
        border-radius: 8px;
        padding: 1.5em;
        line-height: 1.6;
        box-shadow: 0 2px 8px {theme['shadow']};
    }}
    .json-title {{
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 15px;
        color: {theme['text']};
        border-bottom: 2px solid {theme['line']};
        padding-bottom: 8px;
    }}
    .json-string {{ color: {theme['string']}; word-break: break-word; }}
    .json-number {{ color: {theme['number']}; }}
    .json-boolean {{ color: {theme['boolean']}; }}
    .json-null {{ color: {theme['null']}; }}
    .json-key {{
        color: {theme['key']};
        font-weight: 600;
        margin-right: 8px;
    }}
    .json-bracket {{ color: {theme['text']}; opacity: 0.7; }}
    .json-container {{ position: relative; padding-left: {indent_size}px; }}
    .collapsible {{
        cursor: pointer;
        padding: 2px 8px;
        background-color: {theme['collapsible_bg']};
        border-radius: 4px;
        display: inline-block;
        margin: 2px;
        transition: all 0.2s;
        border: 1px solid transparent;
    }}
    .collapsible:hover {{
        background-color: {theme['collapsible_hover']};
        border-color: {theme['collapsible_border']};
    }}
    .content {{
        display: block;
        position: relative;
    }}
    .collapsed {{ display: none; }}
    .property {{
        display: flex;
        align-items: flex-start;
        padding: 2px 0;
        border-radius: 4px;
    }}
    .property:hover {{
        background-color: {theme['property_hover']};
    }}
    .key-value-separator {{
        margin: 0 8px;
        color: {theme['null']};
    }}
    .depth-marker {{
        color: {theme['null']};
        margin-right: 8px;
        font-size: 10px;
        opacity: 0.5;
    }}
    </style>
    """


def display_json(
    data: Any,
    title: Optional[str] = None,
    max_depth: Optional[int] = None,
    collapsed: bool = False,
    indent_size: int = 24,
    dark_mode: bool = False
) -> None:
    """
    Displays JSON data in Jupyter Notebooks with enhanced visual hierarchy.
    
    This function creates an interactive visualization of JSON data with collapsible
    sections, syntax highlighting, and customizable appearance.
    
    Args:
        data: The JSON data to display (can be dict, list, or JSON-serializable object)
        title: Optional title to display above the JSON view
        max_depth: Maximum nesting depth to display before truncating
        collapsed: Whether the JSON view should be initially collapsed
        indent_size: Indentation size in pixels for nested elements
        dark_mode: Activates dark color scheme for better visibility in dark notebooks
    """
    # Get theme colors and generate CSS
    theme = get_theme_colors(dark_mode)
    styles = generate_css(theme, indent_size)
    
    # Generate JavaScript for collapse functionality
    script = """
    <script>
    function toggleCollapse(element) {
        const content = element.nextElementSibling;
        content.classList.toggle('collapsed');
        element.textContent = content.classList.contains('collapsed') ? '▶' : '▼';
    }
    </script>
    """

    # Combine all components and display
    html_content = [styles, script]
    if title:
        html_content.append(f'<div class="json-title">{title}</div>')
    html_content.append(f'<div class="json-viewer">{format_value(data, max_depth=max_depth)}</div>')
    
    display(HTML('\n'.join(html_content)))