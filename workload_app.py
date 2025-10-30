# workload_app.py
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from db_connection import get_sync_db_connection
from teachers import Teachers
from subjects import Subjects
from workload_distribution import WorkloadDistribution
from filters import DataFilter

class WorkloadApp(tk.Tk):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        
        self.teachers_frame = None
        self.subjects_frame = None
        self.workload_frame = None
        self.filter_frame = None
        
        self.teachers = None
        self.subjects = None
        self.workload = None
        self.data_filter = None
        
        self.title("Система управления учебной нагрузкой")
        self.geometry("1700x600")
        
        # Настройка шрифта по умолчанию должна быть ПОСЛЕ создания главного окна
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Настройка цветов и шрифтов
        self.style.configure('TFrame', background='#f0f8ff')
        self.style.configure('TLabel', background='#f0f8ff', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'), foreground='black', background='#87ceeb')
        self.style.map('TButton',
                      foreground=[('active', 'black'), ('pressed', 'white')],
                      background=[('active', '#7ec0ee'), ('pressed', '#4682b4')])
        
        self.style.configure('Treeview',
                            rowheight=25,
                            font=('Arial', 9),
                            background='#ffffff',
                            fieldbackground='#ffffff')
        self.style.configure('Treeview.Heading',
                            font=('Arial', 10, 'bold'),
                            background='#b0e0e6')
        
        # Цвет основного окна
        self.configure(bg='#f0f8ff')
        
        self.create_widgets()
        self.show()
    
    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        
        # Преподаватели
        self.teachers_frame = ttk.Frame(tab_control)
        tab_control.add(self.teachers_frame, text='Преподаватели')
        self.teachers = Teachers(self.teachers_frame, self.db_connection, self)
        
        # Предметы
        self.subjects_frame = ttk.Frame(tab_control)
        tab_control.add(self.subjects_frame, text='Предметы')
        self.subjects = Subjects(self.subjects_frame, self.db_connection, self)
        
        # Распределение нагрузки
        self.workload_frame = ttk.Frame(tab_control)
        tab_control.add(self.workload_frame, text='Распределение нагрузки')
        self.workload = WorkloadDistribution(self.workload_frame, self.db_connection, self)
        
        # Фильтрация данных
        self.filter_frame = ttk.Frame(tab_control)
        tab_control.add(self.filter_frame, text='Фильтрация данных')
        self.data_filter = DataFilter(self.filter_frame, self.db_connection, self)
        
        tab_control.pack(expand=1, fill='both')
    
    def show(self):
        self.teachers.show_teachers()
        self.subjects.show_subjects()
        self.workload.show_workload()

def main():
    conn = None
    try:
        conn = get_sync_db_connection()
        app = WorkloadApp(conn)
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()