from tkinter import ttk
import tkinter as tk
from export import export_to_word, export_to_excel, import_from_word, import_from_excel, import_data_to_database
from sql_requests import (
    LOAD_TEACHERS_FOR_FILTER_SQL,
    LOAD_SUBJECTS_FOR_FILTER_SQL,
    TEACHER_FILTER_SQL,
    SUBJECT_FILTER_SQL,
    APPLY_FILTERS_SQL,
)

class DataFilter:
    def __init__(self, parent_frame, db_connection):
        self.results_table = None
        self.subject_combobox = None
        self.teacher_combobox = None
        self.parent_frame = parent_frame
        self.db_connection = db_connection
        self.create_filter_form()
    
    def create_filter_form(self):
        # Фильтр по преподавателю
        ttk.Label(self.parent_frame, text='Фильтр по преподавателю').grid(row=0, column=0, padx=(10, 5), pady=5, sticky='e')
        self.teacher_combobox = ttk.Combobox(self.parent_frame, state="readonly")
        self.teacher_combobox.grid(row=0, column=1, padx=(5, 10), pady=5, sticky='w')
        
        # Фильтр по предмету
        ttk.Label(self.parent_frame, text='Фильтр по предмету').grid(row=1, column=0, padx=(10, 5), pady=5, sticky='e')
        self.subject_combobox = ttk.Combobox(self.parent_frame, state="readonly")
        self.subject_combobox.grid(row=1, column=1, padx=(5, 10), pady=5, sticky='w')
        
        # Таблица результатов
        self.results_table = ttk.Treeview(self.parent_frame, columns=(
            'ID', 'Преподаватель', 'Предмет', 'Группа'),
            show='headings')
        for label in self.results_table["columns"]:
            self.results_table.heading(label, text=label)
        
        # Настраиваем ширину колонок
        self.results_table.column('ID', width=50, anchor=tk.CENTER)
        self.results_table.column('Преподаватель', width=200, anchor=tk.W)
        self.results_table.column('Предмет', width=150, anchor=tk.W)
        self.results_table.column('Группа', width=100, anchor=tk.CENTER)
        
        self.results_table.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')
        
        # Создаем фрейм для кнопок под таблицей
        buttons_frame = ttk.Frame(self.parent_frame)
        buttons_frame.grid(row=3, column=0, columnspan=4, pady=(5, 10), sticky='ew')
        
        # Центрируем кнопки в фрейме
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)
        buttons_frame.columnconfigure(3, weight=1)
        
        # Первый ряд кнопок - фильтры
        ttk.Button(buttons_frame, text="Применить фильтр", command=self.apply_filter).grid(
            row=0, column=0, padx=5, pady=5, sticky='ew')
        
        ttk.Button(buttons_frame, text="Очистить фильтры", command=self.clear_filters).grid(
            row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Button(buttons_frame, text="Обновить данные", command=self.refresh_data).grid(
            row=0, column=2, padx=5, pady=5, sticky='ew')
        
        # Второй ряд кнопок - экспорт
        ttk.Button(buttons_frame, text="Экспорт в Word", command=self.export_to_word).grid(
            row=1, column=0, padx=5, pady=5, sticky='ew')
        
        ttk.Button(buttons_frame, text="Экспорт в Excel", command=self.export_to_excel).grid(
            row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Третий ряд кнопок - импорт
        ttk.Button(buttons_frame, text="Импорт из Word", command=self.import_from_word).grid(
            row=2, column=0, padx=5, pady=5, sticky='ew')
        
        ttk.Button(buttons_frame, text="Импорт из Excel", command=self.import_from_excel).grid(
            row=2, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Button(buttons_frame, text="Импорт в базу", command=self.import_to_database).grid(
            row=2, column=2, padx=5, pady=5, sticky='ew')
        
        self.load_teachers()
        self.load_subjects()
    
    def export_to_word(self):
        export_to_word(self)
    
    def export_to_excel(self):
        export_to_excel(self)
    
    def import_from_word(self):
        """Импорт данных из Word отчета"""
        import_from_word(self)
    
    def import_from_excel(self):
        """Импорт данных из Excel отчета"""
        import_from_excel(self)
    
    def import_to_database(self):
        """Импорт данных из текущей таблицы в базу данных"""
        import_data_to_database(self)
    
    def refresh_data(self):
        """Обновление всех данных"""
        self.load_teachers()
        self.load_subjects()
        self.apply_filter()
    
    def clear_filters(self):
        self.teacher_combobox.set('')
        self.subject_combobox.set('')
        for row in self.results_table.get_children():
            self.results_table.delete(row)
    
    def load_teachers(self):
        cur = self.db_connection.cursor()
        cur.execute(LOAD_TEACHERS_FOR_FILTER_SQL)
        teachers = cur.fetchall()
        cur.close()
        self.teacher_combobox['values'] = [f"{teacher[1]} {teacher[2]} {teacher[3]}" for teacher in teachers]
    
    def load_subjects(self):
        cur = self.db_connection.cursor()
        cur.execute(LOAD_SUBJECTS_FOR_FILTER_SQL)
        subjects = cur.fetchall()
        cur.close()
        self.subject_combobox['values'] = [subject[1] for subject in subjects]
    
    def apply_filter(self):
        teacher_name = self.teacher_combobox.get()
        subject_name = self.subject_combobox.get()
        
        teacher_id = None
        subject_id = None
        
        if teacher_name:
            cur = self.db_connection.cursor()
            cur.execute(TEACHER_FILTER_SQL, (teacher_name,))
            result = cur.fetchone()
            if result:
                teacher_id = result[0]
            cur.close()
        
        if subject_name:
            cur = self.db_connection.cursor()
            cur.execute(SUBJECT_FILTER_SQL, (subject_name,))
            result = cur.fetchone()
            if result:
                subject_id = result[0]
            cur.close()
        
        cur = self.db_connection.cursor()
        cur.execute(
            APPLY_FILTERS_SQL, (teacher_id, teacher_id, subject_id, subject_id)
        )
        results = cur.fetchall()
        cur.close()
        
        for row in self.results_table.get_children():
            self.results_table.delete(row)
        for result in results:
            self.results_table.insert('', 'end', values=result)