SELECT
    res_id, res_name
FROM
    < DB_NAME >.res_queue
WHERE
    status = 'new'

    -- select only one row from the table while sorted by created_at and this should be block for other transactions
    