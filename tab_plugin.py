from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTabWidget, QPushButton, QHBoxLayout, QMessageBox
)
from src.core.plugin_manager.plugin_api import PluginBase, API_VERSION


class Plugin(PluginBase):
    def name(self):
        return "Tabbed Plugin"

    def api_version(self):
        return API_VERSION

    def load(self, window, plugin_container):
        # Main plugin widget
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # --- Tab 1: Info ---
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("This is the first tab"))
        tab1_layout.addWidget(QLabel("You can add any widgets here"))
        self.tabs.addTab(tab1, "Info")

        # --- Tab 2: Actions ---
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(QLabel("This is the second tab"))

        # Example button inside tab 2
        btn = QPushButton("Click me!")
        btn.clicked.connect(lambda: QMessageBox.information(window, "Tab Plugin", "Button clicked!"))
        tab2_layout.addWidget(btn)

        self.tabs.addTab(tab2, "Actions")

        # Register with PluginsPage
        plugin_container.add_plugin_widget(self.name(), self.widget)

    def get_widget(self):
        return self.widget

    def unload(self):
        # Safe cleanup
        self.widget.deleteLater()

