#
#
#
#

CREATE TABLE IF NOT EXISTS <REST_NAME>.reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    rev_date DATE,
    rev_desc VARCHAR(225) NOT NULL,
    star_rating DECIMAL(5, 2) NOT NULL,
    service_type VARCHAR(50),
    meal_type VARCHAR(50),
    food_rating DECIMAL(5, 2),
    service_rating DECIMAL(5, 2),
    atmo_rating DECIMAL(5, 2),
    recomm_DISH VARCHAR(225),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES global_database.users(user_id)
)

#
#
#
#