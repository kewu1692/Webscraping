#
#
#
#

CREATE TABLE IF NOT EXISTS global_database.res_queue (
    res_id INT PRIMARY KEY AUTO_INCREMENT,
    res_name VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    res_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

#
#
#
#
