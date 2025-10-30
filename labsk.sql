--
-- PostgreSQL database dump
--

\restrict amhJxYf9oNDqKDS2JIDE7vCXCUKknMEx2wLYYrSPHtx1Eu1e3aucOThekkJM1Ke

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-19 16:09:37

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 222 (class 1259 OID 16613)
-- Name: subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subjects (
    subject_id integer NOT NULL,
    subject_name character varying(100) NOT NULL,
    hours integer NOT NULL
);


ALTER TABLE public.subjects OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16612)
-- Name: subjects_subject_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subjects_subject_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_subject_id_seq OWNER TO postgres;

--
-- TOC entry 5035 (class 0 OID 0)
-- Dependencies: 221
-- Name: subjects_subject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subjects_subject_id_seq OWNED BY public.subjects.subject_id;


--
-- TOC entry 220 (class 1259 OID 16603)
-- Name: teachers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teachers (
    teacher_id integer NOT NULL,
    last_name character varying(50) NOT NULL,
    first_name character varying(50) NOT NULL,
    middle_name character varying(50),
    academic_degree character varying(100),
    "position" character varying(100),
    experience integer
);


ALTER TABLE public.teachers OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16602)
-- Name: teachers_teacher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teachers_teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.teachers_teacher_id_seq OWNER TO postgres;

--
-- TOC entry 5036 (class 0 OID 0)
-- Dependencies: 219
-- Name: teachers_teacher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teachers_teacher_id_seq OWNED BY public.teachers.teacher_id;


--
-- TOC entry 224 (class 1259 OID 16623)
-- Name: workload; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workload (
    workload_id integer NOT NULL,
    teacher_id integer,
    subject_id integer,
    group_number character varying(20) NOT NULL
);


ALTER TABLE public.workload OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16622)
-- Name: workload_workload_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.workload_workload_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workload_workload_id_seq OWNER TO postgres;

--
-- TOC entry 5037 (class 0 OID 0)
-- Dependencies: 223
-- Name: workload_workload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workload_workload_id_seq OWNED BY public.workload.workload_id;


--
-- TOC entry 4867 (class 2604 OID 16616)
-- Name: subjects subject_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects ALTER COLUMN subject_id SET DEFAULT nextval('public.subjects_subject_id_seq'::regclass);


--
-- TOC entry 4866 (class 2604 OID 16606)
-- Name: teachers teacher_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers ALTER COLUMN teacher_id SET DEFAULT nextval('public.teachers_teacher_id_seq'::regclass);


--
-- TOC entry 4868 (class 2604 OID 16626)
-- Name: workload workload_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workload ALTER COLUMN workload_id SET DEFAULT nextval('public.workload_workload_id_seq'::regclass);


--
-- TOC entry 5027 (class 0 OID 16613)
-- Dependencies: 222
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.subjects VALUES (1, 'Математический анализ', 120);
INSERT INTO public.subjects VALUES (2, 'Физика', 90);
INSERT INTO public.subjects VALUES (3, 'Программирование', 150);
INSERT INTO public.subjects VALUES (4, 'Базы данных', 80);
INSERT INTO public.subjects VALUES (5, 'Теория алгоритмов', 100);


--
-- TOC entry 5025 (class 0 OID 16603)
-- Dependencies: 220
-- Data for Name: teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.teachers VALUES (1, 'Иванов', 'Петр', 'Сергеевич', 'д.т.н.', 'профессор', 25);
INSERT INTO public.teachers VALUES (2, 'Петрова', 'Мария', 'Ивановна', 'к.ф.-м.н.', 'доцент', 15);
INSERT INTO public.teachers VALUES (3, 'Сидоров', 'Алексей', 'Викторович', 'к.т.н.', 'доцент', 12);
INSERT INTO public.teachers VALUES (4, 'Козлова', 'Елена', 'Дмитриевна', 'д.п.н.', 'профессор', 30);
INSERT INTO public.teachers VALUES (5, 'Николаев', 'Сергей', 'Петрович', 'к.э.н.', 'старший преподаватель', 8);


--
-- TOC entry 5029 (class 0 OID 16623)
-- Dependencies: 224
-- Data for Name: workload; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.workload VALUES (1, 1, 1, 'ПМ-101');
INSERT INTO public.workload VALUES (2, 2, 2, 'ФИ-201');
INSERT INTO public.workload VALUES (3, 3, 3, 'ИВТ-301');
INSERT INTO public.workload VALUES (4, 4, 4, 'ИБ-401');
INSERT INTO public.workload VALUES (5, 5, 5, 'ПИ-102');
INSERT INTO public.workload VALUES (6, 1, 3, 'ПМ-102');
INSERT INTO public.workload VALUES (7, 2, 1, 'ФИ-202');


--
-- TOC entry 5038 (class 0 OID 0)
-- Dependencies: 221
-- Name: subjects_subject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subjects_subject_id_seq', 5, true);


--
-- TOC entry 5039 (class 0 OID 0)
-- Dependencies: 219
-- Name: teachers_teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teachers_teacher_id_seq', 5, true);


--
-- TOC entry 5040 (class 0 OID 0)
-- Dependencies: 223
-- Name: workload_workload_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workload_workload_id_seq', 7, true);


--
-- TOC entry 4872 (class 2606 OID 16621)
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (subject_id);


--
-- TOC entry 4870 (class 2606 OID 16611)
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (teacher_id);


--
-- TOC entry 4874 (class 2606 OID 16630)
-- Name: workload workload_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workload
    ADD CONSTRAINT workload_pkey PRIMARY KEY (workload_id);


--
-- TOC entry 4875 (class 2606 OID 16636)
-- Name: workload workload_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workload
    ADD CONSTRAINT workload_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(subject_id);


--
-- TOC entry 4876 (class 2606 OID 16631)
-- Name: workload workload_teacher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workload
    ADD CONSTRAINT workload_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.teachers(teacher_id);


-- Completed on 2025-10-19 16:09:37

--
-- PostgreSQL database dump complete
--

\unrestrict amhJxYf9oNDqKDS2JIDE7vCXCUKknMEx2wLYYrSPHtx1Eu1e3aucOThekkJM1Ke

