import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

# Create a list of filepaths from .txt files
filepaths = glob.glob("invoices/*xlsx")

# For each excel file :
for filepath in filepaths:
    # Create a pdf file
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    # Create a page
    pdf.add_page()
    # Get the file name without extension
    filename = Path(filepath).stem
    # Get invoice number and date by splitting file name
    invoice_nr, date = filename.split("-")
    # Write invoice number in pdf file
    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)
    # Write date in pdf file
    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date: .{date}", ln=1)
    # Read the excel file
    df = pd.read_excel(filepath, sheet_name="Sheet 1")
    # Create a list with each column name
    columns = list(df.columns)
    columns = [item.replace("_", " ").title() for item in columns]
    # Create a cell for each column name
    pdf.set_font(family="Times", size=10, style="B")
    pdf.set_draw_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=columns[0], border=1)
    pdf.cell(w=70, h=8, txt=columns[1], border=1)
    pdf.cell(w=30, h=8, txt=columns[2], border=1)
    pdf.cell(w=30, h=8, txt=columns[3], border=1)
    pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)
    # For each row:
    for index, row in df.iterrows():
        # Create cells
        pdf.set_font(family="Times", size=10)
        pdf.set_draw_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    # Calculate sum
    total_sum = df["total_price"].sum()
    # Create empty cells
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=70, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    # Create sum cell
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

    # Create cell with sentence for total
    pdf.set_font(family="Times", size=12, style="B")
    pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)
    # Add company logo
    pdf.image("generic company.png", w=40)
    # Get the pdf file
    pdf.output(f"PDFs/{filename}.pdf")
