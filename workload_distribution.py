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
    def __init__(self, parent_frame, db_connection):
        self.parent_frame = parent_frame
        self.db_connection = db_connection
        self.create_workload_form()
    
    def create_workload_form(self):
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
        
        # Добавляем событие двойного щелчка
        self.workload_table.bind("<Double-1>", self.fill_entries)
        
        # Загружаем данные в комбобоксы
        self.load_teachers()
        self.load_subjects()
        # Показываем текущую нагрузку
        self.show_workload()
    
    def load_teachers(self):
        try:
            cur = self.db_connection.cursor()
            cur.execute(FETCH_TEACHERS_FOR_WORKLOAD_SQL)
            teachers = cur.fetchall()
            cur.close()
            self.teacher_combobox['values'] = [f"{teacher[1]} {teacher[2]} {teacher[3]}" for teacher in teachers]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке преподавателей: {str(e)}")
    
    def load_subjects(self):
        try:
            cur = self.db_connection.cursor()
            cur.execute(FETCH_SUBJECTS_FOR_WORKLOAD_SQL)
            subjects = cur.fetchall()
            cur.close()
            self.subject_combobox['values'] = [subject[1] for subject in subjects]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке предметов: {str(e)}")
    
    def fill_entries(self, event):
        try:
            selected_items = self.workload_table.selection()
            if not selected_items:
                return
            
            selected_item = selected_items[0]
            values = self.workload_table.item(selected_item, 'values')
            self.teacher_combobox.set(values[1])
            self.subject_combobox.set(values[2])
            self.group_entry.delete(0, tk.END)
            self.group_entry.insert(0, values[3])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при заполнении полей: {str(e)}")
    
    def save_workload(self):
        try:
            teacher_name = self.teacher_combobox.get()
            subject_name = self.subject_combobox.get()
            group_number = self.group_entry.get().strip()
            
            if not teacher_name or not subject_name or not group_number:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            
            # Получаем ID преподавателя
            cur = self.db_connection.cursor()
            cur.execute("SELECT teacher_id FROM teachers WHERE CONCAT(last_name, ' ', first_name, ' ', middle_name) = %s", (teacher_name,))
            teacher_result = cur.fetchone()
            if not teacher_result:
                messagebox.showwarning("Предупреждение", "Преподаватель не найден")
                cur.close()
                return
            teacher_id = teacher_result[0]
            
            # Получаем ID предмета
            cur.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,))
            subject_result = cur.fetchone()
            if not subject_result:
                messagebox.showwarning("Предупреждение", "Предмет не найден")
                cur.close()
                return
            subject_id = subject_result[0]
            
            cur.execute(INSERT_WORKLOAD_SQL, (teacher_id, subject_id, group_number))
            self.db_connection.commit()
            cur.close()
            
            self.show_workload()
            self.clear_entries()
            messagebox.showinfo("Успех", "Нагрузка успешно сохранена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении нагрузки: {str(e)}")
            try:
                self.db_connection.rollback()
            except:
                pass
    
    def show_workload(self):
        try:
            workload = self.fetch_workload()
            for row in self.workload_table.get_children():
                self.workload_table.delete(row)
            for item in workload:
                self.workload_table.insert('', 'end', values=item)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке нагрузки: {str(e)}")
    
    def fetch_workload(self):
        cur = self.db_connection.cursor()
        cur.execute(FETCH_WORKLOAD_SQL)
        workload = cur.fetchall()
        cur.close()
        return workload
    
    def delete_record(self):
        try:
            selected_items = self.workload_table.selection()
            if not selected_items:
                messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
                return
            
            selected_item = selected_items[0]
            workload_id = self.workload_table.item(selected_item, 'values')[0]
            
            # Подтверждение удаления
            result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?")
            if not result:
                return
            
            cur = self.db_connection.cursor()
            cur.execute(DELETE_WORKLOAD_SQL, (workload_id,))
            self.db_connection.commit()
            cur.close()
            
            self.workload_table.delete(selected_item)
            messagebox.showinfo("Успех", "Запись успешно удалена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении записи: {str(e)}")
            try:
                self.db_connection.rollback()
            except:
                pass
    
    def edit_record(self):
        try:
            selected_items = self.workload_table.selection()
            if not selected_items:
                messagebox.showwarning("Предупреждение", "Выберите запись для редактирования")
                return
            
            selected_item = selected_items[0]
            workload_id = self.workload_table.item(selected_item, 'values')[0]
            
            teacher_name = self.teacher_combobox.get()
            subject_name = self.subject_combobox.get()
            group_number = self.group_entry.get().strip()
            
            if not teacher_name or not subject_name or not group_number:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            
            # Получаем ID преподавателя
            cur = self.db_connection.cursor()
            cur.execute("SELECT teacher_id FROM teachers WHERE CONCAT(last_name, ' ', first_name, ' ', middle_name) = %s", (teacher_name,))
            teacher_result = cur.fetchone()
            if not teacher_result:
                messagebox.showwarning("Предупреждение", "Преподаватель не найден")
                cur.close()
                return
            teacher_id = teacher_result[0]
            
            # Получаем ID предмета
            cur.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,))
            subject_result = cur.fetchone()
            if not subject_result:
                messagebox.showwarning("Предупреждение", "Предмет не найден")
                cur.close()
                return
            subject_id = subject_result[0]
            
            cur.execute(EDIT_WORKLOAD_SQL, (teacher_id, subject_id, group_number, workload_id))
            self.db_connection.commit()
            cur.close()
            
            self.show_workload()
            self.clear_entries()
            messagebox.showinfo("Успех", "Запись успешно обновлена!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при редактировании записи: {str(e)}")
            try:
                self.db_connection.rollback()
            except:
                pass
    
    def clear_entries(self):
        self.teacher_combobox.set('')
        self.subject_combobox.set('')
        self.group_entry.delete(0, tk.END)