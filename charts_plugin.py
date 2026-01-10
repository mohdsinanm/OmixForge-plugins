from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QComboBox, 
    QLabel, QPushButton, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from src.core.plugin_manager.plugin_api import PluginBase, API_VERSION


class Plugin(PluginBase):
    def name(self):
        return "Charts Display"

    def api_version(self):
        return API_VERSION

    def load(self, window, plugin_container):

        self.widget = QWidget()
        main_layout = QVBoxLayout(self.widget)

        # Control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # Chart type selector
        control_layout.addWidget(QLabel("Chart Type:"))
        self.chart_selector = QComboBox()
        self.chart_selector.addItems([
            "Line Chart",
            "Bar Chart",
            "Scatter Plot",
            "Pie Chart",
            "Histogram",
            "Area Chart",
            "Bubble Chart"
        ])
        self.chart_selector.currentIndexChanged.connect(self.update_chart)
        control_layout.addWidget(self.chart_selector)

        # Data points control
        control_layout.addWidget(QLabel("Data Points:"))
        self.points_spinbox = QSpinBox()
        self.points_spinbox.setMinimum(5)
        self.points_spinbox.setMaximum(100)
        self.points_spinbox.setValue(20)
        self.points_spinbox.valueChanged.connect(self.update_chart)
        control_layout.addWidget(self.points_spinbox)

        # Refresh button
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.update_chart)
        control_layout.addWidget(refresh_btn)

        control_layout.addStretch()
        main_layout.addWidget(control_panel)

        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Initial chart
        self.update_chart()

        plugin_container.add_plugin_widget(self.name(), self.widget)

    def update_chart(self):
        """Update chart based on selected type"""
        chart_type = self.chart_selector.currentText()
        num_points = self.points_spinbox.value()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if chart_type == "Line Chart":
            self.draw_line_chart(ax, num_points)
        elif chart_type == "Bar Chart":
            self.draw_bar_chart(ax, num_points)
        elif chart_type == "Scatter Plot":
            self.draw_scatter_plot(ax, num_points)
        elif chart_type == "Pie Chart":
            self.draw_pie_chart(ax)
        elif chart_type == "Histogram":
            self.draw_histogram(ax, num_points)
        elif chart_type == "Area Chart":
            self.draw_area_chart(ax, num_points)
        elif chart_type == "Bubble Chart":
            self.draw_bubble_chart(ax, num_points)

        self.figure.tight_layout()
        self.canvas.draw()

    def draw_line_chart(self, ax, num_points):
        """Draw a line chart"""
        x = np.linspace(0, 10, num_points)
        y = np.sin(x) * np.cos(x/2)
        
        ax.plot(x, y, marker='o', linewidth=2, markersize=6, color='#2E86AB')
        ax.set_title('Line Chart - Sin(x) * Cos(x/2)', fontsize=12, fontweight='bold')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.grid(True, alpha=0.3)

    def draw_bar_chart(self, ax, num_points):
        """Draw a bar chart"""
        categories = [f'Cat {i+1}' for i in range(num_points)]
        values = np.random.randint(10, 100, num_points)
        
        colors = plt.cm.Set3(np.linspace(0, 1, num_points))
        ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)
        ax.set_title('Bar Chart - Random Data', fontsize=12, fontweight='bold')
        ax.set_ylabel('Values')
        ax.tick_params(axis='x', rotation=45)

    def draw_scatter_plot(self, ax, num_points):
        """Draw a scatter plot"""
        x = np.random.randn(num_points)
        y = np.random.randn(num_points)
        sizes = np.random.randint(20, 200, num_points)
        colors = np.random.rand(num_points)
        
        scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='viridis', 
                            alpha=0.6, edgecolors='black', linewidth=0.5)
        ax.set_title('Scatter Plot - Random Distribution', fontsize=12, fontweight='bold')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        self.figure.colorbar(scatter, ax=ax, label='Color Value')

    def draw_pie_chart(self, ax):
        """Draw a pie chart"""
        sizes = [30, 25, 20, 15, 10]
        labels = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        explode = (0.05, 0.05, 0, 0, 0)
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.set_title('Pie Chart - Distribution', fontsize=12, fontweight='bold')
        ax.axis('equal')

    def draw_histogram(self, ax, num_points):
        """Draw a histogram"""
        data = np.random.normal(100, 15, num_points * 5)
        
        ax.hist(data, bins=30, color='#A8DADC', edgecolor='black', linewidth=1.2)
        ax.set_title('Histogram - Normal Distribution', fontsize=12, fontweight='bold')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3, axis='y')

    def draw_area_chart(self, ax, num_points):
        """Draw an area chart"""
        x = np.linspace(0, 10, num_points)
        y1 = np.sin(x) + 2
        y2 = np.cos(x) + 2
        y3 = np.sin(x/2) + 2
        
        ax.fill_between(x, 0, y1, alpha=0.4, label='Series 1', color='#FF6B6B')
        ax.fill_between(x, y1, y1 + y2, alpha=0.4, label='Series 2', color='#4ECDC4')
        ax.fill_between(x, y1 + y2, y1 + y2 + y3, alpha=0.4, label='Series 3', color='#45B7D1')
        
        ax.set_title('Area Chart - Stacked', fontsize=12, fontweight='bold')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

    def draw_bubble_chart(self, ax, num_points):
        """Draw a bubble chart"""
        x = np.random.randn(num_points)
        y = np.random.randn(num_points)
        sizes = np.random.randint(50, 500, num_points)
        colors = np.random.randint(0, 100, num_points)
        
        scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='plasma', 
                            alpha=0.6, edgecolors='black', linewidth=1)
        ax.set_title('Bubble Chart - Variable Size Data', fontsize=12, fontweight='bold')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        self.figure.colorbar(scatter, ax=ax, label='Color Value')

    def get_widget(self):
        return self.widget

    def unload(self):
        self.widget.deleteLater()
