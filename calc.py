from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QGridLayout,
    QPushButton, QSizePolicy, QMessageBox
)
from src.core.plugin_manager.plugin_api import PluginBase, API_VERSION


class Plugin(PluginBase):
    def name(self):
        return "Calculator"

    def api_version(self):
        return API_VERSION

    def load(self, window, plugin_container):
        # Main widget
        self.widget = QWidget()
        main_layout = QVBoxLayout(self.widget)

        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(40)
        self.display.setStyleSheet("font-size: 18px;")
        main_layout.addWidget(self.display)

        # Buttons layout
        buttons_layout = QGridLayout()
        main_layout.addLayout(buttons_layout)

        # Button labels
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            buttons_layout.addWidget(btn, row, col)
            
        plugin_container.add_plugin_widget(self.name(), self.widget)

    def get_widget(self):
        return self.widget

    def unload(self):
        # Clean up widgets
        self.widget.deleteLater()

    # --- Calculator logic ---
    def on_button_click(self, char):
        if char == "=":
            try:
                # safely evaluate expression
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + char)

