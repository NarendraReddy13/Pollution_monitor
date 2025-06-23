from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd
import matplotlib.pyplot as plt
import os
from uuid import uuid4

# Load data
try:
    df = pd.read_csv('cleaned_pollution_data.csv')
    avg_pm25 = df.groupby('city')['pm25'].mean().reset_index()
except FileNotFoundError:
    print("Error: 'cleaned_pollution_data.csv' not found.")
    avg_pm25 = pd.DataFrame(columns=['city', 'pm25'])

# Generate bar chart
def create_bar_chart(data):
    plt.figure(figsize=(10, 5))
    plt.bar(data['city'], data['pm25'], color='#1f77b4')
    plt.xlabel('City')
    plt.ylabel('Average PM2.5 (µg/m³)')
    plt.title('Average PM2.5 Levels by City')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    chart_path = 'pm25_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# Create PDF
def create_pdf_report(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Pollution Monitoring Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Average PM2.5 Levels by City", styles['Heading2']))
    elements.append(Spacer(1, 12))

    # Table
    table_data = [data.columns.tolist()] + data.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Bar chart
    chart_path = create_bar_chart(data)
    elements.append(Paragraph("PM2.5 Levels Visualization", styles['Heading2']))
    elements.append(Spacer(1, 12))
    elements.append(Image(chart_path, width=400, height=200))

    # Build PDF
    doc.build(elements)
    os.remove(chart_path)  # Clean up chart image

if __name__ == '__main__':
    create_pdf_report('pollution_report.pdf', avg_pm25)