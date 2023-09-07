CREATE TABLE urls (
    id bigint GENERATED ALWAYS AS IDENTITY,
    name character varying(255),
    created_at timestamp,
    scheme character varying(20)
);

CREATE TABLE url_checks (
    id bigint GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls(id),
    status_code integer,
    h1 text,
    title text,
    description text,
    created_at timestamp
);