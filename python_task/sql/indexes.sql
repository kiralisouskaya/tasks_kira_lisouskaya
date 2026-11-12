-- Composite index on room_id and sex to optimize GROUP BY and HAVING COUNT(DISTINCT sex) operations
CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);