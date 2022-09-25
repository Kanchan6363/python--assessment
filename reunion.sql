--
-- PostgreSQL database dump
--

-- Dumped from database version 10.22
-- Dumped by pg_dump version 10.22

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

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comment (
    post_id character varying(200),
    comment_id character varying(200),
    comment character varying(200)
);


ALTER TABLE public.comment OWNER TO postgres;

--
-- Name: following; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.following (
    user_email character varying(200),
    following_id character varying(200)
);


ALTER TABLE public.following OWNER TO postgres;

--
-- Name: likestatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.likestatus (
    user_email character varying(100),
    post_id character varying(200),
    status character varying(10)
);


ALTER TABLE public.likestatus OWNER TO postgres;

--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    post_id character varying(200) NOT NULL,
    title character varying(200),
    description character varying(200),
    create_time character varying(100),
    likes integer,
    dislikes integer,
    comment character varying(100)
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: postsusers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.postsusers (
    user_email character varying(100),
    post_id character varying(200)
);


ALTER TABLE public.postsusers OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id character varying(200) NOT NULL,
    email character varying(100),
    password character varying(100) NOT NULL,
    user_name character varying(100) NOT NULL,
    followers integer,
    following integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comment (post_id, comment_id, comment) FROM stdin;
post1	qwe12	very good
post1	uytr	 nice post
post1	po very	 very very nice
post1	vpoeporpoypo 	very nice
\.


--
-- Data for Name: following; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.following (user_email, following_id) FROM stdin;
\.


--
-- Data for Name: likestatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.likestatus (user_email, post_id, status) FROM stdin;
megha63637@gmail.com	post1	l
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (post_id, title, description, create_time, likes, dislikes, comment) FROM stdin;
post1	travel	manali diaries	2022-09-25 16:19:15.954397	2	1	very nice
\.


--
-- Data for Name: postsusers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.postsusers (user_email, post_id) FROM stdin;
megha63637@gmail.com	post1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password, user_name, followers, following) FROM stdin;
kan634	kanckuma@gmail.com	redhat	kanchan	2	0
me214	megha63637@gmail.com	admin	megha	1	11
\.


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

