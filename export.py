from docx import Document
import pandas as pd

def export_to_word(self):
    # Получаем данные из таблицы
    rows = [(self.results_table.item(item)["values"]) for item in self.results_table.get_children()]
    
    # Создаем документ Word
    doc = Document()
    doc.add_heading('Отчет по распределению учебной нагрузки', 0)
    
    # Добавляем таблицу
    table = doc.add_table(rows=1, cols=len(self.results_table["columns"]))
    hdr_cells = table.rows[0].cells
    for i, column in enumerate(self.results_table["columns"]):
        hdr_cells[i].text = column
    
    for row in rows:
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)
    
    # Сохраняем документ
    teacher_option = self.teacher_combobox.get()
    subject_option = self.subject_combobox.get()
    filename = f"Отчет_нагрузка_{teacher_option}_{subject_option}.docx"
    doc.save(filename)
    print(f"Отчет сохранен в {filename}")

def export_to_excel(self):
    # Получаем данные из таблицы
    rows = [(self.results_table.item(item)["values"]) for item in self.results_table.get_children()]
    columns = self.results_table["columns"]
    
    # Создаем DataFrame и сохраняем в Excel
    df = pd.DataFrame(rows, columns=columns)
    teacher_option = self.teacher_combobox.get()
    subject_option = self.subject_combobox.get()
    filename = f"Отчет_нагрузка_{teacher_option}_{subject_option}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Отчет сохранен в {filename}")