from typing import Final

SELECT_TASK : Final[str] = """
SELECT * FROM Tasks
WHERE ID = $s;
"""

SELECT_TASKS: Final[str] = """
SELECT * FROM Tasks;
"""

SELECT_LAST_ID : Final[str] = """
SELECT ID FROM Tasks
ORDER BY ID DESC
LIMIT 1;
"""

CREATE_TASK : Final[str] = """
INSERT INTO Tasks(Title, UserID, IsCompleted, CreatedAt)
VALUES($s, $s, $s, NOW())
RETURNING *;
"""