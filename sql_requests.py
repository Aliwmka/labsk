# Запросы для преподавателей
INSERT_TEACHER_SQL = """
INSERT INTO teachers (last_name, first_name, middle_name, academic_degree, position, experience)
VALUES (%s, %s, %s, %s, %s, %s)
"""

FETCH_TEACHERS_SQL = """SELECT * FROM teachers ORDER BY last_name, first_name"""

DELETE_TEACHER_SQL = """DELETE FROM teachers WHERE teacher_id = %s"""

EDIT_TEACHER_SQL = """
UPDATE teachers
SET last_name = %s, first_name = %s, middle_name = %s, academic_degree = %s, position = %s, experience = %s
WHERE teacher_id = %s
"""

# Запросы для предметов
INSERT_SUBJECT_SQL = """
INSERT INTO subjects (subject_name, hours)
VALUES (%s, %s)
"""

FETCH_SUBJECTS_SQL = """SELECT * FROM subjects ORDER BY subject_name"""

DELETE_SUBJECT_SQL = """DELETE FROM subjects WHERE subject_id = %s"""

EDIT_SUBJECT_SQL = """
UPDATE subjects
SET subject_name = %s, hours = %s
WHERE subject_id = %s
"""

# Запросы для распределения нагрузки
INSERT_WORKLOAD_SQL = """
INSERT INTO workload (teacher_id, subject_id, group_number)
VALUES (%s, %s, %s)
"""

FETCH_WORKLOAD_SQL = """SELECT * FROM workload ORDER BY workload_id DESC"""

DELETE_WORKLOAD_SQL = """DELETE FROM workload WHERE workload_id = %s"""

EDIT_WORKLOAD_SQL = """
UPDATE workload
SET teacher_id = %s, subject_id = %s, group_number = %s
WHERE workload_id = %s
"""

FETCH_TEACHERS_FOR_WORKLOAD_SQL = """SELECT teacher_id, last_name, first_name, middle_name FROM teachers ORDER BY last_name, first_name"""

FETCH_SUBJECTS_FOR_WORKLOAD_SQL = """SELECT subject_id, subject_name FROM subjects ORDER BY subject_name"""

# Запросы для фильтрации
LOAD_TEACHERS_FOR_FILTER_SQL = """SELECT teacher_id, last_name, first_name, middle_name FROM teachers ORDER BY last_name, first_name"""

LOAD_SUBJECTS_FOR_FILTER_SQL = """SELECT subject_id, subject_name FROM subjects ORDER BY subject_name"""

TEACHER_FILTER_SQL = """SELECT teacher_id FROM teachers WHERE CONCAT(last_name, ' ', first_name, ' ', middle_name) = %s"""

SUBJECT_FILTER_SQL = """SELECT subject_id FROM subjects WHERE subject_name = %s"""

APPLY_FILTERS_SQL = """
SELECT w.workload_id, 
       t.last_name || ' ' || t.first_name || ' ' || t.middle_name AS teacher_name,
       s.subject_name,
       w.group_number
FROM workload w
JOIN teachers t ON w.teacher_id = t.teacher_id
JOIN subjects s ON w.subject_id = s.subject_id
WHERE (%s IS NULL OR w.teacher_id = %s)
AND (%s IS NULL OR w.subject_id = %s)
"""