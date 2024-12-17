create table users (
    email varchar(50) not null primary key, 
    ticker varchar(50),
    low_value float,
    high_value float) engine=innodb;
    
create table data (
    ticker varchar(50) not null, 
    value float not null, 
    timestamp timestamp default CURRENT_TIMESTAMP not null) engine=innodb;

CREATE INDEX idx_timestamp ON data(timestamp);
CREATE INDEX idx_ticker ON data(ticker);
