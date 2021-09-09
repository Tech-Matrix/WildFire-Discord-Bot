CREATE TABLE IF NOT EXISTS offences {
    server_id VARCHAR(30) NOT NULL,
    id VARCHAR(30) NOT NULL PRIMARY KEY,
    num_of_offences INTEGER NOT NULL
}

CREATE TABLE IF NOT EXISTS filter {
    server_id bigint NOT NULL,
    filter_pattern varchar(256) NOT NULL
}

