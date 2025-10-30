# workload_distribution.py
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from sql_requests import (
    INSERT_WORKLOAD_SQL,
    FETCH_WORKLOAD_SQL,
    DELETE_WORKLOAD_SQL,
    EDIT_WORKLOAD_SQL,
    FETCH_TEACHERS_FOR_WORKLOAD_SQL,
    FETCH_SUBJECTS_FOR_WORKLOAD_SQL,
)

class WorkloadDistribution:
    def __init__(self, parent_frame, db_connection, app=None):
        self.parent_frame = parent_frame
        self.db_connection = db_connection
        self.app = app
        self.create_workload_form()
    
    def create_workload_form(self):
        self.refresh_data()
        
        labels = ['ID', 'Преподаватель', 'Предмет', 'Группа']
        
        # Выбор преподавателя
        ttk.Label(self.parent_frame, text='Преподаватель').grid(row=0, column=0, padx=(10, 5), pady=5, sticky='e')
        self.teacher_combobox = ttk.Combobox(self.parent_frame, state="readonly")
        self.teacher_combobox.grid(row=0, column=1, padx=(5, 10), pady=5, sticky='w')
        
        # Выбор предмета
        ttk.Label(self.parent_frame, text='Предмет').grid(row=1, column=0, padx=(10, 5), pady=5, sticky='e')
        self.subject_combobox = ttk.Combobox(self.parent_frame, state="readonly")
        self.subject_combobox.grid(row=1, column=1, padx=(5, 10), pady=5, sticky='w')
        
        # Ввод группы
        ttk.Label(self.parent_frame, text='Группа').grid(row=2, column=0, padx=(10, 5), pady=5, sticky='e')
        self.group_entry = ttk.Entry(self.parent_frame)
        self.group_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky='w')
        
        self.workload_table = ttk.Treeview(self.parent_frame, columns=labels, show='headings')
        for label in labels:
            self.workload_table.heading(label, text=label)
        self.workload_table.column("#0", width=0, stretch=tk.NO)
        for col in labels:
            self.workload_table.column(col, anchor=tk.CENTER, width=200)
        
        self.workload_table.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        # Добавляем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.workload_table.yview)
        self.workload_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=3, sticky='ns')
        
        # Создаем фрейм для кнопок
        buttons_frame = ttk.Frame(self.parent_frame)
        buttons_frame.grid(row=4, column=0, columnspan=4, pady=(5, 10), sticky='ew')
        
        # Центрируем кнопки в фрейме
        buttons_frame.columnconfigure(0, weight=1)
        save_button = ttk.Button(buttons_frame, text="Сохранить", command=self.save_workload)
        save_button.grid(row=0, column=1, padx=5, pady=5)
        
        edit_button = ttk.Button(buttons_frame, text="Изменить запись", command=self.edit_record)
        edit_button.grid(row=0, column=2, padx=5, pady=5)
        
        delete_button = ttk.Button(buttons_frame, text="Удалить запись", command=self.delete_record)
        delete_button.grid(row=0, column=3, padx=5, pady=5)
        
        refresh_button = ttk.Button(buttons_frame, text="Обновить", command=self.refresh_data)
        refresh_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Добавляем событие двойного щелчка
        self.workload_table.bind("<Double-1>", self.fill_entries)
        
        self.show_workload()
    
    def refresh_data(self):
        """Обновление данных преподавателей и предметов"""
        self.teachers = self.fetch_teachers()
        self.subjects = self.fetch_subjects()
        
        if hasattr(self, 'teacher_combobox'):
            self.teacher_combobox['values'] = [f"{teacher[1]} {teacher[2]} {teacher[3]}" for teacher in self.teachers]
        
        if hasattr(self, 'subject_combobox'):
            self.subject_combobox['values'] = [f"{subject[1]}" for subject in self.subjects]
    
    def fill_entries(self, event):
        if not self.workload_table.selection():
            return
        selected_item = self.workload_table.selection()[0]
        values = self.workload_table.item(selected_item, 'values')
        self.teacher_combobox.set(values[1])
        self.subject_combobox.set(values[2])
        self.group_entry.delete(0, tk.END)
        self.group_entry.insert(0, values[3])
    
    def save_workload(self):
        data = [
            self.teacher_combobox.get(),
            self.subject_combobox.get(),
            self.group_entry.get()
        ]
        
        if not data[0] or not data[1] or not data[2]:
            messagebox.showwarning("Предупреждение", "Преподаватель, предмет и группа являются обязательными полями!")
            return
        
        try:
            self.insert_workload(data)
            self.show_workload()
            self.clear_entries()
            messagebox.showinfo("Успех", "Нагрузка успешно добавлена!")
            
            # Обновляем данные в фильтрах
            if self.app and hasattr(self.app, 'data_filter'):
                self.app.data_filter.refresh_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить нагрузку: {e}")
    
    def insert_workload(self, data):
        teacher_name = data[0]
        subject_name = data[1]
        
        # Находим ID преподавателя и предмета по их данным
        teacher_id = next(teacher[0] for teacher in self.teachers if f"{teacher[1]} {teacher[2]} {teacher[3]}" == teacher_name)
        subject_id = next(subject[0] for subject in self.subjects if f"{subject[1]}" == subject_name)
        
        cur = self.db_connection.cursor()
        cur.execute(INSERT_WORKLOAD_SQL, (teacher_id, subject_id, data[2]))
        self.db_connection.commit()
        cur.close()
    
    def show_workload(self):
        workload = self.fetch_workload()
        for row in self.workload_table.get_children():
            self.workload_table.delete(row)
        for item in workload:
            teacher_name = next(f"{teacher[1]} {teacher[2]} {teacher[3]}" for teacher in self.teachers if teacher[0] == item[1])
            subject_name = next(f"{subject[1]}" for subject in self.subjects if subject[0] == item[2])
            self.workload_table.insert('', 'end', values=(item[0], teacher_name, subject_name, item[3]))
    
    def fetch_workload(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_WORKLOAD_SQL)
        workload = cur.fetchall()
        cur.close()
        return workload
    
    def fetch_teachers(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_TEACHERS_FOR_WORKLOAD_SQL)
        teachers = cur.fetchall()
        cur.close()
        return teachers
    
    def fetch_subjects(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_SUBJECTS_FOR_WORKLOAD_SQL)
        subjects = cur.fetchall()
        cur.close()
        return subjects
    
    def delete_record(self):
        if not self.workload_table.selection():
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        
        selected_item = self.workload_table.selection()[0]
        workload_id = self.workload_table.item(selected_item, 'values')[0]
        
        try:
            cur = self.db_connection.cursor()
            cur.execute(DELETE_WORKLOAD_SQL, (workload_id,))
            self.db_connection.commit()
            cur.close()
            
            self.workload_table.delete(selected_item)
            self.clear_entries()
            messagebox.showinfo("Успех", "Нагрузка успешно удалена!")
            
            # Обновляем данные в фильтрах
            if self.app and hasattr(self.app, 'data_filter'):
                self.app.data_filter.refresh_data()
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Ошибка", f"Не удалось удалить нагрузку: {e}")
    
    def edit_record(self):
        if not self.workload_table.selection():
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования!")
            return
        
        selected_item = self.workload_table.selection()[0]
        workload_id = self.workload_table.item(selected_item, 'values')[0]
        data = [
            self.teacher_combobox.get(),
            self.subject_combobox.get(),
            self.group_entry.get()
        ]
        
        if not data[0] or not data[1] or not data[2]:
            messagebox.showwarning("Предупреждение", "Преподаватель, предмет и группа являются обязательными полями!")
            return
        
        try:
            teacher_name = data[0]
            subject_name = data[1]
            
            # Находим ID преподавателя и предмета по их данным
            teacher_id = next(teacher[0] for teacher in self.teachers if f"{teacher[1]} {teacher[2]} {teacher[3]}" == teacher_name)
            subject_id = next(subject[0] for subject in self.subjects if f"{subject[1]}" == subject_name)
            
            cur = self.db_connection.cursor()
            cur.execute(EDIT_WORKLOAD_SQL, (teacher_id, subject_id, data[2], workload_id))
            self.db_connection.commit()
            cur.close()
            self.show_workload()
            self.clear_entries()
            messagebox.showinfo("Успех", "Данные нагрузки успешно обновлены!")
            
            # Обновляем данные в фильтрах
            if self.app and hasattr(self.app, 'data_filter'):
                self.app.data_filter.refresh_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")
    
    def clear_entries(self):
        self.teacher_combobox.set('')
        self.subject_combobox.set('')
        self.group_entry.delete(0, tk.END)