# filters.py
from tkinter import ttk
from export import export_to_word, export_to_excel
from import_data import import_from_excel, import_from_word
from tkinter import messagebox
from sql_requests import (
    LOAD_TEACHERS_FOR_FILTER_SQL,
    LOAD_SUBJECTS_FOR_FILTER_SQL,
    TEACHER_FILTER_SQL,
    SUBJECT_FILTER_SQL,
    APPLY_FILTERS_SQL,
    INSERT_WORKLOAD_SQL,
    FETCH_TEACHERS_FOR_WORKLOAD_SQL,
    FETCH_SUBJECTS_FOR_WORKLOAD_SQL,
)

class DataFilter:
    def __init__(self, parent_frame, db_connection, app=None):
        self.results_table = None
        self.subject_combobox = None
        self.teacher_combobox = None
        self.parent_frame = parent_frame
        self.db_connection = db_connection
        self.app = app
        self.create_filter_form()
        self.refresh_data()
    
    def refresh_data(self):
        """Обновление данных преподавателей и предметов"""
        self.teachers = self.fetch_teachers_for_import()
        self.subjects = self.fetch_subjects_for_import()
        
        if hasattr(self, 'teacher_combobox'):
            self.load_teachers()
        
        if hasattr(self, 'subject_combobox'):
            self.load_subjects()
        
        # Обновляем таблицу результатов
        self.reload_all_workload()
    
    def fetch_teachers_for_import(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_TEACHERS_FOR_WORKLOAD_SQL)
        data = cur.fetchall()
        cur.close()
        return data
    
    def fetch_subjects_for_import(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_SUBJECTS_FOR_WORKLOAD_SQL)
        data = cur.fetchall()
        cur.close()
        return data
    
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
        columns = ('ID', 'Преподаватель', 'Предмет', 'Группа')
        self.results_table = ttk.Treeview(self.parent_frame, columns=columns, show='headings')
        
        # Настраиваем заголовки колонок
        for col in columns:
            self.results_table.heading(col, text=col)
            self.results_table.column(col, width=150, anchor='center')
        
        self.results_table.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')
        
        # Фрейм для кнопок
        buttons_frame = ttk.Frame(self.parent_frame)
        buttons_frame.grid(row=3, column=0, columnspan=4, pady=(5, 10), sticky='ew')
        
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)
        buttons_frame.columnconfigure(3, weight=1)
        
        ttk.Button(buttons_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(buttons_frame, text="Очистить", command=self.clear_filters).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        word_button = ttk.Button(buttons_frame, text="Экспорт в Word", command=self.export_to_word)
        word_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        excel_button = ttk.Button(buttons_frame, text="Экспорт в Excel", command=self.export_to_excel)
        excel_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        excel_imp_button = ttk.Button(buttons_frame, text="Импорт из Excel", command=self.handle_import_excel)
        excel_imp_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        
        word_imp_button = ttk.Button(buttons_frame, text="Импорт из Word", command=self.handle_import_word)
        word_imp_button.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        refresh_button = ttk.Button(buttons_frame, text="Обновить данные", command=self.refresh_data)
        refresh_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        
        # Настройка весов для растягивания
        self.parent_frame.columnconfigure(0, weight=1)
        self.parent_frame.columnconfigure(1, weight=1)
        self.parent_frame.rowconfigure(2, weight=1)
    
    def handle_import_excel(self):
        def on_data(headers, rows):
            self.process_imported_data(headers, rows)
        import_from_excel(self.parent_frame.winfo_toplevel(), on_data)
    
    def handle_import_word(self):
        def on_data(headers, rows):
            self.process_imported_data(headers, rows)
        import_from_word(self.parent_frame.winfo_toplevel(), on_data)
    
    def process_imported_data(self, headers, rows):
        try:
            imported_count = 0
            skipped_count = 0
            errors = []
            
            print(f"Начало обработки импорта: {len(rows)} записей")
            print(f"Заголовки: {headers}")
            
            for i, row in enumerate(rows):
                # Пропускаем пустые строки
                if not any(str(cell).strip() for cell in row if cell is not None):
                    skipped_count += 1
                    continue
                    
                print(f"Обработка строки {i}: {row}")
                
                # Определяем индексы столбцов на основе заголовков
                teacher_col = self._find_column_index(headers, ['преподаватель', 'teacher', 'фио', 'фам'])
                subject_col = self._find_column_index(headers, ['предмет', 'subject', 'дисциплина'])
                group_col = self._find_column_index(headers, ['группа', 'group', 'номер группы'])
                
                # Если не нашли по заголовкам, используем порядок по умолчанию
                if teacher_col is None: teacher_col = 0
                if subject_col is None: subject_col = 1
                if group_col is None: group_col = 2
                
                # Получаем данные с проверкой индексов
                teacher_name = str(row[teacher_col]).strip() if len(row) > teacher_col and row[teacher_col] else ""
                subject_name = str(row[subject_col]).strip() if len(row) > subject_col and row[subject_col] else ""
                group_number = str(row[group_col]).strip() if len(row) > group_col and row[group_col] else ""
                
                print(f"Извлеченные данные: преподаватель='{teacher_name}', предмет='{subject_name}', группа='{group_number}'")
                
                # Проверяем обязательные поля
                if not teacher_name or not subject_name or not group_number:
                    errors.append(f"Строка {i+1}: отсутствуют обязательные поля")
                    skipped_count += 1
                    continue
                
                # Ищем преподавателя по ФИО
                teacher_id = None
                for teacher in self.teachers:
                    full_name = f"{teacher[1]} {teacher[2]} {teacher[3]}".strip()
                    last_first = f"{teacher[1]} {teacher[2]}".strip()
                    
                    if (teacher_name == full_name or 
                        teacher_name == last_first or
                        teacher_name.startswith(teacher[1]) or
                        full_name.startswith(teacher_name)):
                        teacher_id = teacher[0]
                        print(f"Найден преподаватель: {full_name} -> ID: {teacher_id}")
                        break
                
                # Ищем предмет по названию
                subject_id = None
                for subject in self.subjects:
                    if (subject_name == subject[1] or
                        subject[1].startswith(subject_name)):
                        subject_id = subject[0]
                        print(f"Найден предмет: {subject[1]} -> ID: {subject_id}")
                        break
                
                if not teacher_id:
                    errors.append(f"Строка {i+1}: преподаватель '{teacher_name}' не найден в базе")
                    skipped_count += 1
                    continue
                    
                if not subject_id:
                    errors.append(f"Строка {i+1}: предмет '{subject_name}' не найден в базе")
                    skipped_count += 1
                    continue
                
                try:
                    cur = self.db_connection.cursor()
                    cur.execute(INSERT_WORKLOAD_SQL, (
                        teacher_id, 
                        subject_id, 
                        group_number
                    ))
                    self.db_connection.commit()
                    cur.close()
                    imported_count += 1
                    print(f"Успешно импортирована запись {i+1}")
                    
                except Exception as e:
                    if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
                        errors.append(f"Строка {i+1}: дублирующая запись (уже существует в базе)")
                    else:
                        errors.append(f"Строка {i+1}: ошибка базы данных - {str(e)}")
                    skipped_count += 1
                    continue
            
            # Обновляем данные
            self.reload_all_workload()
            if self.app and hasattr(self.app, 'workload'):
                self.app.workload.show_workload()
            
            # Формируем сообщение о результате
            message = f"Импорт завершен!\nУспешно: {imported_count} записей"
            if skipped_count > 0:
                message += f"\nПропущено: {skipped_count} записей"
            
            if errors:
                error_details = "\n".join(errors[:10])
                if len(errors) > 10:
                    error_details += f"\n... и еще {len(errors) - 10} ошибок"
                message += f"\n\nОшибки:\n{error_details}"
            
            messagebox.showinfo("Результат импорта", message)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать данные: {str(e)}")
            print(f"Критическая ошибка импорта: {e}")
    
    def _find_column_index(self, headers, possible_names):
        """Находит индекс столбца по возможным названиям"""
        if not headers:
            return None
            
        headers_lower = [str(h).lower() for h in headers]
        for name in possible_names:
            for i, header in enumerate(headers_lower):
                if name in header:
                    return i
        return None
    
    def reload_all_workload(self):
        cur = self.db_connection.cursor()
        cur.execute("""
            SELECT w.workload_id, 
                   t.last_name || ' ' || t.first_name || ' ' || COALESCE(t.middle_name, '') AS teacher_name,
                   s.subject_name,
                   w.group_number
            FROM workload w
            JOIN teachers t ON w.teacher_id = t.teacher_id
            JOIN subjects s ON w.subject_id = s.subject_id
            ORDER BY w.workload_id DESC
        """)
        results = cur.fetchall()
        cur.close()
        
        # Очищаем таблицу
        for row in self.results_table.get_children():
            self.results_table.delete(row)
        
        # Заполняем новыми данными
        for result in results:
            self.results_table.insert('', 'end', values=result)
    
    def export_to_word(self):
        export_to_word(self)
    
    def export_to_excel(self):
        export_to_excel(self)
    
    def clear_filters(self):
        self.teacher_combobox.set('')
        self.subject_combobox.set('')
        self.reload_all_workload()
    
    def load_teachers(self):
        cur = self.db_connection.cursor()
        cur.execute(LOAD_TEACHERS_FOR_FILTER_SQL)
        teachers = cur.fetchall()
        cur.close()
        teacher_names = [f"{teacher[1]} {teacher[2]} {teacher[3]}" for teacher in teachers]
        self.teacher_combobox['values'] = teacher_names
        print(f"Загружено {len(teacher_names)} преподавателей для фильтра")
    
    def load_subjects(self):
        cur = self.db_connection.cursor()
        cur.execute(LOAD_SUBJECTS_FOR_FILTER_SQL)
        subjects = cur.fetchall()
        cur.close()
        subject_names = [subject[1] for subject in subjects]
        self.subject_combobox['values'] = subject_names
        print(f"Загружено {len(subject_names)} предметов для фильтра")
    
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
        
        try:
            cur = self.db_connection.cursor()
            cur.execute(
                APPLY_FILTERS_SQL, 
                (teacher_id, teacher_id, subject_id, subject_id)
            )
            results = cur.fetchall()
            cur.close()
            
            # Очищаем таблицу
            for row in self.results_table.get_children():
                self.results_table.delete(row)
            
            # Заполняем отфильтрованными данными
            for result in results:
                self.results_table.insert('', 'end', values=result)
                
            messagebox.showinfo("Успех", f"Найдено {len(results)} записей")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось применить фильтр: {e}")
            print(f"Ошибка фильтрации: {e}")