CREATE TABLE IF NOT EXISTS offences {
    server_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    num_of_offences INTEGER NOT NULL
};

CREATE TABLE IF NOT EXISTS filter {
    server_id BIGINT NOT NULL,
    filter_pattern VARCHAR(256) NOT NULL
};

CREATE TABLE IF NOT EXISTS prefixes {
    server_id BIGINT NOT NULL,
    prefix VARCHAR(16) NOT NULL
};

