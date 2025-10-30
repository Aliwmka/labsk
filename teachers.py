# teachers.py
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from sql_requests import (
    INSERT_TEACHER_SQL,
    FETCH_TEACHERS_SQL,
    DELETE_TEACHER_SQL,
    EDIT_TEACHER_SQL,
)

class Teachers:
    def __init__(self, parent_frame, db_connection, app=None):
        self.parent_frame = parent_frame
        self.db_connection = db_connection
        self.app = app
        self.create_teachers_form()
    
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
        
        refresh_button = ttk.Button(buttons_frame, text="Обновить", command=self.show_teachers)
        refresh_button.grid(row=0, column=4, padx=5, pady=5)
        
        import_button = ttk.Button(buttons_frame, text="Импорт из Excel", command=self.handle_import_excel)
        import_button.grid(row=0, column=5, padx=5, pady=5)
        
        # Добавляем событие двойного щелчка
        self.teachers_table.bind("<Double-1>", self.fill_entries)
        
        self.show_teachers()
    
    def fill_entries(self, event):
        if not self.teachers_table.selection():
            return
        selected_item = self.teachers_table.selection()[0]
        values = self.teachers_table.item(selected_item, 'values')
        for entry, value in zip(self.teacher_entries, values[1:]):  # Пропускаем 'ID'
            entry.delete(0, tk.END)
            entry.insert(0, value)
    
    def save_teacher(self):
        data = [entry.get() for entry in self.teacher_entries]
        
        # Проверка обязательных полей
        if not data[0] or not data[1]:  # Фамилия и Имя обязательны
            messagebox.showwarning("Предупреждение", "Фамилия и Имя являются обязательными полями!")
            return
        
        try:
            # Проверяем числовое поле стажа
            experience = int(data[5]) if data[5] else 0
            
            self.insert_teacher(data)
            self.show_teachers()
            self.clear_entries()
            messagebox.showinfo("Успех", "Преподаватель успешно добавлен!")
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
        except ValueError:
            messagebox.showerror("Ошибка", "Стаж должен быть числом!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить преподавателя: {e}")
    
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
        if not self.teachers_table.selection():
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        
        selected_item = self.teachers_table.selection()[0]
        teacher_id = self.teachers_table.item(selected_item, 'values')[0]
        teacher_name = f"{self.teachers_table.item(selected_item, 'values')[1]} {self.teachers_table.item(selected_item, 'values')[2]}"
        
        # Подтверждение удаления
        result = messagebox.askyesno(
            "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить преподавателя '{teacher_name}'?\nВсе связанные записи нагрузки также будут удалены."
        )
        
        if not result:
            return
        
        try:
            cur = self.db_connection.cursor()
            cur.execute(DELETE_TEACHER_SQL, (teacher_id,))
            self.db_connection.commit()
            cur.close()
            
            self.teachers_table.delete(selected_item)
            self.clear_entries()
            messagebox.showinfo("Успех", "Преподаватель и все связанные записи нагрузки успешно удалены!")
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                    self.app.workload.show_workload()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Ошибка", f"Не удалось удалить преподавателя: {e}")
    
    def edit_record(self):
        if not self.teachers_table.selection():
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования!")
            return
        
        selected_item = self.teachers_table.selection()[0]
        teacher_id = self.teachers_table.item(selected_item, 'values')[0]
        data = [entry.get() for entry in self.teacher_entries]
        
        # Проверка обязательных полей
        if not data[0] or not data[1]:  # Фамилия и Имя обязательны
            messagebox.showwarning("Предупреждение", "Фамилия и Имя являются обязательными полями!")
            return
        
        try:
            # Проверяем числовое поле стажа
            experience = int(data[5]) if data[5] else 0
            
            cur = self.db_connection.cursor()
            cur.execute(EDIT_TEACHER_SQL, (*data, teacher_id))
            self.db_connection.commit()
            cur.close()
            self.show_teachers()
            self.clear_entries()
            messagebox.showinfo("Успех", "Данные преподавателя успешно обновлены!")
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                    self.app.workload.show_workload()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
        except ValueError:
            messagebox.showerror("Ошибка", "Стаж должен быть числом!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")
    
    def clear_entries(self):
        for entry in self.teacher_entries:
            entry.delete(0, tk.END)
    
    def handle_import_excel(self):
        def on_data(headers, rows):
            self.process_imported_teachers(headers, rows)
        
        from import_data import import_teachers_from_excel
        import_teachers_from_excel(self.parent_frame.winfo_toplevel(), on_data)
    
    def process_imported_teachers(self, headers, rows):
        try:
            imported_count = 0
            skipped_count = 0
            
            for row in rows:
                if len(row) < 6:
                    skipped_count += 1
                    continue
                    
                last_name = str(row[0]).strip() if row[0] else ""
                first_name = str(row[1]).strip() if row[1] else ""
                middle_name = str(row[2]).strip() if row[2] else ""
                academic_degree = str(row[3]).strip() if row[3] else ""
                position = str(row[4]).strip() if row[4] else ""
                experience = str(row[5]).strip() if row[5] else ""
                
                # Проверяем обязательные поля
                if not last_name or not first_name:
                    skipped_count += 1
                    continue
                
                try:
                    # Преобразуем числовые поля
                    experience_int = int(experience) if experience else 0
                    
                    cur = self.db_connection.cursor()
                    cur.execute(INSERT_TEACHER_SQL, (last_name, first_name, middle_name, academic_degree, position, experience_int))
                    self.db_connection.commit()
                    cur.close()
                    imported_count += 1
                    
                except (ValueError, Exception) as e:
                    skipped_count += 1
                    continue
            
            self.show_teachers()
            
            # Обновляем данные в других модулях
            if self.app:
                if hasattr(self.app, 'workload'):
                    self.app.workload.refresh_data()
                if hasattr(self.app, 'data_filter'):
                    self.app.data_filter.refresh_data()
            
            message = f"Импорт преподавателей завершен!\nУспешно: {imported_count} записей"
            if skipped_count > 0:
                message += f"\nПропущено: {skipped_count} записей (некорректные данные)"
            messagebox.showinfo("Успех", message)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать преподавателей: {str(e)}")