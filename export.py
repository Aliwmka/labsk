from docx import Document
import pandas as pd

def export_to_word(instance):
    # Получаем данные из таблицы
    rows = [(instance.results_table.item(item)["values"]) for item in instance.results_table.get_children()]
    
    # Проверяем, есть ли данные для экспорта
    if not rows:
        print("Нет данных для экспорта")
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
    print(f"Отчет сохранен в {filename}")

def export_to_excel(instance):
    # Получаем данные из таблицы
    rows = [(instance.results_table.item(item)["values"]) for item in instance.results_table.get_children()]
    columns = instance.results_table["columns"]
    
    # Проверяем, есть ли данные для экспорта
    if not rows:
        print("Нет данных для экспорта")
        return
    
    # Создаем DataFrame и сохраняем в Excel
    df = pd.DataFrame(rows, columns=columns)
    teacher_option = instance.teacher_combobox.get() or "Все"
    subject_option = instance.subject_combobox.get() or "Все"
    filename = f"Отчет_нагрузка_{teacher_option}_{subject_option}.xlsx".replace(" ", "_")
    df.to_excel(filename, index=False)
    print(f"Отчет сохранен в {filename}")