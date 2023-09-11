package mysqldb

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/go-sql-driver/mysql"
)

type MySQLDB struct {
	Conn *sql.DB
}

func Connect() (*MySQLDB, error) {
	user := os.Getenv("MYSQL_USER")
	password := os.Getenv("MYSQL_PASS")
	host := os.Getenv("MYSQL_HOST")
	port := os.Getenv("MYSQL_PORT")
	database := os.Getenv("MYSQL_DB")

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", user, password, host, port, database)

	conn, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, err
	}

	db := &MySQLDB{Conn: conn}
	return db, nil
}

func (db *MySQLDB) Insert(table, query string, args ...interface{}) (sql.Result, error) {
	stmt, err := db.Conn.Prepare(fmt.Sprintf("INSERT INTO %s %s", table, query))
	if err != nil {
		return nil, err
	}
	defer stmt.Close()

	return stmt.Exec(args...)
}

func (db *MySQLDB) Query(query string, args ...interface{}) (*sql.Rows, error) {
	return db.Conn.Query(query, args...)
}

func (db *MySQLDB) Update(query string, args ...interface{}) (sql.Result, error) {
	return db.Conn.Exec(query, args...)
}

func (db *MySQLDB) Delete(query string, args ...interface{}) (sql.Result, error) {
	return db.Conn.Exec(query, args...)
}

func (db *MySQLDB) Close() error {
	return db.Conn.Close()
}
