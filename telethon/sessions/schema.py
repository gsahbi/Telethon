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
    seq integer,
    unread_count integer
);

CREATE TRIGGER IF NOT EXISTS delete_update_state_trigger
after delete on "sessions" for each row
begin
    delete from update_state where update_state.session_id = old.dc_id;
end;

"""