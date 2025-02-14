import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt6agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
from PySide6.QtCore import Qt

# Load the dataset
final_df = pd.read_csv(r"combined_co2_emissions.csv")

# Define a function to categorize Scope
def categorize_scope(source):
    if source in ['manufacturing', 'rnd']:
        return 'Scope 1'
    elif source in ['electricity_bills', 'offices']:
        return 'Scope 2'
    elif source in ['logistics', 'employee', 'product', 'iot']:
        return 'Scope 3'

# Creating interactive charts using matplotlib
class EmissionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CO2 Emissions Dashboard")
        self.setGeometry(100, 100, 800, 600)

        # Layout for the widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Label for the scope dropdown
        self.scope_label = QLabel("Select Scope:")
        self.layout.addWidget(self.scope_label)

        # Dropdown for Scope filter
        self.scope_dropdown = QComboBox(self)
        self.scope_dropdown.addItem("All Scopes")
        self.scope_dropdown.addItem("Scope 1")
        self.scope_dropdown.addItem("Scope 2")
        self.scope_dropdown.addItem("Scope 3")
        self.layout.addWidget(self.scope_dropdown)

        # Button to trigger chart update
        self.update_button = QPushButton("Update Chart", self)
        self.update_button.clicked.connect(self.update_charts)
        self.layout.addWidget(self.update_button)

        # Creating the matplotlib figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def emissions_trend_chart(self, selected_scope):
        filtered_df = final_df[final_df['Scope'] == selected_scope] if selected_scope != 'All' else final_df
        self.ax.clear()
        self.ax.plot(filtered_df['Date'], filtered_df['Total_CO2_Emissions (kg)'], label=f"Emissions Trend for {selected_scope}")
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Total CO₂ Emissions (kg)')
        self.ax.set_title(f"CO2 Emissions Trend for {selected_scope} over Time")
        self.ax.legend()
        self.ax.set_xticklabels(filtered_df['Date'], rotation=45, ha='right')
        self.canvas.draw()

    def emissions_heatmap(self):
        # Create a pivot table for heatmap
        heatmap_data = final_df.pivot(index='Date', columns='Scope', values='Total_CO2_Emissions (kg)')
        self.ax.clear()
        cax = self.ax.imshow(heatmap_data, cmap='viridis', aspect='auto')
        self.ax.set_xticks(range(len(heatmap_data.columns)))
        self.ax.set_xticklabels(heatmap_data.columns, rotation=45)
        self.ax.set_yticks(range(len(heatmap_data.index)))
        self.ax.set_yticklabels(heatmap_data.index)
        self.ax.set_xlabel('Scope')
        self.ax.set_ylabel('Date')
        self.ax.set_title('Heatmap of CO₂ Emissions by Scope and Date')
        self.figure.colorbar(cax)
        self.canvas.draw()

    def update_charts(self):
        selected_scope = self.scope_dropdown.currentText()
        if selected_scope != "All Scopes":
            self.emissions_trend_chart(selected_scope)
        else:
            self.emissions_heatmap()

# Application setup
app = QApplication(sys.argv)
window = EmissionApp()
window.show()
sys.exit(app.exec())

