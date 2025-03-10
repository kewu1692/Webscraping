SELECT
    res_id, res_name
FROM
    < DB_NAME >.res_queue
WHERE
    status = 'new'