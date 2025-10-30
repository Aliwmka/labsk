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
    def __init__(self, parent_frame, db_connection):
        self.parent_frame = parent_frame
        self.create_subjects_form()
        self.db_connection = db_connection
    
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
        
        # Добавляем событие двойного щелчка
        self.subjects_table.bind("<Double-1>", self.fill_entries)
    
    def fill_entries(self, event):
        selected_item = self.subjects_table.selection()[0]
        values = self.subjects_table.item(selected_item, 'values')
        for entry, value in zip(self.subject_entries, values[1:]):  # Пропускаем 'ID'
            entry.delete(0, tk.END)
            entry.insert(0, value)
    
    def save_subject(self):
        try:
            data = self.validate_subject_data()
            if data is None:
                return
            
            self.insert_subject(data)
            self.show_subjects()
            self.clear_entries()
            messagebox.showinfo("Успех", "Предмет успешно сохранен!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении предмета: {str(e)}")
            self.db_connection.rollback()
    
    def validate_subject_data(self):
        """Проверка и преобразование данных предмета"""
        raw_data = [entry.get().strip() for entry in self.subject_entries]
        
        # Проверяем обязательные поля
        if not raw_data[0]:  # Название предмета
            messagebox.showwarning("Предупреждение", "Поле 'Название предмета' обязательно для заполнения")
            return None
        
        # Преобразуем часы в число
        try:
            hours = int(raw_data[1]) if raw_data[1] else 0
        except ValueError:
            messagebox.showwarning("Предупреждение", "Поле 'Количество часов' должно быть числом")
            return None
        
        # Возвращаем проверенные данные
        return [
            raw_data[0],  # Название предмета
            hours         # Количество часов
        ]
    
    def insert_subject(self, data):
        cur = self.db_connection.cursor()
        try:
            cur.execute(INSERT_SUBJECT_SQL, data)
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
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
        try:
            selected_items = self.subjects_table.selection()
            if not selected_items:
                messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
                return
            
            selected_item = selected_items[0]
            subject_id = self.subjects_table.item(selected_item, 'values')[0]
            
            # Подтверждение удаления
            result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?")
            if not result:
                return
            
            cur = self.db_connection.cursor()
            cur.execute(DELETE_SUBJECT_SQL, (subject_id,))
            self.db_connection.commit()
            cur.close()
            
            self.subjects_table.delete(selected_item)
            messagebox.showinfo("Успех", "Запись успешно удалена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении записи: {str(e)}")
            self.db_connection.rollback()
    
    def edit_record(self):
        try:
            selected_items = self.subjects_table.selection()
            if not selected_items:
                messagebox.showwarning("Предупреждение", "Выберите запись для редактирования")
                return
            
            selected_item = selected_items[0]
            subject_id = self.subjects_table.item(selected_item, 'values')[0]
            
            data = self.validate_subject_data()
            if data is None:
                return
            
            cur = self.db_connection.cursor()
            cur.execute(EDIT_SUBJECT_SQL, (*data, subject_id))
            self.db_connection.commit()
            cur.close()
            
            self.show_subjects()
            self.clear_entries()
            messagebox.showinfo("Успех", "Запись успешно обновлена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при редактировании записи: {str(e)}")
            self.db_connection.rollback()
    
    def clear_entries(self):
        for entry in self.subject_entries:
            entry.delete(0, tk.END)