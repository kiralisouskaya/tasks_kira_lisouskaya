# Query 1: Returns a list of rooms and the total count of students in each room
QUERY_ROOMS_WITH_STUDENT_COUNT = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name,
        COUNT(s.id) AS student_count
    FROM rooms r
    LEFT JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    ORDER BY r.id;
"""

# Query 2: Returns top 5 rooms with the lowest average student age
QUERY_TOP5_ROOMS_LOWEST_AVG_AGE = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name,
        -- RU: Переводим возраст в годы (делим на 365.25 для учета високосных) и округляем до 1 знака[cite: 2].
        -- EN: Convert age to years (divide by 365.25 for leap years) and round to 1 decimal place[cite: 2].
        ROUND(AVG((CURRENT_DATE - s.birthday) / 365.25), 1) AS avg_age
    FROM rooms r
    JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    -- RU: Сортировка по возрастанию и лимит 5. / EN: Sort ascending and limit to 5.
    ORDER BY avg_age ASC
    LIMIT 5;
"""

# Query 3: Returns top 5 rooms with the highest age difference among resident students
QUERY_TOP5_ROOMS_HIGHEST_AGE_DIFF = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name,
        MAX(s.birthday) - MIN(s.birthday) AS age_difference
    FROM rooms r
    JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    HAVING COUNT(s.id) > 1
    ORDER BY age_difference DESC
    LIMIT 5;
"""

# Query 4: Returns a list of rooms inhabited by students of mixed sexes
QUERY_ROOMS_WITH_MIXED_SEXES = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name
    FROM rooms r
    JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    HAVING COUNT(DISTINCT s.sex) > 1
    ORDER BY r.id;
"""