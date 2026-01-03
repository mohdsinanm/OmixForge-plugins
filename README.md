# OmixForge Plugins

This directory contains plugins for the OmixForge application. You can use these plugins as examples or templates for creating your own extensions.

## Included Examples

- **[Calculator](calc.py)**: A fully functional calculator widget demonstrating grid layouts and user interaction.
- **[Tabbed Plugin](tab_plugin.py)**: Demonstrates how to use a `QTabWidget` to organize content within a plugin.

---

# Plugin Development Guide

This guide details how to create plugins for the application. Plugins are Python scripts that integrate with the main application window using the `PluginBase` API.

## 1. Prerequisites

- **Language**: Python 3.x
- **GUI Framework**: PyQt6

## 2. Plugin Structure

Every plugin must be a single Python file containing a class named `Plugin` that inherits from `PluginBase`.

### Required Imports

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel  # + other widgets you need
from src.core.plugin_manager.plugin_api import PluginBase, API_VERSION
```

### The Plugin Class

Your class must implement specific methods to interact with the host application.

| Method | Description |
| :--- | :--- |
| `name(self)` | Returns the display name of the plugin (str). |
| `api_version(self)` | Returns the API version constant (should return `API_VERSION`). |
| `load(self, window, plugin_container)` | Called when the plugin is loaded. Initialize your UI here. |
| `get_widget(self)` | Returns the main QWidget instance of the plugin. |
| `unload(self)` | Called when the plugin is disabled/removed. Clean up resources here. |

## 3. Step-by-Step Implementation

1.  **Initialize the Widget**: In `load()`, create a `QWidget` which will hold your plugin's UI.
2.  **Build UI**: Add layouts and widgets (buttons, labels, etc.) to your main widget.
3.  **Register Plugin**: Call `plugin_container.add_plugin_widget(self.name(), self.widget)` at the end of `load()`.
4.  **Handle Interactions**: Connect signals (e.g., button clicks) to methods within your class.
5.  **Cleanup**: In `unload()`, ensure you call `self.widget.deleteLater()` to free memory.

## 4. Plugin Template
- Clone this repo
- Copy this code into a new file (e.g., `my_plugin.py`) 
- After development the plugin can be test by placing the plugin file into the `OmixForge/.omixforge/plugins` folder 
- Run the application in dev mode or install the latest version of the application to try the plugin 
- After development run ```make check``` to check if the plugin is valid
- If the plugin is valid create a PR against the main branch of the repository

```python
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
# Ensure this import path matches your project structure
from src.core.plugin_manager.plugin_api import PluginBase, API_VERSION


class Plugin(PluginBase):
    """
    A template plugin class.
    """

    def name(self):
        """
        The name of the plugin as it appears in the UI.
        """
        return "My New Plugin"

    def api_version(self):
        """
        Returns the API version to ensure compatibility.
        """
        return API_VERSION

    def load(self, window, plugin_container):
        """
        Initialize the plugin logic and UI.
        
        Args:
            window: The main application window instance.
            plugin_container: The controller that manages plugin tabs/widgets.
        """
        # 1. Create the main widget for this plugin
        self.widget = QWidget()
        
        # 2. Setup layout
        layout = QVBoxLayout(self.widget)
        
        # 3. Add UI elements
        label = QLabel("Hello from My New Plugin!")
        layout.addWidget(label)

        btn = QPushButton("Click Me")
        btn.clicked.connect(lambda: self.on_button_clicked(window))
        layout.addWidget(btn)

        # 4. Register the widget with the main application
        # This adds your widget to the application's plugin area
        plugin_container.add_plugin_widget(self.name(), self.widget)

    def get_widget(self):
        """
        Return the main widget instance.
        """
        return self.widget

    def unload(self):
        """
        Clean up resources when the plugin is disabled.
        """
        if hasattr(self, 'widget'):
            self.widget.deleteLater()

    # --- Custom Logic ---

    def on_button_clicked(self, window):
        QMessageBox.information(window, "Plugin Action", "Button was clicked inside the plugin!")

```

## 5. Tips

- **Safe Evaluation**: If you are parsing user input (like in a calculator), use `try...except` blocks to prevent crashes.
- **Widgets**: You can use any `PyQt6` widget (`QTabWidget`, `QTableWidget`, etc.) inside your plugin.
- **Context**: The `window` argument in `load()` gives you access to the main window if you need to parent dialogs or access global state.
