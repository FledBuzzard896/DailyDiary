from typing import Final

SELECT_TASK : Final[str] = """
SELECT * FROM Tasks
WHERE ID = $s;
"""

SELECT_TASKS: Final[str] = """
SELECT * FROM Tasks;
"""

CREATE_TASK: Final[str] = """
INSERT INTO tasks (title, description, user_id, status_id, created_at, updated_at, deadline, completed_at, is_deleted)
VALUES ($s, $s, $s, $s, NOW(), NOW(), $s, $s, FALSE)
RETURNING id, title, description, created_at, updated_at, deadline, completed_at, user_id, status_id, is_deleted;
"""