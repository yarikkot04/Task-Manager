1. Get all statuses, not repeating, alphabetically ordered
```
SELECT DISTINCT is_done 
FROM tasks_task
ORDER BY is_done ASC;
```
2. Get the count of all tasks in each project, order by tasks count descending
```
SELECT tasks_project.name, COUNT(tasks_task.id) AS tasks_count
FROM tasks_project
LEFT JOIN tasks_task ON tasks_project.id = tasks_task.project_id
GROUP BY tasks_project.id, tasks_project.name
ORDER BY tasks_count DESC;
```
3. Get the count of all tasks in each project, order by projects names
```
SELECT tasks_project.name, COUNT(tasks_task.id) AS tasks_count
FROM tasks_project
LEFT JOIN tasks_task ON tasks_project.id = tasks_task.project_id
GROUP BY tasks_project.id, tasks_project.name
ORDER BY tasks_project.name ASC;
```
4. Get the tasks for all projects having the name beginning with "N" letter
```
SELECT tasks_task.*
FROM tasks_task
JOIN tasks_project ON tasks_task.project_id = tasks_project.id
WHERE tasks_project.name LIKE 'N%';
```
5. Get the list of projects containing the 'a' letter in the middle, show tasks count (inc. NULL projects)
```
SELECT tasks_project.name, COUNT(tasks_task.id) AS tasks_count
FROM tasks_project
LEFT JOIN tasks_task ON tasks_project.id = tasks_task.project_id
WHERE tasks_project.name LIKE '_%a%_'
GROUP BY tasks_project.id, tasks_project.name
UNION
SELECT 'Task without project' AS name, COUNT(id) AS tasks_count
FROM tasks_task
WHERE project_id IS NULL;
```
6. Get the list of tasks with duplicate names and their count
```
SELECT title, COUNT(id) AS duplicate_count
FROM tasks_task
GROUP BY title
HAVING COUNT(id) > 1
ORDER BY title ASC;
```
7. Get tasks with exact matches of both name and status in 'Delivery' project
```
SELECT tasks_task.title, tasks_task.is_done, COUNT(*) AS matches_count
FROM tasks_task
JOIN tasks_project ON tasks_task.project_id = tasks_project.id
WHERE tasks_project.name = 'Delivery'
GROUP BY tasks_task.title, tasks_task.is_done
HAVING COUNT(*) > 1
ORDER BY matches_count DESC;
```
8. Get project names having more than 10 tasks in status 'completed'
```
SELECT tasks_project.name
FROM tasks_project
JOIN tasks_task ON tasks_project.id = tasks_task.project_id
WHERE tasks_task.is_done = true
GROUP BY tasks_project.id, tasks_project.name
HAVING COUNT(tasks_task.id) > 10
ORDER BY tasks_project.id ASC;
```