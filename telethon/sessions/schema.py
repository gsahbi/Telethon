SCHEMA = """

CREATE TABLE IF NOT EXISTS
version (version integer primary key);
                
CREATE TABLE IF NOT EXISTS 
sessions (
    dc_id integer primary key,
    server_address text,
    port integer,
    auth_key blob
);

CREATE TABLE IF NOT EXISTS 
entities (
    id integer primary key,
    hash integer not null,
    username text,
    phone integer,
    name text
);

CREATE TABLE IF NOT EXISTS 
sent_files (
    md5_digest blob,
    file_size integer,
    type integer,
    id integer,
    hash integer,
    primary key(md5_digest, file_size, type)
);

CREATE TABLE IF NOT EXISTS 
update_state (
    session_id integer primary key,
    date integer,
    pts integer,
    qts integer,
    seq integer
);

CREATE TRIGGER IF NOT EXISTS delete_update_state_trigger
AFTER DELETE ON "sessions" FOR EACH ROW
BEGIN
    DELETE FROM update_state WHERE update_state.session_id = old.dc_id;
END;

CREATE TRIGGER IF NOT EXISTS insert_update_state_trigger
AFTER INSERT ON "sessions" FOR EACH ROW
BEGIN
    INSERT OR REPLACE INTO update_state(session_id, `date`, pts, qts, seq) 
    VALUES (new.dc_id, CURRENT_TIMESTAMP, 0,0,0);
END;
"""

UPSERT_UPDATE_STATE = """
INSERT OR REPLACE INTO update_state(session_id, `date`, pts, qts, seq) 
VALUES (?, ?, ?, ?, ?)
"""

GET_UPDATE_STATE = """
SELECT `date`, pts, qts, seq FROM update_state WHERE session_id=?
"""