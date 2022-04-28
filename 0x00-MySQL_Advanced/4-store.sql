-- Script that creates a trigger that decreases the 
-- quantity of an item after adding a new order
CREATE TRIGGER decreaser
AFTER INSERT
ON orders
FOR EACH ROW
UPDATE items AS i
SET i.quantity = i.quantity - NEW.number
WHERE i.name = NEW.item_name;
