# Jupyter JSON Viewer v1.0
**An Interactive JSON Visualization System for Jupyter Notebooks**

```ascii
╔══════════════════════════════════════════════════════════════╗
║ JUPYTER JSON VIEWER v1.0                                     ║
║ >_INTERACTIVE JSON VISUALIZATION SYSTEM                      ║
║ >>DOCUMENTATION INITIALIZED                                  ║
╚══════════════════════════════════════════════════════════════╝
```

## Overview

Jupyter JSON Viewer is a sophisticated visualization tool designed to make JSON data exploration in Jupyter Notebooks more intuitive and efficient. It transforms complex JSON structures into interactive, collapsible displays with intelligent visual hierarchy and customizable themes.

## Key Features

```ascii
>_CORE CAPABILITIES
------------------
[■] VISUAL HIERARCHY
    > Tree-style markers (┐├┘) showing data relationships
    > Color-coded data types for quick recognition
    > Clear indentation for nested structures
    > Collapsible sections for managing complexity

[■] INTERACTIVE ELEMENTS
    > Click-to-expand/collapse functionality
    > Intuitive arrow indicators (▼/▶)
    > Responsive hover effects
    > Smooth transitions

[■] THEME SUPPORT
    > Professional light and dark modes
    > Carefully chosen color palettes
    > Optimized for readability
    > Reduced eye strain for long sessions
```

## Installation

```bash
pip install jupyter-json-viewer
```

## Quick Start

```python
from jupyter_json_viewer import display_json

# Your JSON-compatible data
data = {
    "name": "example",
    "details": {
        "type": "demo",
        "values": [1, 2, 3],
        "active": True
    }
}

# Basic usage
display_json(data)

# Advanced configuration
display_json(
    data,
    title="Data Structure",    # Optional heading
    dark_mode=True,           # Enable dark theme
    collapsed=True,           # Start collapsed
    max_depth=3,             # Maximum nesting display
    indent_size=24           # Spacing size in pixels
)
```

## Configuration Options

```ascii
>_PARAMETERS
-----------
[DATA]       Any JSON-compatible Python object (required)
[TITLE]      Optional string for display heading
[MAX_DEPTH]  Integer limiting nesting visualization
[COLLAPSED]  Boolean for initial collapse state
[INDENT]     Integer for visual spacing (pixels)
[DARK_MODE]  Boolean for theme selection
```

## Theme Specifications

```ascii
>_COLOR SCHEMES
-------------
LIGHT THEME                 DARK THEME
Background: #f8f9fa         Background: #1e1e1e
Text:       #2c3e50         Text:       #d4d4d4
Strings:    #28a745         Strings:    #6A9955
Numbers:    #0066cc         Numbers:    #569CD6
Booleans:   #e83e8c         Booleans:   #C586C0
Keys:       #2c3e50         Keys:       #4EC9B0
```

## Visual Structure Guide

The viewer creates a clear visual hierarchy:

```ascii
>_STRUCTURE
---------
┐ Root level elements
├ Middle elements with siblings
└ Last elements in their level
  └ Nested structures
    └ Further nesting
```

## Technical Requirements

```ascii
>_PREREQUISITES
------------
- Python 3.6+
- IPython 7.0.0+
- Jupyter Notebook/Lab
```

## Security Features

The viewer implements several security measures:
- HTML escaping for title text
- UUID-based element isolation
- Proper error handling and reporting
- Type-safe data processing

## Error Handling

The viewer provides clear error messages for common issues:
- Invalid JSON structures
- Unsupported data types
- Malformed input data
- Display rendering problems

## License

```ascii
╔════════════════════════════════════════════════╗
║ GNU General Public License v3.0                ║
║ Copyright (c) 2024                            ║
║ Developed by Johannes Kaindl                  ║
╚════════════════════════════════════════════════╝
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/jupyter-json-viewer
cd jupyter-json-viewer

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Support

For questions and support:
1. Check the [issues page](https://github.com/yourusername/jupyter-json-viewer/issues)
2. Review existing questions
3. Create a new issue if needed

---

The viewer works best with modern browsers and updated Jupyter environments. For optimal performance, keep your Python packages up to date.