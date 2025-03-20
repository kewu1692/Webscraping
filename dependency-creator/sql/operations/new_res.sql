SELECT
    res_id,
    res_name
FROM
    < GLOBAL_DB_NAME >.res_queue
WHERE
    status = 'new'
ORDER BY
    created_at
LIMIT
    1 FOR
UPDATE;