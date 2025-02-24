#
#
#
#


CREATE TABLE IF NOT EXISTS global_database.file_queue (
    file_id INT PRIMARY KEY AUTO_INCREMENT,
    status VARCHAR(50) NOT NULL,
    res_name VARCHAR(50) NOT NULL,
    folder_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)


#
#
#
#