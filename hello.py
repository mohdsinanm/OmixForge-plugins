from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox

from src.core.plugin_manager.plugin_api import PluginBase, API_VERSION


class Plugin(PluginBase):

    def name(self):
        return "Hello Plugin"

    def api_version(self):
        return API_VERSION

    def load(self, window, plugin_container):
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.addWidget(QLabel("<b>Hello Plugin</b>"))
        layout.addWidget(QLabel("This UI lives inside Plugins page"))
        
        plugin_container.add_plugin_widget(self.name(), self.widget)


    def unload(self):
        self.widget.deleteLater()
        self.action.deleteLater()
        
    def get_widget(self):
        return self.widget

