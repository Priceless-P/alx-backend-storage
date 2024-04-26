-- Creates a stored procedure AddBonus that
-- adds a new correction for a student.

DROP IF PROCEDURE EXISTS AddBonus;

DELIMITER $$
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;

    -- check if project exists
    SELECT id into project_id
    FROM projects
    WHERE name = project_name;

    -- if it doesn't exist
    IF project_id IS NULL
    THEN
        INSERT INTO projects (name)
        VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;
    INSERT INTO corrections (user_id, project_name, score)
    VALUES (user_id, project_id, score);
END $$
DELIMITER ;
