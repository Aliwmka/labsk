# import_data.py
from docx import Document
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def import_from_excel(parent_window, callback):
    filepath = filedialog.askopenfilename(
        parent=parent_window,
        title="Выберите файл Excel",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not filepath:
        return

    try:
        # Читаем Excel файл
        df = pd.read_excel(filepath, dtype=str, header=0)
        
        # Заменяем NaN на пустые строки
        df = df.fillna('')
        
        # Убираем пробелы в начале и конце всех строковых значений
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Преобразуем в список
        data = df.values.tolist()
        headers = df.columns.tolist()
        
        # Проверяем структуру данных
        if len(data) == 0:
            messagebox.showwarning("Предупреждение", "Файл не содержит данных!")
            return
            
        print(f"Загружено {len(data)} записей из Excel")
        print(f"Заголовки: {headers}")
        print(f"Первая запись: {data[0] if data else 'нет данных'}")
        
        callback(headers, data)
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать Excel файл: {str(e)}")
        print(f"Ошибка при чтении Excel: {e}")

def import_from_word(parent_window, callback):
    filepath = filedialog.askopenfilename(
        parent=parent_window,
        title="Выберите файл Word",
        filetypes=[("Word files", "*.docx")]
    )
    if not filepath:
        return

    try:
        doc = Document(filepath)
        if not doc.tables:
            messagebox.showwarning("Внимание", "В документе нет таблиц.")
            return

        table = doc.tables[0]
        data = []
        headers = []
        
        # Читаем заголовки из первой строки
        for i, row in enumerate(table.rows):
            row_data = []
            for cell in row.cells:
                text = cell.text.strip()
                row_data.append(text)
            
            if i == 0:
                headers = row_data
                if len(headers) == 0:
                    messagebox.showwarning("Предупреждение", "Таблица не содержит заголовков!")
                    return
            else:
                # Пропускаем полностью пустые строки
                if any(cell for cell in row_data):
                    # Если в данных строке меньше столбцов чем в заголовках, дополняем пустыми значениями
                    while len(row_data) < len(headers):
                        row_data.append('')
                    data.append(row_data)
        
        if not data:
            messagebox.showwarning("Внимание", "В таблице нет данных (кроме заголовков).")
            return
            
        print(f"Загружено {len(data)} записей из Word")
        print(f"Заголовки: {headers}")
        print(f"Первая запись: {data[0] if data else 'нет данных'}")
            
        callback(headers, data)
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать Word документ: {str(e)}")
        print(f"Ошибка при чтении Word: {e}")

def import_teachers_from_excel(parent_window, callback):
    """Импорт преподавателей из Excel"""
    filepath = filedialog.askopenfilename(
        parent=parent_window,
        title="Выберите файл Excel с преподавателями",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not filepath:
        return

    try:
        df = pd.read_excel(filepath, dtype=str, header=0)
        df = df.fillna('')
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        data = df.values.tolist()
        headers = df.columns.tolist()
        
        if len(data) == 0:
            messagebox.showwarning("Предупреждение", "Файл не содержит данных!")
            return
            
        print(f"Загружено {len(data)} преподавателей из Excel")
        callback(headers, data)
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать Excel файл: {str(e)}")

def import_subjects_from_excel(parent_window, callback):
    """Импорт предметов из Excel"""
    filepath = filedialog.askopenfilename(
        parent=parent_window,
        title="Выберите файл Excel с предметами",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not filepath:
        return

    try:
        df = pd.read_excel(filepath, dtype=str, header=0)
        df = df.fillna('')
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        data = df.values.tolist()
        headers = df.columns.tolist()
        
        if len(data) == 0:
            messagebox.showwarning("Предупреждение", "Файл не содержит данных!")
            return
            
        print(f"Загружено {len(data)} предметов из Excel")
        callback(headers, data)
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать Excel файл: {str(e)}")