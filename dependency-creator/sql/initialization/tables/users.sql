#
#
#
#

CREATE TABLE IF NOT EXISTS global_database.users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    level INTEGER,
    points INTEGER,
    review_count INTEGER,
    photo_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

#
#
#
#
