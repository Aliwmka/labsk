from docx import Document
from docx.table import Table
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from sql_requests import (
    INSERT_TEACHER_SQL, INSERT_SUBJECT_SQL, INSERT_WORKLOAD_SQL,
    EDIT_TEACHER_SQL, EDIT_SUBJECT_SQL, EDIT_WORKLOAD_SQL
)

def export_to_word(instance):
    """Экспорт данных в Word"""
    # Получаем данные из таблицы
    rows = [(instance.results_table.item(item)["values"]) for item in instance.results_table.get_children()]
    
    # Проверяем, есть ли данные для экспорта
    if not rows:
        messagebox.showwarning("Предупреждение", "Нет данных для экспорта")
        return
    
    # Создаем документ Word
    doc = Document()
    doc.add_heading('Отчет по распределению учебной нагрузки', 0)
    
    # Добавляем таблицу
    table = doc.add_table(rows=1, cols=len(instance.results_table["columns"]))
    hdr_cells = table.rows[0].cells
    for i, column in enumerate(instance.results_table["columns"]):
        hdr_cells[i].text = column
    
    for row in rows:
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)
    
    # Сохраняем документ
    teacher_option = instance.teacher_combobox.get() or "Все"
    subject_option = instance.subject_combobox.get() or "Все"
    filename = f"Отчет_нагрузка_{teacher_option}_{subject_option}.docx".replace(" ", "_")
    doc.save(filename)
    messagebox.showinfo("Успех", f"Отчет сохранен в {filename}")

def export_to_excel(instance):
    """Экспорт данных в Excel"""
    # Получаем данные из таблицы
    rows = [(instance.results_table.item(item)["values"]) for item in instance.results_table.get_children()]
    columns = instance.results_table["columns"]
    
    # Проверяем, есть ли данные для экспорта
    if not rows:
        messagebox.showwarning("Предупреждение", "Нет данных для экспорта")
        return
    
    # Создаем DataFrame и сохраняем в Excel
    df = pd.DataFrame(rows, columns=columns)
    teacher_option = instance.teacher_combobox.get() or "Все"
    subject_option = instance.subject_combobox.get() or "Все"
    filename = f"Отчет_нагрузка_{teacher_option}_{subject_option}.xlsx".replace(" ", "_")
    df.to_excel(filename, index=False)
    messagebox.showinfo("Успех", f"Отчет сохранен в {filename}")

def import_from_word(instance):
    """Импорт данных из Word файла"""
    file_path = filedialog.askopenfilename(
        title="Выберите Word файл для импорта",
        filetypes=[("Word files", "*.docx")]
    )
    
    if not file_path:
        return
    
    try:
        doc = Document(file_path)
        data = []
        
        # Ищем таблицу в документе
        for table in doc.tables:
            # Пропускаем заголовок таблицы
            for i, row in enumerate(table.rows):
                if i == 0:  # Пропускаем заголовок
                    continue
                
                row_data = [cell.text for cell in row.cells]
                if len(row_data) >= 4:  # ID, Преподаватель, Предмет, Группа
                    data.append(row_data)
        
        if not data:
            messagebox.showwarning("Предупреждение", "В файле Word не найдено данных для импорта")
            return
        
        # Очищаем текущую таблицу
        for row in instance.results_table.get_children():
            instance.results_table.delete(row)
        
        # Добавляем данные в таблицу
        for row_data in data:
            instance.results_table.insert('', 'end', values=row_data)
        
        messagebox.showinfo("Успех", f"Успешно импортировано {len(data)} записей из Word файла")
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при импорте из Word: {str(e)}")

def import_from_excel(instance):
    """Импорт данных из Excel файла"""
    file_path = filedialog.askopenfilename(
        title="Выберите Excel файл для импорта",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    
    if not file_path:
        return
    
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path)
        
        # Проверяем наличие необходимых колонок
        required_columns = ['ID', 'Преподаватель', 'Предмет', 'Группа']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            messagebox.showerror("Ошибка", f"В файле отсутствуют колонки: {', '.join(missing_columns)}")
            return
        
        # Очищаем текущую таблицу
        for row in instance.results_table.get_children():
            instance.results_table.delete(row)
        
        # Добавляем данные в таблицу
        for _, row in df.iterrows():
            row_data = [
                int(row['ID']) if pd.notna(row['ID']) else 0,
                str(row['Преподаватель']),
                str(row['Предмет']),
                str(row['Группа'])
            ]
            instance.results_table.insert('', 'end', values=row_data)
        
        messagebox.showinfo("Успех", f"Успешно импортировано {len(df)} записей из Excel файла")
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при импорте из Excel: {str(e)}")

def import_data_to_database(instance):
    """Импорт данных из текущей таблицы в базу данных"""
    try:
        # Получаем данные из таблицы
        rows = [(instance.results_table.item(item)["values"]) for item in instance.results_table.get_children()]
        
        if not rows:
            messagebox.showwarning("Предупреждение", "Нет данных для импорта в базу данных")
            return
        
        imported_count = 0
        updated_count = 0
        
        for row in rows:
            workload_id = int(row[0]) if row[0] else 0
            teacher_name = str(row[1])
            subject_name = str(row[2])
            group_number = str(row[3])
            
            # Получаем ID преподавателя
            cur = instance.db_connection.cursor()
            cur.execute(
                "SELECT teacher_id FROM teachers WHERE CONCAT(last_name, ' ', first_name, ' ', middle_name) = %s",
                (teacher_name,)
            )
            teacher_result = cur.fetchone()
            
            if not teacher_result:
                messagebox.showwarning("Предупреждение", f"Преподаватель не найден: {teacher_name}")
                continue
            
            teacher_id = teacher_result[0]
            
            # Получаем ID предмета
            cur.execute(
                "SELECT subject_id FROM subjects WHERE subject_name = %s",
                (subject_name,)
            )
            subject_result = cur.fetchone()
            
            if not subject_result:
                messagebox.showwarning("Предупреждение", f"Предмет не найден: {subject_name}")
                continue
            
            subject_id = subject_result[0]
            
            if workload_id > 0:
                # Обновляем существующую запись
                cur.execute(EDIT_WORKLOAD_SQL, (teacher_id, subject_id, group_number, workload_id))
                updated_count += 1
            else:
                # Добавляем новую запись
                cur.execute(INSERT_WORKLOAD_SQL, (teacher_id, subject_id, group_number))
                imported_count += 1
            
            instance.db_connection.commit()
            cur.close()
        
        messagebox.showinfo("Успех", 
                           f"Импорт в базу данных завершен:\n"
                           f"Добавлено: {imported_count} записей\n"
                           f"Обновлено: {updated_count} записей")
        
        # Обновляем данные в основном интерфейсе
        if hasattr(instance, 'show_workload'):
            instance.show_workload()
            
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при импорте в базу данных: {str(e)}")