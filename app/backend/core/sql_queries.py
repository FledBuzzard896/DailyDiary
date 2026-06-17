from typing import Final

SELECT_TASK : Final[str] = """
SELECT * FROM tasks
WHERE id = $1;
"""

SELECT_TASKS: Final[str] = """
SELECT * FROM tasks;
"""

CREATE_TASK: Final[str] = """
INSERT INTO tasks (title, description, user_id, status_id, created_at, updated_at, deadline, completed_at, is_deleted)
VALUES ($1, $2, $3, $4, NOW(), NOW(), $5, $6, FALSE)
RETURNING id, title, description, created_at, updated_at, deadline, completed_at, user_id, status_id, is_deleted;
"""

SELECT_USER_BY_LOGIN: Final[str] = """
SELECT id, login, password_hash, name, surname, email, created_at
FROM users
WHERE login = $1
"""

SELECT_USER_BY_ID: Final[str] = """
SELECT * FROM users
WHERE id = $1;
"""

INSERT_USER: Final[str] = """
INSERT INTO users (login, password_hash, name, surname, email, created_at)
VALUES ($1, $2, $3, $4, $5, NOW())
RETURNING id, login, password_hash, name, surname, email, created_at;
"""