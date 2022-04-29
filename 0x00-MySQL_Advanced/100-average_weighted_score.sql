-- Script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE avg INT;
    DECLARE unit_weight FLOAT;

    SELECT 1 / SUM(weight) INTO unit_weight
    FROM projects AS p
    JOIN corrections AS c ON p.id = c.project_id
    WHERE c.user_id = user_id;

    SELECT ROUND(SUM(score * (p.weight * unit_weight)), 0) INTO avg
    FROM corrections AS c
    JOIN projects AS p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    UPDATE users
    SET average_score = avg
    WHERE id = user_id;
END; $$
DELIMITER ;
