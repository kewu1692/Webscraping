# MySQL Async Worker Project

A Python application that manages asynchronous database operations with multiple worker processes for handling resource queue management and database initialization.

## Overview

This project implements an asynchronous MySQL-based system that:
- Manages a global resource queue
- Creates and initializes databases dynamically
- Processes jobs using multiple concurrent workers
- Handles database connections efficiently using connection pooling

## Features

- **Async Connection Pooling**: Efficient MySQL connection management using `aiomysql`
- **Multi-Worker Processing**: Concurrent job processing with configurable worker count
- **Dynamic Database Creation**: Automatic database and table creation for new resources
- **Transaction Management**: Proper rollback and commit handling
- **SQL Injection Protection**: Parameterized queries throughout
- **Error Handling**: Comprehensive error handling and logging
- **Testing Data Generation**: Built-in test data creation utilities

## Prerequisites

- Python 3.7+
- MySQL Server 5.7+ or 8.0+
- Required Python packages (see [Installation](#installation))

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mysql-async-worker-project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

### Prerequisites
- Docker installed on your system
- DBeaver (or any SQL client)

### Running the Database
```bash
# Start MySQL container
docker run -d \
  --name project-db \
  -e MYSQL_ROOT_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=projectdb \
  -p 3306:3306 \
  mysql:8.0

# Verify container is running
docker ps
```

## Configuration

Create a `config.py` file with your database settings:

```python
# Database Configuration
HOST = "localhost"
USER = "your_username"
PASSWORD = "your_password"
GLOBAL_DB_NAME = "global_database"

# Directory Paths for SQL Files
INIT_DB_DIR = "./sql/init_db"
INIT_TABLES_DIR = "./sql/init_tables"
RES_DB_DIR = "./sql/res_db"
RES_TABLES_DIR = "./sql/res_tables"
```

### Environment Variables (Optional)
You can also use environment variables:
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=your_username
export MYSQL_PASSWORD=your_password
```

## Usage

### Basic Usage

1. **Run the main application:**
   ```bash
   python main.py
   ```

2. **The application will:**
   - Create connection pool
   - Clear existing test databases
   - Initialize the global database
   - Insert testing data
   - Start worker processes to handle jobs

### Advanced Usage

**Customize worker count:**
```python
num_workers = 5  # Modify in main.py
```

**Adjust testing data:**
```python
await insert_testing_data(pool, number_of_testing_data=50)
```

## Project Structure

```
project/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── mysql_toolbox.py       # Database utility functions
├── db_clear_up.py         # Database cleanup operations
├── initialize_db.py       # Database initialization
├── testing_data.py        # Test data insertion
├── user_db_worker.py      # Worker processes for job handling
├── requirements.txt       # Python dependencies
├── sql/                   # SQL files directory
│   ├── init_db/          # Database initialization scripts
│   ├── init_tables/      # Table creation scripts
│   ├── res_db/           # Resource database scripts
│   └── res_tables/       # Resource table scripts
└── README.md             # This file
```

## Database Schema

### Global Database Tables

**res_queue Table:**
```sql
CREATE TABLE res_queue (
    res_id INT AUTO_INCREMENT PRIMARY KEY,
    res_name VARCHAR(255) NOT NULL,
    status ENUM('new', 'in_progress', 'done', 'error') DEFAULT 'new',
    res_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Resource Databases
Each resource gets its own database with:
- Custom tables based on resource type
- Review and tracking tables
- Resource-specific configurations

## API Reference

### Core Functions

#### `create_async_connection_pool(host, user, password)`
Creates and returns an async MySQL connection pool.

**Parameters:**
- `host` (str): MySQL server hostname
- `user` (str): MySQL username  
- `password` (str): MySQL password

**Returns:**
- `aiomysql.Pool`: Connection pool object

#### `dependency_creation_worker(pool, worker_id)`
Main worker function that processes jobs from the queue.

**Parameters:**
- `pool` (aiomysql.Pool): Database connection pool
- `worker_id` (int): Unique identifier for the worker

### Utility Functions

#### `execute_queries_in_directory(cursor, directory, replace_map)`
Executes all SQL files in a directory with variable replacement.

#### `execute_query_from_path(cursor, file_path, replace_map)`
Executes a single SQL file with variable replacement.

## Common Issues

### Connection Pool Errors
**Error:** `Error releasing connection: (<aiomysql.connection.Connection object>, set())`

**Solution:** Ensure you're not manually releasing connections when using `async with pool.acquire()`. The context manager handles connection release automatically.

### SQL Injection Warnings
**Issue:** Using string formatting in SQL queries

**Solution:** Use parameterized queries:
```python
# Bad
await cursor.execute(f"SELECT * FROM table WHERE id = {user_id}")

# Good  
await cursor.execute("SELECT * FROM table WHERE id = %s", (user_id,))
```

### Transaction Scope Issues
**Issue:** Commits/rollbacks outside connection scope

**Solution:** Keep all transaction operations within the `async with` block:
```python
async with pool.acquire() as conn:
    async with conn.cursor() as cursor:
        # Do operations
        await conn.commit()  # Inside the block
```
