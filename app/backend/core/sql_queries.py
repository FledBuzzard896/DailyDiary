from typing import Final

SELECT_TASK : Final[str] = """
SELECT * FROM tasks
WHERE id = $s;
"""

SELECT_TASKS: Final[str] = """
SELECT * FROM tasks;
"""

CREATE_TASK: Final[str] = """
INSERT INTO tasks (title, description, user_id, status_id, created_at, updated_at, deadline, completed_at, is_deleted)
VALUES ($s, $s, $s, $s, NOW(), NOW(), $s, $s, FALSE)
RETURNING id, title, description, created_at, updated_at, deadline, completed_at, user_id, status_id, is_deleted;
"""

SELECT_USER_BY_LOGIN: Final[str] = """
SELECT * FROM users;
WHERE login = $s;
"""

SELECT_USER_BY_ID: Final[str] = """
SELECT * FROM users;
WHERE id = $s;
"""