import os
import pathlib
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from datetime import datetime
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.layout.table.table import TableCell

import random

class Report:

    def __init__(self):
        self.current_fulfillment = None


    def generate_stock_report(self, current_stock):
        print("Generating stock report...")
        
        # Add page
        result = self.add_page()
        page_layout = result["page_layout"]
        pdf = result["pdf"]

        # Header information
        page_layout.add(self.build_report_information())  
        
        # Add paragraph for spacing  
        page_layout.add(Paragraph(" "))

        # Table content
        page_layout.add(self.build_stock_content(current_stock))

        with open("reports/stock_report.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)


    def generate_fulfilled_report(self, fulfilment_data):
        print("Generating order fulfillment report...")
        # Add page
        result = self.add_page()
        page_layout = result["page_layout"]
        pdf = result["pdf"]

        # Header information
        page_layout.add(self.build_report_information())  
        
        # Add paragraph for spacing  
        page_layout.add(Paragraph(" "))

        # Table content
        page_layout.add(self.build_fulfil_content(fulfilment_data))

        with open("reports/fulfilled_report.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)


    # HELPER FUNCTIONS
    def add_page(self):
        wd = pathlib.Path().resolve()
        abs_file_path = os.path.join(wd, "assets/logo.png")

        # Create document
        pdf = Document()

        page = Page()
        pdf.append_page(page)

        page_layout = SingleColumnLayout(page)
        page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
        page_layout.add(    
        Image(        
        pathlib.Path(abs_file_path),        
        width=Decimal(110),        
        height=Decimal(110),    
        ))
        return {"page_layout": page_layout, "pdf": pdf}


    def build_report_information(self):    
        table = Table(number_of_rows=5, number_of_columns=2, column_widths=[Decimal(3), Decimal(1)])
        
        table.add(Paragraph("123 Newcastle Rd"))      
        now = datetime.now()    
        table.add(Paragraph("Date: %d/%d/%d" % (now.day, now.month, now.year)))
        
        table.add(Paragraph("Newcastle, NSW, 2300"))    
        table.add(Paragraph("Report #: %d" % random.randint(1000, 10000)))   
        
        table.add(Paragraph("Ph: 123-456-789"))    
        table.add(Paragraph(" "))
        
        table.add(Paragraph("orders@nomss.com.au"))    
        table.add(Paragraph(" "))

        table.add(Paragraph("www.noms.com.au"))
        table.add(Paragraph(" "))

        table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
        table.no_borders()
        return table


    def build_stock_content(self, current_stock):  
        table = Table(number_of_rows=len(current_stock)+1, number_of_columns=4)  
        for h in ["PRODUCT_ID", "QTY", "STOCK_IN", "REORDER_AMNT"]:  
            table.add(  
                TableCell(  
                    Paragraph(h, font_color=X11Color("Black"), font="Helvetica-Bold",),  
                    border_bottom=True,
                    border_color=X11Color("Black"),
                    border_width=Decimal(2),
                    border_left=False,
                    border_right=False,
                    border_top=False
                )  
            )  
    
        odd_color = HexColor("BBBBBB")  
        even_color = HexColor("FFFFFF")  
        for row_number, item in enumerate( current_stock ):  
            c = even_color if row_number % 2 == 0 else odd_color  
            table.add(TableCell(Paragraph(str(item["productId"])), background_color=c, border_width=Decimal(0)))  
            table.add(TableCell(Paragraph(str(item["description"])), background_color=c, border_width=Decimal(0)))  
            table.add(TableCell(Paragraph(str(item["quantityOnHand"])), background_color=c, border_width=Decimal(0)))  
            table.add(TableCell(Paragraph(str(item["reorderAmount"])), background_color=c, border_width=Decimal(0)))  
        
        table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
        return table


    def build_fulfil_content(self, current_stock):  
        table = Table(number_of_rows=1, number_of_columns=3)  
        odd_color = HexColor("BBBBBB")  
        even_color = HexColor("FFFFFF")

        for h in ["ORDER_ID", "DATE", "STATUS"]:  
            table.add(  
                TableCell(  
                    Paragraph(h, font_color=X11Color("Black"), font="Helvetica-Bold",),  
                    border_bottom=True,
                    border_color=X11Color("Black"),
                    border_width=Decimal(2),
                    border_left=False,
                    border_right=False,
                    border_top=False
                )  
            )
            
        if len(current_stock["Fulfilled"])>0:
            table._number_of_rows += len(current_stock["Fulfilled"]) + 1
            for h in ["Fulfilled", " ", " "]:  
                table.add(TableCell(  
                        Paragraph(h, font_color=X11Color("Black"), font="Helvetica-Bold",),  
                        border_bottom=False,
                        border_color=X11Color("Black"),
                        border_width=Decimal(2),
                        border_left=False,
                        border_right=False,
                        border_top=False
                    ))

            for row_number, item in enumerate( current_stock["Fulfilled"] ):  
                c = even_color if row_number % 2 == 0 else odd_color  
                table.add(TableCell(Paragraph(str(item["orderId"])), background_color=c, border_width=Decimal(0)))  
                table.add(TableCell(Paragraph(str(item["dateCreated"])), background_color=c, border_width=Decimal(0)))  
                table.add(TableCell(Paragraph(str(item["status"])), background_color=c, border_width=Decimal(0)))  

        if len(current_stock["Unfulfilled"])>0:
            table._number_of_rows += len(current_stock["Unfulfilled"]) + 1
            for h in ["Unfulfilled", " ", " "]:  
                table.add(TableCell(  
                        Paragraph(h, font_color=X11Color("Black"), font="Helvetica-Bold",),  
                        border_bottom=False,
                        border_color=X11Color("Black"),
                        border_width=Decimal(2),
                        border_left=False,
                        border_right=False,
                        border_top=False
                    ))  

            for row_number, item in enumerate( current_stock["Unfulfilled"] ):  
                c = even_color if row_number % 2 == 0 else odd_color  
                table.add(TableCell(Paragraph(str(item["orderId"])), background_color=c, border_width=Decimal(0)))  
                table.add(TableCell(Paragraph(str(item["dateCreated"])), background_color=c, border_width=Decimal(0)))  
                table.add(TableCell(Paragraph(str(item["status"])), background_color=c, border_width=Decimal(0)))  
        
        table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        return table