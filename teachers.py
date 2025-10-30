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
        try:
            data = self.validate_teacher_data()
            if data is None:
                return
            
            self.insert_teacher(data)
            self.show_teachers()
            self.clear_entries()
            messagebox.showinfo("Успех", "Преподаватель успешно сохранен!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении преподавателя: {str(e)}")
            self.db_connection.rollback()
    
    def validate_teacher_data(self):
        """Проверка и преобразование данных преподавателя"""
        raw_data = [entry.get().strip() for entry in self.teacher_entries]
        
        # Проверяем обязательные поля
        if not raw_data[0]:  # Фамилия
            messagebox.showwarning("Предупреждение", "Поле 'Фамилия' обязательно для заполнения")
            return None
        if not raw_data[1]:  # Имя
            messagebox.showwarning("Предупреждение", "Поле 'Имя' обязательно для заполнения")
            return None
        
        # Преобразуем стаж в число
        try:
            experience = int(raw_data[5]) if raw_data[5] else 0
        except ValueError:
            messagebox.showwarning("Предупреждение", "Поле 'Стаж' должно быть числом")
            return None
        
        # Возвращаем проверенные данные
        return [
            raw_data[0],  # Фамилия
            raw_data[1],  # Имя
            raw_data[2],  # Отчество
            raw_data[3],  # Ученая степень
            raw_data[4],  # Должность
            experience    # Стаж
        ]
    
    def insert_teacher(self, data):
        cur = self.db_connection.cursor()
        try:
            cur.execute(INSERT_TEACHER_SQL, data)
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
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
        try:
            selected_items = self.teachers_table.selection()
            if not selected_items:
                messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
                return
            
            selected_item = selected_items[0]
            teacher_id = self.teachers_table.item(selected_item, 'values')[0]
            
            # Подтверждение удаления
            result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?")
            if not result:
                return
            
            cur = self.db_connection.cursor()
            cur.execute(DELETE_TEACHER_SQL, (teacher_id,))
            self.db_connection.commit()
            cur.close()
            
            self.teachers_table.delete(selected_item)
            messagebox.showinfo("Успех", "Запись успешно удалена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении записи: {str(e)}")
            self.db_connection.rollback()
    
    def edit_record(self):
        try:
            selected_items = self.teachers_table.selection()
            if not selected_items:
                messagebox.showwarning("Предупреждение", "Выберите запись для редактирования")
                return
            
            selected_item = selected_items[0]
            teacher_id = self.teachers_table.item(selected_item, 'values')[0]
            
            data = self.validate_teacher_data()
            if data is None:
                return
            
            cur = self.db_connection.cursor()
            cur.execute(EDIT_TEACHER_SQL, (*data, teacher_id))
            self.db_connection.commit()
            cur.close()
            
            self.show_teachers()
            self.clear_entries()
            messagebox.showinfo("Успех", "Запись успешно обновлена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при редактировании записи: {str(e)}")
            self.db_connection.rollback()
    
    def clear_entries(self):
        for entry in self.teacher_entries:
            entry.delete(0, tk.END)