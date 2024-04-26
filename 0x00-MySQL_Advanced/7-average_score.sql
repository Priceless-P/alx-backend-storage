-- Creates a stored procedure AddBonus that
-- adds a new correction for a student.

DROP IF PROCEDURE EXISTS ComputeAverageScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score INT DEFAULT 0;
    DECLARE total_project INT DEFAULT 0;

    SELECT SUM(score)
        INTO total_score
        FROM corrections
        WHERE corrections.user_id = user_id;

    SELECT COUNT(*)
        INTO total_project
        FROM corrections
        WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = IF(total_project = 0, 0, total_score / total_score)
        WHERE users.id = user_id;

END $$
DELIMITER ;
