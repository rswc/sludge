CREATE TABLE IF NOT EXISTS worker (
    id_worker INTEGER PRIMARY KEY DEFAULT 0,
    `name` TEXT NOT NULL,
    surname TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    job_title TEXT NOT NULL,
    date_of_expiration DATE,
    thumbnail BLOB,
    rolling_secret INTEGER NOT NULL,
    rolling_counter INTEGER NOT NULL,
    otp_secret INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS `role` (
    id_role INTEGER PRIMARY KEY DEFAULT 0,
    `name` TEXT UNIQUE,
    color TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS roleOfWorker (
    id_worker INTEGER,
    id_role INTEGER,

    PRIMARY KEY(id_worker, id_role),
    FOREIGN KEY (id_worker) REFERENCES worker (id_worker) 
            ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (id_role) REFERENCES `role` (id_role) 
            ON DELETE CASCADE ON UPDATE NO ACTION
);
