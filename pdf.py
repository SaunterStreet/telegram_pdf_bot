from io import BytesIO
from random import randint

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PyPDF2 import PdfReader, PdfWriter

pdfmetrics.registerFont(TTFont('calibri', 'fonts/Calibri/calibri.ttf'))
pdfmetrics.registerFont(TTFont('calibri_bold', 'fonts/Calibri/calibri_bold.ttf'))
pdfmetrics.registerFont(TTFont('open', 'fonts/opensans/OpenSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('open_bold', 'fonts/opensans/OpenSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('open_semi', 'fonts/opensans/OpenSans-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('utsaahb', 'fonts/utsaah/utsaahb.ttf'))
pdfmetrics.registerFont(TTFont('utsaah', 'fonts/utsaah/utsaah.ttf'))
pdfmetrics.registerFont(TTFont('tahoma', 'fonts/Tahoma/tahoma.ttf'))
pdfmetrics.registerFont(TTFont('arial', 'fonts/Arial/ARIAL.TTF'))
pdfmetrics.registerFont(TTFont('arialb', 'fonts/Arial/ARIALBD.TTF'))
pdfmetrics.registerFont(TTFont('arial_black', 'fonts/Arial-black/arial_black.ttf'))
pdfmetrics.registerFont(TTFont('arial_blacki', 'fonts/Arial-black/arial-black-italic.ttf'))
pdfmetrics.registerFont(TTFont('verdana', 'fonts/Verdana/Verdana.ttf'))
pdfmetrics.registerFont(TTFont('ocrb10', 'fonts/ocrb10/OCRB10.TTF'))

class PDFEditor:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.reader = PdfReader(template_path)
        
    def add_text(self, output_path: str, text_data: list):
        page = self.reader.pages[0]
        packet = BytesIO()
        mediabox = page.mediabox
        page_width = float(mediabox.width) + 5
        page_height = float(mediabox.height) + 5

        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        for item in text_data:
            text = item['text']
            x = item['x']
            y = item['y']
            font = item.get('font', 'Helvetica')
            size = item.get('size', 12)
            align = item.get('align', 'left')
            color = item.get('color', '#000000')
            
            can.setFont(font, size)

            if color.startswith('#'):
            # Убираем # и конвертируем в RGB (0-1)
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16) / 255
                g = int(hex_color[2:4], 16) / 255
                b = int(hex_color[4:6], 16) / 255
                can.setFillColorRGB(r, g, b)
            else:
                # Поддержка именованных цветов
                if color == 'red':
                    can.setFillColorRGB(1, 0, 0)
                elif color == 'blue':
                    can.setFillColorRGB(0, 0, 1)
                elif color == 'green':
                    can.setFillColorRGB(0, 1, 0)
                else:
                    can.setFillColorRGB(0, 0, 0)
            
            if align == 'right':
                can.drawRightString(x, y, text)
            elif align == 'center':
                can.drawCentredString(x, y, text)
            else:
                can.drawString(x, y, text)
        
        can.save()
        packet.seek(0)
        
        overlay_pdf = PdfReader(packet)
        overlay_page = overlay_pdf.pages[0]
        page.merge_page(overlay_page)
        
        writer = PdfWriter()

        for i in range(len(self.reader.pages)):
            if i == 0:
                writer.add_page(page)  # Первая страница с текстом
            else:
                writer.add_page(self.reader.pages[i])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


class text_generator:
    def __init__(self, user_input: str):
        self.user_input = user_input

    def generate_text_data_ir(user_input) -> list:
        lines = user_input.strip().split('\n')
        
        name = lines[0].strip()
        address_street = lines[1].strip()
        address_city = lines[2].strip()
        address_postcode = lines[3].strip()

        address = f"{address_street}, {address_city}, {address_postcode}"

        emergency_no = lines[4].strip() 
        acc_enquires = lines[5].strip()
        # account_number = ''.join([str(randint(0, 9)) for _ in range(11)])
        bill_period = lines[6].strip()
        issue_date = lines[7].strip()
        acc_no = lines[8].strip()
        bill_no = lines[9].strip()
        gprn = lines[10].strip()
        amount_value1 = lines[11].strip()
        amount_value2 = lines[12].strip()
        amount_value3 = lines[13].strip()

        noformat_value = float(amount_value1) - float(amount_value2) + float(amount_value3)
        total_value = f"{noformat_value:.2f}"

        unpaid_dd = lines[14].strip()
        unpaid_dd_fee = lines[15].strip()
        vat = lines[16].strip()
        value_be_taken = lines[17].strip()
        tel = lines[18].strip()
        numbers = lines[19].strip()

        address_city_up = address_city.upper()
        
        text_data = [
            {'text': name, 'x': 157.6, 'y': 714.6, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': address, 'x': 157.6, 'y': 700.6, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': emergency_no, 'x': 511.6, 'y': 740.1, 'font': 'calibri_bold', 'size': 10, 'align': 'left'},
            {'text': acc_enquires, 'x': 517.5, 'y': 711.5, 'font': 'arial_blacki', 'size': 8, 'align': 'left'},
            {'text': bill_period, 'x': 491, 'y': 694, 'font': 'ocrb10', 'size': 9, 'align': 'left'},
            {'text': issue_date, 'x': 491, 'y': 682, 'font': 'ocrb10', 'size': 9, 'align': 'left'},
            {'text': issue_date, 'x': 491, 'y': 664, 'font': 'ocrb10', 'size': 9, 'align': 'left'},
            {'text': acc_no, 'x': 491, 'y': 645.5, 'font': 'ocrb10', 'size': 9, 'align': 'left'},
            {'text': bill_no, 'x': 491, 'y': 634, 'font': 'ocrb10', 'size': 9, 'align': 'left'},
            {'text': gprn, 'x': 491, 'y': 611.3, 'font': 'ocrb10', 'size': 9, 'align': 'left'},
            {'text': amount_value1, 'x': 440, 'y': 484, 'font': 'calibri', 'size': 9, 'align': 'right'},
            {'text': amount_value2, 'x': 440, 'y': 473, 'font': 'calibri', 'size': 9, 'align': 'right'},
            {'text': amount_value3, 'x': 440, 'y': 416.6, 'font': 'calibri', 'size': 9, 'align': 'right'},
            {'text': str(total_value), 'x': 407.5, 'y': 353.5, 'font': 'calibri_bold', 'size': 11, 'align': 'left'},
            {'text': unpaid_dd, 'x': 362, 'y': 440, 'font': 'calibri', 'size': 9, 'align': 'right'},
            {'text': unpaid_dd_fee, 'x': 362, 'y': 428.75, 'font': 'calibri', 'size': 9, 'align': 'right'},
            {'text': vat, 'x': 362, 'y': 416.6, 'font': 'calibri', 'size': 9, 'align': 'right'},
            {'text': unpaid_dd_fee, 'x': 241, 'y': 416.6, 'font': 'calibri', 'size': 9, 'align': 'left'},
            {'text': value_be_taken, 'x': 116, 'y': 366, 'font': 'calibri', 'size': 12, 'align': 'right'},
            {'text': name, 'x': 81.5, 'y': 243, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': address_street.upper(), 'x': 81.5, 'y': 231.4, 'font': 'calibri', 'size': 9, 'align': 'left'},
            {'text': f"{address_city_up}, ISRAEL", 'x': 81.5, 'y': 219.8, 'font': 'calibri', 'size': 9, 'align': 'left'},
            {'text': f"TEL: {tel}", 'x': 81.5, 'y': 208.2, 'font': 'calibri', 'size': 9, 'align': 'left'},
            {'text': acc_no, 'x': 400, 'y': 269, 'font': 'calibri', 'size': 10, 'align': 'right'},
            {'text': gprn, 'x': 400, 'y': 245, 'font': 'calibri', 'size': 10, 'align': 'right'},
            {'text': issue_date, 'x': 400, 'y': 223, 'font': 'calibri', 'size': 10, 'align': 'right'},
            {'text': str(total_value), 'x': 400, 'y': 200, 'font': 'calibri_bold', 'size': 10, 'align': 'right'},
            {'text': numbers, 'x': 345, 'y': 132, 'font': 'ocrb10', 'size': 9, 'align': 'left'}
        ]
        
        return text_data

    def generate_text_data_uk(user_input: str) -> list:
        lines = user_input.strip().split('\n')
        
        name = lines[0].strip()
        address_line1 = lines[1].strip()
        address_line2 = lines[2].strip()
        address_line3 = lines[3].strip()
        statement_date = lines[4].strip() 
        statement_period = lines[5].strip()
        cust_number = lines[6].strip()
        balance = lines[7].strip()
        value1 = lines[8].strip()
        value_2 = lines[9].strip()
        value_3 = lines[10].strip()
        value_4 = lines[11].strip()
        start_str, end_str = [s.strip() for s in statement_period.split('-')]
        
        text_data = [
            {'text': name, 'x': 219, 'y': 3008, 'font': 'open_bold', 'size': 41, 'align': 'left'},
            {'text': address_line1, 'x': 219, 'y': 2962, 'font': 'open', 'size': 41, 'align': 'left'},
            {'text': address_line2, 'x': 219, 'y': 2915, 'font': 'open', 'size': 41, 'align': 'left'},
            {'text': address_line3, 'x': 219, 'y': 2865, 'font': 'open', 'size': 41, 'align': 'left'},
            {'text': statement_date, 'x': 226, 'y': 2093, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': statement_period, 'x': 664, 'y': 2093, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': cust_number, 'x': 1282, 'y': 2351, 'font': 'open_semi', 'size': 50, 'align': 'left'},
            {'text': balance, 'x': 734, 'y': 1708, 'font': 'utsaahb', 'size': 140, 'align': 'left'},
            {'text': f"The amount of £{value1} will be taken from your", 'x': 1382, 'y': 1785, 'font': 'utsaah', 'size': 60, 'align': 'left'},
            {'text': "bank account on or within 3 days of", 'x': 1382, 'y': 1738, 'font': 'utsaah', 'size': 60, 'align': 'left'},
            {'text': statement_date, 'x': 2064, 'y': 1738, 'font': 'utsaahb', 'size': 60, 'align': 'left'},
            {'text': "Your 12 month Personal Projection for your current", 'x': 1382, 'y': 1308, 'font': 'utsaah', 'size': 55, 'align': 'left'},
            {'text': "tariff is", 'x': 1382, 'y': 1256, 'font': 'utsaah', 'size': 55, 'align': 'left'},
            {'text': value_2, 'x': 1511, 'y': 1256, 'font': 'utsaahb', 'size': 55, 'align': 'left'},
            {'text': "Your balance was in debit by", 'x': 212, 'y': 1262, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': "Total charges", 'x': 212, 'y': 1204, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': "(including VAT)", 'x': 482, 'y': 1206, 'font': 'open_semi', 'size': 30, 'align': 'left'},
            {'text': "What you've paid", 'x': 212, 'y': 1149, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': f"Direct Debit {start_str}", 'x': 212, 'y': 1098, 'font': 'open', 'size': 37, 'align': 'left'},
            {'text': f"Direct Debit {end_str}", 'x': 212, 'y': 1048, 'font': 'open', 'size': 37, 'align': 'left'},
            {'text': balance, 'x': 1192, 'y': 1263, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
            {'text': f"£{value1}", 'x': 1192, 'y': 1206, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
            {'text': value_3, 'x': 1192, 'y': 1151, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
            {'text': "-£10.00", 'x': 1192, 'y': 1098, 'font': 'utsaah', 'size': 55, 'align': 'right'},
            {'text': "-£10.00", 'x': 1192, 'y': 1048, 'font': 'utsaah', 'size': 55, 'align': 'right'},
            {'text': value_4, 'x': 1192, 'y': 957, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
        ]
        
        return text_data
    
    def generate_text_data_ie(user_input: str) -> list:
        lines = user_input.strip().split('\n')
        
        name = lines[0].strip()
        address_line1 = lines[1].strip()
        address_line2 = lines[2].strip()
        address_line3 = lines[3].strip()
        address_line4 = lines[4].strip() 
        date_under_address = lines[5].strip() 
        gas = lines[6].strip()
        supply_address = lines[7].strip()
        blue_kw = lines[8].strip()
        lblue_kw = lines[9].strip()
        aqua_kw = lines[10].strip()
        acc_num = lines[11].strip()
        end_date = lines[12].strip()
        total = lines[13].strip()
        due_on = lines[14].strip()
        gas_1 = lines[15].strip()
        gas_2 = lines[16].strip()
        value1 = lines[17].strip()
        value2 = lines[18].strip()
        value3 = lines[19].strip()
        value4 = lines[20].strip()
        value5 = lines[21].strip()
        value6 = lines[22].strip()
        
        text_data = [
            {'text': name, 'x': 36, 'y': 690, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line1, 'x': 36, 'y': 680, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line2, 'x': 36, 'y': 670, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line3, 'x': 36, 'y': 660, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line4, 'x': 36, 'y': 650, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': date_under_address, 'x': 36, 'y': 630, 'font': 'arialb', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': gas, 'x': 36, 'y': 577, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': gas, 'x': 36, 'y': 408, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': supply_address, 'x': 102, 'y': 547.5, 'font': 'arialb', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': blue_kw, 'x': 269, 'y': 510, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': lblue_kw, 'x': 269, 'y': 487, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': aqua_kw, 'x': 269, 'y': 464, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': acc_num, 'x': 463, 'y': 705.5, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': end_date, 'x': 454.5, 'y': 682, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 376, 'y': 572, 'font': 'verdana', 'size': 13.5, 'align': 'left', 'color': '#ffffff'},
            {'text': total, 'x': 384.5, 'y': 571.5, 'font': 'arialb', 'size': 18, 'align': 'left', 'color': '#ffffff'},
            {'text': due_on, 'x': 370, 'y': 542, 'font': 'arialb', 'size': 11.1, 'align': 'left', 'color': '#ffffff'},
            {'text': gas_1, 'x': 128, 'y': 303, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': gas_2, 'x': 50, 'y': 293.4, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': value1, 'x': 267.8, 'y': 346, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value2, 'x': 267.8, 'y': 329, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value3, 'x': 267.8, 'y': 315.5, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value4, 'x': 267.8, 'y': 299, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value4, 'x': 267.8, 'y': 280.3, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value5, 'x': 267.8, 'y': 264.8, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': total, 'x': 267.8, 'y': 251, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value6, 'x': 267.8, 'y': 236, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value6, 'x': 267.8, 'y': 220, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': total, 'x': 267.8, 'y': 202.5, 'font': 'arialb', 'size': 9, 'align': 'right', 'color': '#1b2950'},
            {'text': '€', 'x': 243.5, 'y': 346, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 243.5, 'y': 329, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 315.5, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 299, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 280.3, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 264.8, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 243.5, 'y': 251, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 239.5, 'y': 236, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 239.5, 'y': 220, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 241, 'y': 202.8, 'font': 'verdana', 'size': 6.9, 'align': 'left', 'color': '#1b2950'},
            {'text': '-', 'x': 246.7, 'y': 299, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': '-', 'x': 246.7, 'y': 280.3, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': '-', 'x': 238.7, 'y': 220, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
        ]
        
        return text_data