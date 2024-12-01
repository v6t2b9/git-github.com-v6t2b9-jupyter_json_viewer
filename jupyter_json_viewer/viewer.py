from IPython.display import HTML, display
from typing import Any, Optional
import json

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

def get_marker(index: int, length: int) -> str:
    """Returns the marker for the current property based on its position."""
    if index == 0:
        return "┐"  # Top corner
    elif index == length - 1:
        return "┘"  # Bottom corner
    else:
        return "├"  # Middle connector

def format_value(v: Any, depth: int = 0, path: str = '', max_depth: Optional[int] = None) -> str:
    """
    Formats a value into HTML with proper styling and structure.
    
    Args:
        v: The value to format
        depth: Current nesting depth
        path: Current path in the JSON structure
        max_depth: Maximum nesting depth before truncating
        
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

    items = list(d.items())
    for i, (k, v) in enumerate(items):
        marker = get_marker(i, len(items))
        current_path = f"{path}.{k}" if path else k
        
        result.append(
            f'<div class="property">'
            f'<span class="depth-marker">{marker}</span>'
            f'<span class="json-key">"{k}"</span>'
            f'<span class="key-value-separator">:</span>'
            f'{format_value(v, depth + 1, current_path, max_depth)}'
            f'{"," if i < len(items) - 1 else ""}</div>'
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
        marker = get_marker(i, len(lst))
        current_path = f"{path}[{i}]"
        
        result.append(
            f'<div class="property">'
            f'<span class="depth-marker">{marker}</span>'
            f'{format_value(item, depth + 1, current_path, max_depth)}'
            f'{"," if i < len(lst) - 1 else ""}</div>'
        )

    result.append('</div></div>')
    return '\n'.join(result)

def generate_css(indent_size: int) -> str:
    """Generates CSS styles for the JSON viewer with dynamic theme detection."""
    return f"""
    <style id="json-viewer-styles">
    .json-viewer {{
        font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
        font-size: 10px;
        background-color: var(--theme-background);
        color: var(--theme-text);
        border-radius: 8px;
        padding: 1.5em;
        line-height: 1.6;
        box-shadow: 0 2px 8px var(--theme-shadow);
    }}
    .json-title {{
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 15px;
        color: var(--theme-text);
        border-bottom: 2px solid var(--theme-line);
        padding-bottom: 8px;
    }}
    .json-string {{ color: var(--theme-string); word-break: break-word; }}
    .json-number {{ color: var(--theme-number); }}
    .json-boolean {{ color: var(--theme-boolean); }}
    .json-null {{ color: var(--theme-null); }}
    .json-key {{
        color: var(--theme-key);
        font-weight: 600;
        margin-right: 8px;
    }}
    .json-bracket {{ color: var(--theme-text); opacity: 0.7; }}
    .json-container {{ position: relative; padding-left: {indent_size}px; }}
    .collapsible {{
        cursor: pointer;
        padding: 2px 8px;
        background-color: var(--theme-collapsible-bg);
        border-radius: 4px;
        display: inline-block;
        margin: 2px;
        transition: all 0.2s;
        border: 1px solid transparent;
    }}
    .collapsible:hover {{
        background-color: var(--theme-collapsible-hover);
        border-color: var(--theme-collapsible-border);
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
        background-color: var(--theme-property-hover);
    }}
    .key-value-separator {{
        margin: 0 8px;
        color: var(--theme-null);
    }}
    .depth-marker {{
        color: var(--theme-null);
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
    Displays JSON data in Jupyter Notebooks with enhanced visual hierarchy and dynamic theme support.
    
    This function creates an interactive visualization of JSON data that automatically adapts
    to notebook theme changes.
    
    Args:
        data: The JSON data to display (can be dict, list, or JSON-serializable object)
        title: Optional title to display above the JSON view
        max_depth: Maximum nesting depth to display before truncating
        collapsed: Whether the JSON view should be initially collapsed
        indent_size: Indentation size in pixels for nested elements
        dark_mode: Initial dark mode state (will be updated dynamically)
    """
    try:
        # Generate the base CSS with CSS variables
        styles = generate_css(indent_size)
        
        # Convert theme colors to JSON for JavaScript
        light_theme = json.dumps(get_theme_colors(False))
        dark_theme = json.dumps(get_theme_colors(True))
        
        # Generate JavaScript for theme handling and collapse functionality
        script = f"""
        <script>
        const lightTheme = {light_theme};
        const darkTheme = {dark_theme};
        
        function setThemeColors(isDark) {{
            const theme = isDark ? darkTheme : lightTheme;
            const root = document.documentElement;
            
            Object.entries(theme).forEach(([key, value]) => {{
                root.style.setProperty(`--theme-${{key}}`, value);
            }});
        }}
        
        function detectTheme() {{
            // Check for Jupyter's data-jp-theme attribute
            const jupyter = document.querySelector('[data-jp-theme-name]');
            const isDark = jupyter ? jupyter.getAttribute('data-jp-theme-name') === 'JupyterLab Dark' : false;
            setThemeColors(isDark);
            
            // Set up a mutation observer to watch for theme changes
            const observer = new MutationObserver((mutations) => {{
                mutations.forEach((mutation) => {{
                    if (mutation.attributeName === 'data-jp-theme-name') {{
                        const isDark = mutation.target.getAttribute('data-jp-theme-name') === 'JupyterLab Dark';
                        setThemeColors(isDark);
                    }}
                }});
            }});
            
            if (jupyter) {{
                observer.observe(jupyter, {{ attributes: true }});
            }}
        }}
        
        function toggleCollapse(element) {{
            const content = element.nextElementSibling;
            content.classList.toggle('collapsed');
            element.textContent = content.classList.contains('collapsed') ? '▶' : '▼';
        }}

        function initializeCollapse() {{
            const containers = document.querySelectorAll('.json-viewer .content');
            const toggles = document.querySelectorAll('.json-viewer .collapsible');
            containers.forEach((content, index) => {{
                if ({str(collapsed).lower()}) {{
                    content.classList.add('collapsed');
                    toggles[index].textContent = '▶';
                }}
            }});
        }}
        
        // Initialize theme detection and collapse state
        detectTheme();
        initializeCollapse();
        </script>
        """
        
        # Combine all components
        html_content = [styles]
        
        if title:
            escaped_title = title.replace('<', '&lt;').replace('>', '&gt;')
            html_content.append(f'<div class="json-title">{escaped_title}</div>')
        
        # Generate the JSON viewer content
        json_content = format_value(data, max_depth=max_depth)
        html_content.append(f'<div class="json-viewer">{json_content}</div>')
        
        # Add the script at the end
        html_content.append(script)
        
        # Display the combined HTML
        display(HTML('\n'.join(html_content)))
        
    except Exception as e:
        raise ValueError(f"Failed to process JSON data: {str(e)}") from e