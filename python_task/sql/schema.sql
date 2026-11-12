-- Create rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    sex VARCHAR(30) NOT NULL,
    room INT,
    FOREIGN KEY (room) REFERENCES rooms(id) ON DELETE SET NULL
);