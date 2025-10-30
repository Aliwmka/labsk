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
        
        self.title("Распределение учебной нагрузки")
        self.geometry("1700x600")
        
        # Настройка шрифта по умолчанию должна быть ПОСЛЕ создания главного окна
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Настройка цветов и шрифтов
        self.style.configure('TFrame', background='#f0fff0')
        self.style.configure('TLabel', background='#f0fff0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'), foreground='black', background='#98fb98')
        self.style.map('TButton',
                      foreground=[('active', 'black'), ('pressed', 'white')],
                      background=[('active', '#90ee90'), ('pressed', '#2e8b57')])
        
        self.style.configure('Treeview',
                            rowheight=25,
                            background='#ffffff',
                            fieldbackground='#ffffff',
                            foreground='black',
                            font=('Arial', 10))
        
        self.style.configure('Treeview.Heading',
                            background='#98fb98',
                            foreground='black',
                            font=('Arial', 10, 'bold'))
        
        self.create_widgets()
    
    def create_widgets(self):
        # Создаем Notebook для вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Создаем фреймы для каждой вкладки
        self.teachers_frame = ttk.Frame(self.notebook)
        self.subjects_frame = ttk.Frame(self.notebook)
        self.workload_frame = ttk.Frame(self.notebook)
        self.filter_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.teachers_frame, text='Преподаватели')
        self.notebook.add(self.subjects_frame, text='Предметы')
        self.notebook.add(self.workload_frame, text='Распределение нагрузки')
        self.notebook.add(self.filter_frame, text='Фильтрация данных')
        
        # Инициализируем классы для каждой вкладки
        try:
            self.teachers = Teachers(self.teachers_frame, self.db_connection)
            self.subjects = Subjects(self.subjects_frame, self.db_connection)
            self.workload = WorkloadDistribution(self.workload_frame, self.db_connection)
            self.data_filter = DataFilter(self.filter_frame, self.db_connection)
            
            # Показываем данные при запуске
            self.teachers.show_teachers()
            self.subjects.show_subjects()
            
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при инициализации приложения: {str(e)}")

def main():
    conn = None
    try:
        conn = get_sync_db_connection()
        app = WorkloadApp(conn)
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        tk.messagebox.showerror("Ошибка", f"Ошибка при запуске приложения: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()