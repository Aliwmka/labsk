from tkinter import ttk
import tkinter as tk
from sql_requests import (
    INSERT_TEACHER_SQL,
    FETCH_TEACHERS_SQL,
    DELETE_TEACHER_SQL,
    EDIT_TEACHER_SQL,
)

class Teachers:
    def __init__(self, parent_frame, db_connection):
        self.parent_frame = parent_frame
        self.create_teachers_form()
        self.db_connection = db_connection
    
    def create_teachers_form(self):
        labels = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Ученая степень', 'Должность', 'Стаж']
        self.teacher_entries = []
        for i, label in enumerate(labels[1:]):  # Пропускаем 'ID' для ввода данных
            ttk.Label(self.parent_frame, text=label).grid(row=i, column=0, padx=(10, 5), pady=5, sticky='e')
            entry = ttk.Entry(self.parent_frame)
            entry.grid(row=i, column=1, padx=(5, 10), pady=5, sticky='w')
            self.teacher_entries.append(entry)
        
        self.teachers_table = ttk.Treeview(self.parent_frame, columns=labels, show='headings')
        for label in labels:
            self.teachers_table.heading(label, text=label)
        self.teachers_table.column("#0", width=0, stretch=tk.NO)
        for col in labels:
            self.teachers_table.column(col, anchor=tk.CENTER, width=150)
        
        self.teachers_table.grid(row=len(labels), column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        # Добавляем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.teachers_table.yview)
        self.teachers_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=len(labels), column=3, sticky='ns')
        
        # Создаем фрейм для кнопок
        buttons_frame = ttk.Frame(self.parent_frame)
        buttons_frame.grid(row=len(labels) + 1, column=0, columnspan=4, pady=(5, 10), sticky='ew')
        
        # Центрируем кнопки в фрейме
        buttons_frame.columnconfigure(0, weight=1)
        save_button = ttk.Button(buttons_frame, text="Сохранить", command=self.save_teacher)
        save_button.grid(row=0, column=1, padx=5, pady=5)
        
        edit_button = ttk.Button(buttons_frame, text="Изменить запись", command=self.edit_record)
        edit_button.grid(row=0, column=2, padx=5, pady=5)
        
        delete_button = ttk.Button(buttons_frame, text="Удалить запись", command=self.delete_record)
        delete_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Добавляем событие двойного щелчка
        self.teachers_table.bind("<Double-1>", self.fill_entries)
    
    def fill_entries(self, event):
        selected_item = self.teachers_table.selection()[0]
        values = self.teachers_table.item(selected_item, 'values')
        for entry, value in zip(self.teacher_entries, values[1:]):  # Пропускаем 'ID'
            entry.delete(0, tk.END)
            entry.insert(0, value)
    
    def save_teacher(self):
        data = [entry.get() for entry in self.teacher_entries]
        self.insert_teacher(data)
        self.show_teachers()
        self.clear_entries()
    
    def insert_teacher(self, data):
        cur = self.db_connection.cursor()
        cur.execute(INSERT_TEACHER_SQL, data)
        self.db_connection.commit()
        cur.close()
    
    def show_teachers(self):
        teachers = self.fetch_teachers()
        for row in self.teachers_table.get_children():
            self.teachers_table.delete(row)
        for teacher in teachers:
            self.teachers_table.insert('', 'end', values=teacher)
    
    def fetch_teachers(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_TEACHERS_SQL)
        teachers = cur.fetchall()
        cur.close()
        return teachers
    
    def delete_record(self):
        selected_item = self.teachers_table.selection()[0]
        teacher_id = self.teachers_table.item(selected_item, 'values')[0]
        cur = self.db_connection.cursor()
        cur.execute(DELETE_TEACHER_SQL, (teacher_id,))
        self.db_connection.commit()
        cur.close()
        self.teachers_table.delete(selected_item)
    
    def edit_record(self):
        selected_item = self.teachers_table.selection()[0]
        teacher_id = self.teachers_table.item(selected_item, 'values')[0]
        data = [entry.get() for entry in self.teacher_entries]
        cur = self.db_connection.cursor()
        cur.execute(EDIT_TEACHER_SQL, (*data, teacher_id))
        self.db_connection.commit()
        cur.close()
        self.show_teachers()
        self.clear_entries()
    
    def clear_entries(self):
        for entry in self.teacher_entries:
            entry.delete(0, tk.END)