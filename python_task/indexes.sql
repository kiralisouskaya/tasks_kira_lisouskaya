-- Index on FK room_id to accelerate JOIN and GROUP BY
CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room);

-- Composite index on room_id and sex to optimize GROUP BY and HAVING COUNT(DISTINCT sex) operations
CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);