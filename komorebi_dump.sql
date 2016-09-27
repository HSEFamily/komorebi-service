--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.1

-- Started on 2016-09-28 01:49:50 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12395)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2233 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 563 (class 1247 OID 16634)
-- Name: crew_role; Type: TYPE; Schema: public; Owner: komorebi_psql
--

CREATE TYPE crew_role AS ENUM (
    'director',
    'screenwriter',
    'composer',
    'producer',
    'editor',
    'operator'
);


ALTER TYPE crew_role OWNER TO komorebi_psql;

--
-- TOC entry 569 (class 1247 OID 16868)
-- Name: movie_status; Type: TYPE; Schema: public; Owner: komorebi_psql
--

CREATE TYPE movie_status AS ENUM (
    'watched',
    'favourite',
    'watch_later',
    'non_watched'
);


ALTER TYPE movie_status OWNER TO komorebi_psql;

--
-- TOC entry 566 (class 1247 OID 16861)
-- Name: user_role; Type: TYPE; Schema: public; Owner: komorebi_psql
--

CREATE TYPE user_role AS ENUM (
    'owner',
    'admin',
    'visitor'
);


ALTER TYPE user_role OWNER TO komorebi_psql;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 188 (class 1259 OID 16921)
-- Name: cast_movies; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE cast_movies (
    id integer NOT NULL,
    actor_id integer NOT NULL,
    movie_id integer NOT NULL
);


ALTER TABLE cast_movies OWNER TO komorebi_psql;

--
-- TOC entry 187 (class 1259 OID 16919)
-- Name: cast_movies_id_seq; Type: SEQUENCE; Schema: public; Owner: komorebi_psql
--

CREATE SEQUENCE cast_movies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cast_movies_id_seq OWNER TO komorebi_psql;

--
-- TOC entry 2234 (class 0 OID 0)
-- Dependencies: 187
-- Name: cast_movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: komorebi_psql
--

ALTER SEQUENCE cast_movies_id_seq OWNED BY cast_movies.id;


--
-- TOC entry 196 (class 1259 OID 17046)
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE chat_messages (
    id integer NOT NULL,
    from_id integer NOT NULL,
    to_id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    message text NOT NULL
);


ALTER TABLE chat_messages OWNER TO komorebi_psql;

--
-- TOC entry 195 (class 1259 OID 17044)
-- Name: chat_message_id_seq; Type: SEQUENCE; Schema: public; Owner: komorebi_psql
--

CREATE SEQUENCE chat_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE chat_message_id_seq OWNER TO komorebi_psql;

--
-- TOC entry 2235 (class 0 OID 0)
-- Dependencies: 195
-- Name: chat_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: komorebi_psql
--

ALTER SEQUENCE chat_message_id_seq OWNED BY chat_messages.id;


--
-- TOC entry 192 (class 1259 OID 16990)
-- Name: clubs; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE clubs (
    id integer NOT NULL,
    name character varying(50),
    description character varying(255)
);


ALTER TABLE clubs OWNER TO komorebi_psql;

--
-- TOC entry 191 (class 1259 OID 16988)
-- Name: clubs_id_seq; Type: SEQUENCE; Schema: public; Owner: komorebi_psql
--

CREATE SEQUENCE clubs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE clubs_id_seq OWNER TO komorebi_psql;

--
-- TOC entry 2236 (class 0 OID 0)
-- Dependencies: 191
-- Name: clubs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: komorebi_psql
--

ALTER SEQUENCE clubs_id_seq OWNED BY clubs.id;


--
-- TOC entry 190 (class 1259 OID 16939)
-- Name: crew_movies; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE crew_movies (
    id integer NOT NULL,
    crew_id integer NOT NULL,
    movie_id integer NOT NULL,
    crew_role crew_role NOT NULL
);


ALTER TABLE crew_movies OWNER TO komorebi_psql;

--
-- TOC entry 189 (class 1259 OID 16937)
-- Name: crew_movies_id_seq; Type: SEQUENCE; Schema: public; Owner: komorebi_psql
--

CREATE SEQUENCE crew_movies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crew_movies_id_seq OWNER TO komorebi_psql;

--
-- TOC entry 2237 (class 0 OID 0)
-- Dependencies: 189
-- Name: crew_movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: komorebi_psql
--

ALTER SEQUENCE crew_movies_id_seq OWNED BY crew_movies.id;


--
-- TOC entry 183 (class 1259 OID 16885)
-- Name: movies; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE movies (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    year date NOT NULL,
    description character varying(255),
    tagline character varying(50),
    duration character varying(50),
    genre character varying(50)[],
    country character varying(50)[],
    picture character varying(100)
);


ALTER TABLE movies OWNER TO komorebi_psql;

--
-- TOC entry 186 (class 1259 OID 16914)
-- Name: persons; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE persons (
    id integer NOT NULL,
    name character varying(100)
);


ALTER TABLE persons OWNER TO komorebi_psql;

--
-- TOC entry 182 (class 1259 OID 16879)
-- Name: users; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE users (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    email character varying(50),
    user_name character varying(50) NOT NULL,
    password character varying(50) NOT NULL
);


ALTER TABLE users OWNER TO komorebi_psql;

--
-- TOC entry 194 (class 1259 OID 17016)
-- Name: users_clubs; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE users_clubs (
    id integer NOT NULL,
    user_id integer NOT NULL,
    club_id integer NOT NULL,
    user_role user_role NOT NULL
);


ALTER TABLE users_clubs OWNER TO komorebi_psql;

--
-- TOC entry 193 (class 1259 OID 17014)
-- Name: users_clubs_id_seq; Type: SEQUENCE; Schema: public; Owner: komorebi_psql
--

CREATE SEQUENCE users_clubs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_clubs_id_seq OWNER TO komorebi_psql;

--
-- TOC entry 2238 (class 0 OID 0)
-- Dependencies: 193
-- Name: users_clubs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: komorebi_psql
--

ALTER SEQUENCE users_clubs_id_seq OWNED BY users_clubs.id;


--
-- TOC entry 181 (class 1259 OID 16877)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: komorebi_psql
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO komorebi_psql;

--
-- TOC entry 2239 (class 0 OID 0)
-- Dependencies: 181
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: komorebi_psql
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- TOC entry 185 (class 1259 OID 16895)
-- Name: users_movies; Type: TABLE; Schema: public; Owner: komorebi_psql
--

CREATE TABLE users_movies (
    id integer NOT NULL,
    user_id integer NOT NULL,
    movie_id integer NOT NULL,
    status movie_status NOT NULL,
    rating integer,
    comment text
);


ALTER TABLE users_movies OWNER TO komorebi_psql;

--
-- TOC entry 184 (class 1259 OID 16893)
-- Name: users_movies_id_seq; Type: SEQUENCE; Schema: public; Owner: komorebi_psql
--

CREATE SEQUENCE users_movies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_movies_id_seq OWNER TO komorebi_psql;

--
-- TOC entry 2240 (class 0 OID 0)
-- Dependencies: 184
-- Name: users_movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: komorebi_psql
--

ALTER SEQUENCE users_movies_id_seq OWNED BY users_movies.id;


--
-- TOC entry 2077 (class 2604 OID 16924)
-- Name: id; Type: DEFAULT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY cast_movies ALTER COLUMN id SET DEFAULT nextval('cast_movies_id_seq'::regclass);


--
-- TOC entry 2081 (class 2604 OID 17049)
-- Name: id; Type: DEFAULT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY chat_messages ALTER COLUMN id SET DEFAULT nextval('chat_message_id_seq'::regclass);


--
-- TOC entry 2079 (class 2604 OID 16993)
-- Name: id; Type: DEFAULT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY clubs ALTER COLUMN id SET DEFAULT nextval('clubs_id_seq'::regclass);


--
-- TOC entry 2078 (class 2604 OID 16942)
-- Name: id; Type: DEFAULT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY crew_movies ALTER COLUMN id SET DEFAULT nextval('crew_movies_id_seq'::regclass);


--
-- TOC entry 2075 (class 2604 OID 16882)
-- Name: id; Type: DEFAULT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- TOC entry 2080 (class 2604 OID 17019)
-- Name: id; Type: DEFAULT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_clubs ALTER COLUMN id SET DEFAULT nextval('users_clubs_id_seq'::regclass);


--
-- TOC entry 2076 (class 2604 OID 16898)
-- Name: id; Type: DEFAULT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_movies ALTER COLUMN id SET DEFAULT nextval('users_movies_id_seq'::regclass);


--
-- TOC entry 2093 (class 2606 OID 16926)
-- Name: cast_movies_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY cast_movies
    ADD CONSTRAINT cast_movies_pkey PRIMARY KEY (id);


--
-- TOC entry 2101 (class 2606 OID 17054)
-- Name: chat_message_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY chat_messages
    ADD CONSTRAINT chat_message_pkey PRIMARY KEY (id);


--
-- TOC entry 2097 (class 2606 OID 16995)
-- Name: clubs_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY clubs
    ADD CONSTRAINT clubs_pkey PRIMARY KEY (id);


--
-- TOC entry 2095 (class 2606 OID 16944)
-- Name: crew_movies_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY crew_movies
    ADD CONSTRAINT crew_movies_pkey PRIMARY KEY (id);


--
-- TOC entry 2086 (class 2606 OID 16892)
-- Name: movies_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- TOC entry 2091 (class 2606 OID 16918)
-- Name: persons_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- TOC entry 2099 (class 2606 OID 17021)
-- Name: users_clubs_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_clubs
    ADD CONSTRAINT users_clubs_pkey PRIMARY KEY (id);


--
-- TOC entry 2088 (class 2606 OID 16903)
-- Name: users_movies_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_movies
    ADD CONSTRAINT users_movies_pkey PRIMARY KEY (id);


--
-- TOC entry 2084 (class 2606 OID 16884)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2089 (class 1259 OID 16987)
-- Name: person_name_idx; Type: INDEX; Schema: public; Owner: komorebi_psql
--

CREATE INDEX person_name_idx ON persons USING btree (name);


--
-- TOC entry 2082 (class 1259 OID 16986)
-- Name: username_idx; Type: INDEX; Schema: public; Owner: komorebi_psql
--

CREATE INDEX username_idx ON users USING btree (user_name);


--
-- TOC entry 2104 (class 2606 OID 16927)
-- Name: cast_movies_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY cast_movies
    ADD CONSTRAINT cast_movies_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES persons(id);


--
-- TOC entry 2105 (class 2606 OID 16932)
-- Name: cast_movies_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY cast_movies
    ADD CONSTRAINT cast_movies_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES movies(id);


--
-- TOC entry 2110 (class 2606 OID 17055)
-- Name: chat_message_from_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY chat_messages
    ADD CONSTRAINT chat_message_from_id_fkey FOREIGN KEY (from_id) REFERENCES users(id);


--
-- TOC entry 2111 (class 2606 OID 17060)
-- Name: chat_message_to_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY chat_messages
    ADD CONSTRAINT chat_message_to_id_fkey FOREIGN KEY (to_id) REFERENCES users(id);


--
-- TOC entry 2106 (class 2606 OID 16945)
-- Name: crew_movies_crew_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY crew_movies
    ADD CONSTRAINT crew_movies_crew_id_fkey FOREIGN KEY (crew_id) REFERENCES persons(id);


--
-- TOC entry 2107 (class 2606 OID 16950)
-- Name: crew_movies_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY crew_movies
    ADD CONSTRAINT crew_movies_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES movies(id);


--
-- TOC entry 2109 (class 2606 OID 17027)
-- Name: users_clubs_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_clubs
    ADD CONSTRAINT users_clubs_club_id_fkey FOREIGN KEY (club_id) REFERENCES clubs(id);


--
-- TOC entry 2108 (class 2606 OID 17022)
-- Name: users_clubs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_clubs
    ADD CONSTRAINT users_clubs_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- TOC entry 2103 (class 2606 OID 16909)
-- Name: users_movies_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_movies
    ADD CONSTRAINT users_movies_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES movies(id);


--
-- TOC entry 2102 (class 2606 OID 16904)
-- Name: users_movies_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: komorebi_psql
--

ALTER TABLE ONLY users_movies
    ADD CONSTRAINT users_movies_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- TOC entry 2232 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2016-09-28 01:50:08 MSK

--
-- PostgreSQL database dump complete
--

