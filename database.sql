--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

-- Started on 2023-08-28 12:43:27 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 212 (class 1259 OID 41086)
-- Name: url_checks; Type: TABLE; Schema: public; Owner: ikhanter
--

CREATE TABLE public.url_checks (
    id bigint NOT NULL,
    url_id bigint,
    status_code integer,
    h1 text,
    title text,
    description text,
    created_at timestamp without time zone
);


ALTER TABLE public.url_checks OWNER TO ikhanter;

--
-- TOC entry 211 (class 1259 OID 41085)
-- Name: checks_id_seq; Type: SEQUENCE; Schema: public; Owner: ikhanter
--

ALTER TABLE public.url_checks ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.checks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 210 (class 1259 OID 41080)
-- Name: urls; Type: TABLE; Schema: public; Owner: ikhanter
--

CREATE TABLE public.urls (
    id bigint NOT NULL,
    name character varying(255),
    created_at timestamp without time zone,
    scheme character varying(20)
);


ALTER TABLE public.urls OWNER TO ikhanter;

--
-- TOC entry 209 (class 1259 OID 41079)
-- Name: urls_id_seq; Type: SEQUENCE; Schema: public; Owner: ikhanter
--

ALTER TABLE public.urls ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.urls_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3321 (class 0 OID 41086)
-- Dependencies: 212
-- Data for Name: url_checks; Type: TABLE DATA; Schema: public; Owner: ikhanter
--

COPY public.url_checks (id, url_id, status_code, h1, title, description, created_at) FROM stdin;
\.


--
-- TOC entry 3319 (class 0 OID 41080)
-- Dependencies: 210
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: ikhanter
--

COPY public.urls (id, name, created_at, scheme) FROM stdin;
\.


--
-- TOC entry 3327 (class 0 OID 0)
-- Dependencies: 211
-- Name: checks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ikhanter
--

SELECT pg_catalog.setval('public.checks_id_seq', 1, false);


--
-- TOC entry 3328 (class 0 OID 0)
-- Dependencies: 209
-- Name: urls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ikhanter
--

SELECT pg_catalog.setval('public.urls_id_seq', 1, false);


--
-- TOC entry 3177 (class 2606 OID 41092)
-- Name: url_checks checks_pkey; Type: CONSTRAINT; Schema: public; Owner: ikhanter
--

ALTER TABLE ONLY public.url_checks
    ADD CONSTRAINT checks_pkey PRIMARY KEY (id);


--
-- TOC entry 3175 (class 2606 OID 41084)
-- Name: urls urls_pkey; Type: CONSTRAINT; Schema: public; Owner: ikhanter
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_pkey PRIMARY KEY (id);


--
-- TOC entry 3178 (class 2606 OID 41093)
-- Name: url_checks checks_url_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ikhanter
--

ALTER TABLE ONLY public.url_checks
    ADD CONSTRAINT checks_url_id_fkey FOREIGN KEY (url_id) REFERENCES public.urls(id);


-- Completed on 2023-08-28 12:43:30 MSK

--
-- PostgreSQL database dump complete
--

