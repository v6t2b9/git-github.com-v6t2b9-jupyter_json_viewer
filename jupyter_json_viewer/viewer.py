import json
from IPython.display import HTML, display
from typing import Any, Optional

def display_json(data: Any, 
                title: Optional[str] = None,
                max_depth: int = None,
                collapsed: bool = False,
                indent_size: int = 24,
                dark_mode: bool = False) -> None:
    """
    Zeigt JSON-Daten in Jupyter Notebooks mit verbesserter visueller Hierarchie an.
    
    Args:
        data: Die JSON-Daten zum Anzeigen
        title: Optionaler Titel über der JSON-Ansicht
        max_depth: Maximale Verschachtelungstiefe zum Anzeigen
        collapsed: Ob die JSON-Ansicht initial eingeklappt sein soll
        indent_size: Größe der Einrückung in Pixeln
        dark_mode: Aktiviert das dunkle Farbschema
    """
    
    # Light/Dark Mode Farbschemata
    colors = {
        'light': {
            'background': '#f8f9fa',
            'text': '#2c3e50',
            'string': '#28a745',
            'number': '#0066cc',
            'boolean': '#e83e8c',
            'null': '#6c757d',
            'key': '#2c3e50',
            'line': '#dee2e6',
            'collapsible_bg': '#e9ecef',
            'collapsible_hover': '#dee2e6',
            'collapsible_border': '#ced4da',
            'property_hover': 'rgba(0,0,0,0.02)',
            'shadow': 'rgba(0,0,0,0.05)'
        },
        'dark': {
            'background': '#1e1e1e',
            'text': '#d4d4d4',
            'string': '#6A9955',
            'number': '#569CD6',
            'boolean': '#C586C0',
            'null': '#808080',
            'key': '#4EC9B0',  # Geändert von #9CDCFE zu einem angenehmen Grünton
            'line': '#404040',
            'collapsible_bg': '#2d2d2d',
            'collapsible_hover': '#383838',
            'collapsible_border': '#404040',
            'property_hover': 'rgba(255,255,255,0.02)',
            'shadow': 'rgba(0,0,0,0.2)'
        }
    }
    
    theme = colors['dark'] if dark_mode else colors['light']
    
    styles = f"""
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
        .json-string {{ 
            color: {theme['string']}; 
            word-break: break-word;
        }}
        .json-number {{ color: {theme['number']}; }}
        .json-boolean {{ color: {theme['boolean']}; }}
        .json-null {{ color: {theme['null']}; }}
        .json-key {{ 
            color: {theme['key']}; 
            font-weight: 600;
            margin-right: 8px;
        }}
        .json-bracket {{ 
            color: {theme['text']};
            opacity: 0.7;
        }}
        .json-container {{
            position: relative;
        }}
        .vertical-line {{
            position: absolute;
            left: 8px;
            top: 0;
            bottom: 0;
            width: 1px;
            background-color: {theme['line']};
        }}
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
            margin-left: 12px;
        }}
        .collapsed {{
            display: none;
        }}
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
    
    script = """
    <script>
        function toggleCollapse(element) {
            const content = element.nextElementSibling;
            content.classList.toggle('collapsed');
            if (content.classList.contains('collapsed')) {
                element.textContent = element.textContent.replace('▼', '▶');
            } else {
                element.textContent = element.textContent.replace('▶', '▼');
            }
        }
    </script>
    """
    
    def format_value(v: Any, depth: int = 0, path: str = '') -> str:
        if max_depth is not None and depth >= max_depth:
            return '<span class="json-string">"..."</span>'
        
        indent = depth * indent_size
        
        if isinstance(v, dict):
            if not v:
                return '<span class="json-bracket">{}</span>'
                
            collapse_class = ' collapsed' if collapsed else ''
            result = [
                f'<div class="collapsible" onclick="toggleCollapse(this)">{"▶" if collapsed else "▼"}</div>',
                f'<div class="content{collapse_class}"><div class="json-container">'
            ]
            
            for k, val in v.items():
                current_path = f"{path}.{k}" if path else k
                result.append(
                    f'<div class="property">'
                    f'<span class="depth-marker">{"┌" if k == list(v.keys())[0] else "└" if k == list(v.keys())[-1] else "├"}</span>'
                    f'<span class="json-key">"{k}"</span>'
                    f'<span class="key-value-separator">:</span>'
                    f'{format_value(val, depth + 1, current_path)}'
                    f'</div>'
                )
            
            result.append('</div></div>')
            return '\n'.join(result)
            
        elif isinstance(v, list):
            if not v:
                return '<span class="json-bracket">[]</span>'
                
            collapse_class = ' collapsed' if collapsed else ''
            result = [
                f'<div class="collapsible" onclick="toggleCollapse(this)">{"▶" if collapsed else "▼"}</div>',
                f'<div class="content{collapse_class}"><div class="json-container">'
            ]
            
            for i, item in enumerate(v):
                current_path = f"{path}[{i}]"
                result.append(
                    f'<div class="property">'
                    f'<span class="depth-marker">{"┌" if i == 0 else "└" if i == len(v)-1 else "├"}</span>'
                    f'{format_value(item, depth + 1, current_path)}'
                    f'</div>'
                )
            
            result.append('</div></div>')
            return '\n'.join(result)
            
        elif isinstance(v, str):
            return f'<span class="json-string">"{v}"</span>'
        elif isinstance(v, bool):
            return f'<span class="json-boolean">{str(v).lower()}</span>'
        elif v is None:
            return f'<span class="json-null">null</span>'
        else:
            return f'<span class="json-number">{v}</span>'
    
    html_content = styles + script
    if title:
        html_content += f'<div class="json-title">{title}</div>'
    
    html_content += f'<div class="json-viewer">{format_value(data)}</div>'
    
    display(HTML(html_content))