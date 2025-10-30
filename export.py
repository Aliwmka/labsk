# export.py
from docx import Document
import pandas as pd
import os
from datetime import datetime

def export_to_word(instance):
    try:
        rows = [(instance.results_table.item(item)["values"]) for item in instance.results_table.get_children()]
        
        if not rows:
            from tkinter import messagebox
            messagebox.showwarning("Предупреждение", "Нет данных для экспорта!")
            return
        
        doc = Document()
        doc.add_heading('Отчет по распределению учебной нагрузки', 0)
        
        # Добавляем информацию о фильтрах
        teacher_option = instance.teacher_combobox.get() or "все"
        subject_option = instance.subject_combobox.get() or "все"
        
        filters_info = f"Фильтры: Преподаватель - {teacher_option}, Предмет - {subject_option}"
        doc.add_paragraph(filters_info)
        doc.add_paragraph()  # Пустая строка
        
        # Создаем таблицу
        table = doc.add_table(rows=1, cols=len(instance.results_table["columns"]))
        table.style = 'Table Grid'
        
        # Заголовки
        hdr_cells = table.rows[0].cells
        for i, column in enumerate(instance.results_table["columns"]):
            hdr_cells[i].text = str(column)
        
        # Данные
        for row in rows:
            row_cells = table.add_row().cells
            for i, value in enumerate(row):
                row_cells[i].text = str(value) if value is not None else ""
        
        # Создаем папку для отчетов, если ее нет
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/Отчет_нагрузка_{timestamp}.docx"
        
        doc.save(filename)
        
        from tkinter import messagebox
        messagebox.showinfo("Успех", f"Отчет сохранен в {filename}")
        
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Ошибка", f"Не удалось экспортировать в Word: {e}")

def export_to_excel(instance):
    try:
        rows = [(instance.results_table.item(item)["values"]) for item in instance.results_table.get_children()]
        
        if not rows:
            from tkinter import messagebox
            messagebox.showwarning("Предупреждение", "Нет данных для экспорта!")
            return
        
        columns = instance.results_table["columns"]
        
        # Создаем DataFrame
        df = pd.DataFrame(rows, columns=columns)
        
        # Создаем папку для отчетов, если ее нет
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/Отчет_нагрузка_{timestamp}.xlsx"
        
        # Сохраняем в Excel с настройками
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Нагрузка', index=False)
            
            # Настройка ширины колонок
            worksheet = writer.sheets['Нагрузка']
            for idx, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_len, 50)
        
        from tkinter import messagebox
        messagebox.showinfo("Успех", f"Отчет сохранен в {filename}")
        
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Ошибка", f"Не удалось экспортировать в Excel: {e}")