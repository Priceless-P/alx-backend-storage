-- Creates a stored procedure that computes average weighted score for a student
DELIMITER / /

CREATE PROCEDURE ComputeAverageWeightedScoreForUser
(IN user_id INT)
BEGIN
DECLARE
	total_score FLOAT DEFAULT 0;
DECLARE
	total_weight INT DEFAULT 0;
DECLARE
	weighted_score FLOAT;
	-- Calculate total weighted score
	SELECT SUM(score * weight) INTO total_score
	FROM corrections
	    JOIN projects ON corrections.project_id = projects.id
	WHERE
	    corrections.user_id = user_id;
	-- Calculate total weight
	SELECT SUM(weight) INTO total_weight FROM projects;
	-- Calculate average weighted score
	IF total_weight > 0 THEN
	SET
	    weighted_score = total_score / total_weight;
	ELSE SET weighted_score = 0;
END
	IF;
	-- Update average_score for the user
	UPDATE users SET average_score = weighted_score WHERE id = user_id;
END
//

DELIMITER;
