from typing import Final

SELECT_TASK : Final[str] = """
SELECT * FROM Tasks
WHERE ID == $1;
"""

SELECT_TASKS: Final[str] = """
SELECT * FROM Tasks;
"""

SELECT_LAST_ID : Final[str] = """
SELECT ID FROM Tasks
ORDER BY ID DESC
LIMIT 1;
"""