create table users (
    email varchar(50) not null primary key, 
    ticker varchar(50)) engine=innodb;
    
create table data (
    ticker varchar(50) not null, 
    value float not null, 
    timestamp timestamp default CURRENT_TIMESTAMP not null) engine=innodb;

CREATE INDEX idx_timestamp ON data(timestamp);
CREATE INDEX idx_ticker ON data(ticker);

SELECT
                        ticker,
                        AVG(value) AS average_value,
                        timestamp
                    FROM (
                        SELECT
                            d.ticker,
                            d.value,
                            d.timestamp
                        FROM
                            data d
                        WHERE
                            d.ticker = (
                                SELECT u.ticker
                                FROM users u
                                WHERE u.email = 'alchemai@deleit.com'
                            )
                        ORDER BY
                            d.timestamp DESC
                        LIMIT 5000
                    ) AS filtered_data
                    HAVING COUNT(*) = 5000;