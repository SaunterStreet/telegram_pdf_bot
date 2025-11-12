from pdf import *

user_message = """DANA YEHUDAI-OFIR
36 Levi Eshkol
Jerusalem
9422904
1964 582071
042 91837456
12 NOV 25
12 NOV 25
9925841
5736198
2947605
423.40
236.00
171.85
138.75
10.20
2.35
109.00
07-9723846
09763 000010992584 0837415 942168"""

text_data = text_generator.generate_text_data_ir(user_message)
print("Начинаю обработку PDF")
editor = PDFEditor("template_ir.pdf")
output_path = f"result_123.pdf"
editor.add_text(output_path, text_data)
print("PDF создан")