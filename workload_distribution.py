from tkinter import ttk
import tkinter as tk
from sql_requests import (
    INSERT_WORKLOAD_SQL,
    FETCH_WORKLOAD_SQL,
    FETCH_TEACHERS_FOR_WORKLOAD_SQL,
    FETCH_SUBJECTS_FOR_WORKLOAD_SQL,
    DELETE_WORKLOAD_SQL,
    EDIT_WORKLOAD_SQL,
)

class WorkloadDistribution:
    def __init__(self, parent_frame, db_connection):
        self.parent_frame = parent_frame
        self.db_connection = db_connection
        self.create_workload_form()
    
    def create_workload_form(self):
        self.teachers = self.fetch_teachers()
        self.subjects = self.fetch_subjects()
        
        labels = ['ID', 'Преподаватель', 'Предмет', 'Группа']
        self.workload_entries = []
        
        # Поле со списком для преподавателей
        ttk.Label(self.parent_frame, text='Преподаватель').grid(row=0, column=0, padx=(10, 5), pady=5, sticky='e')
        self.teacher_combobox = ttk.Combobox(self.parent_frame, 
                                           values=[f"{teacher[1]} {teacher[2]} {teacher[3]}" for teacher in self.teachers],
                                           state="readonly")
        self.teacher_combobox.grid(row=0, column=1, padx=(5, 10), pady=5, sticky='w')
        self.workload_entries.append(self.teacher_combobox)
        
        # Поле со списком для предметов
        ttk.Label(self.parent_frame, text='Предмет').grid(row=1, column=0, padx=(10, 5), pady=5, sticky='e')
        self.subject_combobox = ttk.Combobox(self.parent_frame,
                                           values=[f"{subject[1]}" for subject in self.subjects],
                                           state="readonly")
        self.subject_combobox.grid(row=1, column=1, padx=(5, 10), pady=5, sticky='w')
        self.workload_entries.append(self.subject_combobox)
        
        # Поле для номера группы
        ttk.Label(self.parent_frame, text='Номер группы').grid(row=2, column=0, padx=(10, 5), pady=5, sticky='e')
        self.group_entry = ttk.Entry(self.parent_frame)
        self.group_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky='w')
        self.workload_entries.append(self.group_entry)
        
        self.workload_table = ttk.Treeview(self.parent_frame, columns=labels, show='headings')
        for label in labels:
            self.workload_table.heading(label, text=label)
        self.workload_table.column("#0", width=0, stretch=tk.NO)
        for col in labels:
            self.workload_table.column(col, anchor=tk.CENTER, width=200)
        
        self.workload_table.grid(row=len(labels), column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        # Добавляем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.workload_table.yview)
        self.workload_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=len(labels), column=3, sticky='ns')
        
        # Создаем фрейм для кнопок
        buttons_frame = ttk.Frame(self.parent_frame)
        buttons_frame.grid(row=len(labels) + 1, column=0, columnspan=4, pady=(5, 10), sticky='ew')
        
        # Центрируем кнопки в фрейме
        buttons_frame.columnconfigure(0, weight=1)
        save_button = ttk.Button(buttons_frame, text="Сохранить", command=self.save_workload)
        save_button.grid(row=0, column=1, padx=5, pady=5)
        
        edit_button = ttk.Button(buttons_frame, text="Изменить запись", command=self.edit_record)
        edit_button.grid(row=0, column=2, padx=5, pady=5)
        
        delete_button = ttk.Button(buttons_frame, text="Удалить запись", command=self.delete_record)
        delete_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.workload_table.bind("<Double-1>", self.fill_entries)
    
    def fill_entries(self, event):
        selected_item = self.workload_table.selection()[0]
        values = self.workload_table.item(selected_item, 'values')
        self.teacher_combobox.set(values[1])  # Заполняем поле преподавателя
        self.subject_combobox.set(values[2])  # Заполняем поле предмета
        self.group_entry.delete(0, tk.END)
        self.group_entry.insert(0, values[3])
    
    def save_workload(self):
        data = [
            self.teacher_combobox.get(),
            self.subject_combobox.get(),
            self.group_entry.get()
        ]
        self.insert_workload(data)
        self.show_workload()
        self.clear_entries()
    
    def insert_workload(self, data):
        teacher_name = data[0]
        subject_name = data[1]
        
        # Находим ID преподавателя и предмета по их именам
        teacher_id = next(teacher[0] for teacher in self.teachers if f"{teacher[1]} {teacher[2]} {teacher[3]}" == teacher_name)
        subject_id = next(subject[0] for subject in self.subjects if subject[1] == subject_name)
        
        cur = self.db_connection.cursor()
        cur.execute(INSERT_WORKLOAD_SQL, (teacher_id, subject_id, data[2]))
        self.db_connection.commit()
        cur.close()
    
    def show_workload(self):
        workload = self.fetch_workload()
        for row in self.workload_table.get_children():
            self.workload_table.delete(row)
        for w in workload:
            teacher_name = next(f"{teacher[1]} {teacher[2]} {teacher[3]}" for teacher in self.teachers if teacher[0] == w[1])
            subject_name = next(subject[1] for subject in self.subjects if subject[0] == w[2])
            self.workload_table.insert('', 'end',
                                      values=(w[0], teacher_name, subject_name, w[3]))
    
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
        selected_item = self.workload_table.selection()[0]
        workload_id = self.workload_table.item(selected_item, 'values')[0]
        cur = self.db_connection.cursor()
        cur.execute(DELETE_WORKLOAD_SQL, (workload_id,))
        self.db_connection.commit()
        cur.close()
        self.workload_table.delete(selected_item)
    
    def edit_record(self):
        selected_item = self.workload_table.selection()[0]
        workload_id = self.workload_table.item(selected_item, 'values')[0]
        data = [
            self.teacher_combobox.get(),
            self.subject_combobox.get(),
            self.group_entry.get()
        ]
        teacher_name = data[0]
        subject_name = data[1]
        
        # Находим ID преподавателя и предмета по их именам
        teacher_id = next(teacher[0] for teacher in self.teachers if f"{teacher[1]} {teacher[2]} {teacher[3]}" == teacher_name)
        subject_id = next(subject[0] for subject in self.subjects if subject[1] == subject_name)
        
        cur = self.db_connection.cursor()
        cur.execute(EDIT_WORKLOAD_SQL, (teacher_id, subject_id, data[2], workload_id))
        self.db_connection.commit()
        cur.close()
        self.show_workload()
        self.clear_entries()
    
    def clear_entries(self):
        for entry in self.workload_entries:
            if isinstance(entry, ttk.Combobox):
                entry.set('')
            else:
                entry.delete(0, tk.END)