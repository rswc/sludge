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

CREATE TABLE IF NOT EXISTS accesspoint (
    id_ap   INTEGER NOT NULL,
    name    VARCHAR2(32) NOT NULL,
    id_room INTEGER NOT NULL,
    icon    INTEGER,

    PRIMARY KEY ( id_ap )
);

CREATE TABLE IF NOT EXISTS accesspointingroup (
    id_ap    INTEGER NOT NULL,
    id_group INTEGER NOT NULL,

    PRIMARY KEY ( id_ap, id_group )
);

CREATE TABLE IF NOT EXISTS accessrule (
    id_role  INTEGER NOT NULL,
    id_group INTEGER NOT NULL,
    policy   CHAR(1) NOT NULL,

    PRIMARY KEY ( id_group, id_role )
);

CREATE TABLE IF NOT EXISTS door (
    id_door     INTEGER NOT NULL,
    id_room_src INTEGER NOT NULL,
    id_room_dst INTEGER NOT NULL,

    PRIMARY KEY ( id_door )
);

CREATE TABLE IF NOT EXISTS dooringroup (
    id_group INTEGER NOT NULL,
    id_door  INTEGER NOT NULL,

    PRIMARY KEY ( id_door, id_group )
);

CREATE TABLE IF NOT EXISTS event (
    id_event  INTEGER NOT NULL,
    timestamp DATE NOT NULL UNIQUE,
    type      INTEGER NOT NULL,
    id_worker INTEGER NOT NULL,
    payload   VARCHAR2(512),
    id_ap     INTEGER,
    id_door   INTEGER,

    CHECK ( ( ( id_ap IS NOT NULL )
        AND ( id_door IS NULL ) )
        OR ( ( id_door IS NOT NULL )
            AND ( id_ap IS NULL ) ) ),
    
    PRIMARY KEY ( id_event )
);

CREATE TABLE IF NOT EXISTS facility (
    id_facility INTEGER NOT NULL,
    name        VARCHAR2(32) NOT NULL UNIQUE,
    address     VARCHAR2(64) NOT NULL,

    PRIMARY KEY ( id_facility )
);

CREATE TABLE IF NOT EXISTS "Group" (
    id_group INTEGER NOT NULL,
    name     VARCHAR2(16) NOT NULL UNIQUE,
    severity INTEGER NOT NULL,

    PRIMARY KEY ( id_group )
);

CREATE TABLE IF NOT EXISTS "Resource" (
    id_resource INTEGER NOT NULL,
    name        VARCHAR2(32) NOT NULL,

    PRIMARY KEY ( id_resource ),
    UNIQUE ( name )
);


CREATE TABLE IF NOT EXISTS room (
    id_room      INTEGER NOT NULL,
    name         VARCHAR2(32) NOT NULL,
    id_facility  INTEGER NOT NULL,
    coordinate_x REAL,
    coordinate_y REAL,

    PRIMARY KEY ( id_room ),
    UNIQUE ( name )
);


CREATE TABLE IF NOT EXISTS transfer (
    id_transfer     INTEGER NOT NULL,
    timestamp       DATE NOT NULL,
    id_resource     INTEGER NOT NULL,
    id_worker       INTEGER NOT NULL,
    amount          REAL NOT NULL,
    id_facility_src INTEGER NOT NULL,
    id_facility_dst INTEGER NOT NULL,

    PRIMARY KEY ( id_transfer ),
    UNIQUE ( timestamp,
            id_worker,
            id_resource,
            id_facility_src,
            id_facility_dst )
);
