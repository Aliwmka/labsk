# subjects.py
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from sql_requests import (
    INSERT_SUBJECT_SQL,
    FETCH_SUBJECTS_SQL,
    DELETE_SUBJECT_SQL,
    EDIT_SUBJECT_SQL,
)

class Subjects:
    def __init__(self, parent_frame, db_connection, app=None):
        self.parent_frame = parent_frame
        self.db_connection = db_connection
        self.app = app
        self.create_subjects_form()
    
    def create_subjects_form(self):
        labels = ['ID', 'Название предмета', 'Количество часов']
        self.subject_entries = []
        for i, label in enumerate(labels[1:]):  # Пропускаем 'ID' для ввода данных
            ttk.Label(self.parent_frame, text=label).grid(row=i, column=0, padx=(10, 5), pady=5, sticky='e')
            entry = ttk.Entry(self.parent_frame)
            entry.grid(row=i, column=1, padx=(5, 10), pady=5, sticky='w')
            self.subject_entries.append(entry)
        
        self.subjects_table = ttk.Treeview(self.parent_frame, columns=labels, show='headings')
        for label in labels:
            self.subjects_table.heading(label, text=label)
        self.subjects_table.column("#0", width=0, stretch=tk.NO)
        for col in labels:
            self.subjects_table.column(col, anchor=tk.CENTER, width=200)
        
        self.subjects_table.grid(row=len(labels), column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        # Добавляем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.subjects_table.yview)
        self.subjects_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=len(labels), column=3, sticky='ns')
        
        # Создаем фрейм для кнопок
        buttons_frame = ttk.Frame(self.parent_frame)
        buttons_frame.grid(row=len(labels) + 1, column=0, columnspan=4, pady=(5, 10), sticky='ew')
        
        # Центрируем кнопки в фрейме
        buttons_frame.columnconfigure(0, weight=1)
        save_button = ttk.Button(buttons_frame, text="Сохранить", command=self.save_subject)
        save_button.grid(row=0, column=1, padx=5, pady=5)
        
        edit_button = ttk.Button(buttons_frame, text="Изменить запись", command=self.edit_record)
        edit_button.grid(row=0, column=2, padx=5, pady=5)
        
        delete_button = ttk.Button(buttons_frame, text="Удалить запись", command=self.delete_record)
        delete_button.grid(row=0, column=3, padx=5, pady=5)
        
        refresh_button = ttk.Button(buttons_frame, text="Обновить", command=self.show_subjects)
        refresh_button.grid(row=0, column=4, padx=5, pady=5)
        
        import_button = ttk.Button(buttons_frame, text="Импорт из Excel", command=self.handle_import_excel)
        import_button.grid(row=0, column=5, padx=5, pady=5)
        
        # Добавляем событие двойного щелчка
        self.subjects_table.bind("<Double-1>", self.fill_entries)
        
        self.show_subjects()
    
    def fill_entries(self, event):
        if not self.subjects_table.selection():
            return
        selected_item = self.subjects_table.selection()[0]
        values = self.subjects_table.item(selected_item, 'values')
        for entry, value in zip(self.subject_entries, values[1:]):  # Пропускаем 'ID'
            entry.delete(0, tk.END)
            entry.insert(0, value)
    
    def save_subject(self):
        data = [entry.get() for entry in self.subject_entries]
        
        # Проверка обязательных полей
        if not data[0]:  # Название предмета обязательно
            messagebox.showwarning("Предупреждение", "Название предмета является обязательным полем!")
            return
        
        try:
            # Проверяем числовые поля
            hours = int(data[1])
            
            self.insert_subject(data)
            self.show_subjects()
            self.clear_entries()
            messagebox.showinfo("Успех", "Предмет успешно добавлен!")
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
        except ValueError:
            messagebox.showerror("Ошибка", "Количество часов должно быть числом!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить предмет: {e}")
    
    def insert_subject(self, data):
        cur = self.db_connection.cursor()
        cur.execute(INSERT_SUBJECT_SQL, data)
        self.db_connection.commit()
        cur.close()
    
    def show_subjects(self):
        subjects = self.fetch_subjects()
        for row in self.subjects_table.get_children():
            self.subjects_table.delete(row)
        for subject in subjects:
            self.subjects_table.insert('', 'end', values=subject)
    
    def fetch_subjects(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_SUBJECTS_SQL)
        subjects = cur.fetchall()
        cur.close()
        return subjects
    
    def delete_record(self):
        if not self.subjects_table.selection():
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        
        selected_item = self.subjects_table.selection()[0]
        subject_id = self.subjects_table.item(selected_item, 'values')[0]
        subject_name = self.subjects_table.item(selected_item, 'values')[1]
        
        # Подтверждение удаления
        result = messagebox.askyesno(
            "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить предмет '{subject_name}'?\nВсе связанные записи нагрузки также будут удалены."
        )
        
        if not result:
            return
        
        try:
            cur = self.db_connection.cursor()
            cur.execute(DELETE_SUBJECT_SQL, (subject_id,))
            self.db_connection.commit()
            cur.close()
            
            self.subjects_table.delete(selected_item)
            self.clear_entries()
            messagebox.showinfo("Успех", "Предмет и все связанные записи нагрузки успешно удалены!")
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                    self.app.workload.show_workload()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Ошибка", f"Не удалось удалить предмет: {e}")
    
    def edit_record(self):
        if not self.subjects_table.selection():
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования!")
            return
        
        selected_item = self.subjects_table.selection()[0]
        subject_id = self.subjects_table.item(selected_item, 'values')[0]
        data = [entry.get() for entry in self.subject_entries]
        
        # Проверка обязательных полей
        if not data[0]:  # Название предмета обязательно
            messagebox.showwarning("Предупреждение", "Название предмета является обязательным полем!")
            return
        
        try:
            # Проверяем числовые поля
            hours = int(data[1])
            
            cur = self.db_connection.cursor()
            cur.execute(EDIT_SUBJECT_SQL, (*data, subject_id))
            self.db_connection.commit()
            cur.close()
            self.show_subjects()
            self.clear_entries()
            messagebox.showinfo("Успех", "Данные предмета успешно обновлены!")
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                    self.app.workload.show_workload()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
        except ValueError:
            messagebox.showerror("Ошибка", "Количество часов должно быть числом!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")
    
    def clear_entries(self):
        for entry in self.subject_entries:
            entry.delete(0, tk.END)
    
    def handle_import_excel(self):
        def on_data(headers, rows):
            self.process_imported_subjects(headers, rows)
        
        from import_data import import_subjects_from_excel
        import_subjects_from_excel(self.parent_frame.winfo_toplevel(), on_data)
    
    def process_imported_subjects(self, headers, rows):
        try:
            imported_count = 0
            skipped_count = 0
            
            for row in rows:
                if len(row) < 2:
                    skipped_count += 1
                    continue
                    
                subject_name = str(row[0]).strip() if row[0] else ""
                hours = str(row[1]).strip() if row[1] else ""
                
                # Проверяем обязательные поля
                if not subject_name or not hours:
                    skipped_count += 1
                    continue
                
                try:
                    # Преобразуем числовые поля
                    hours_int = int(hours)
                    
                    cur = self.db_connection.cursor()
                    cur.execute(INSERT_SUBJECT_SQL, (subject_name, hours_int))
                    self.db_connection.commit()
                    cur.close()
                    imported_count += 1
                    
                except (ValueError, Exception) as e:
                    skipped_count += 1
                    continue
            
            self.show_subjects()
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
            
            message = f"Импорт предметов завершен!\nУспешно: {imported_count} записей"
            if skipped_count > 0:
                message += f"\nПропущено: {skipped_count} записей (некорректные данные)"
            messagebox.showinfo("Успех", message)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать предметы: {str(e)}")