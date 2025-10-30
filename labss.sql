--
-- PostgreSQL database dump
--

\restrict V2xEiWEYi7wcnEU3eGsh73pL29iwVCnM5roKjgoe6iRUspNLOdwR2ZYMDue2hUb

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-19 16:25:06

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
-- TOC entry 224 (class 1259 OID 16670)
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    booking_id integer NOT NULL,
    client_id integer,
    room_id integer,
    check_in_date date NOT NULL,
    check_out_date date,
    note text
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16669)
-- Name: bookings_booking_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookings_booking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookings_booking_id_seq OWNER TO postgres;

--
-- TOC entry 5037 (class 0 OID 0)
-- Dependencies: 223
-- Name: bookings_booking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookings_booking_id_seq OWNED BY public.bookings.booking_id;


--
-- TOC entry 220 (class 1259 OID 16643)
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients (
    client_id integer NOT NULL,
    last_name character varying(50) NOT NULL,
    first_name character varying(50) NOT NULL,
    middle_name character varying(50),
    passport_data character varying(100) NOT NULL,
    comment text
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16642)
-- Name: clients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_client_id_seq OWNER TO postgres;

--
-- TOC entry 5038 (class 0 OID 0)
-- Dependencies: 219
-- Name: clients_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_client_id_seq OWNED BY public.clients.client_id;


--
-- TOC entry 222 (class 1259 OID 16656)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    room_id integer NOT NULL,
    room_number character varying(10) NOT NULL,
    capacity integer NOT NULL,
    comfort_level character varying(50) NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16655)
-- Name: rooms_room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rooms_room_id_seq OWNER TO postgres;

--
-- TOC entry 5039 (class 0 OID 0)
-- Dependencies: 221
-- Name: rooms_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_room_id_seq OWNED BY public.rooms.room_id;


--
-- TOC entry 4868 (class 2604 OID 16673)
-- Name: bookings booking_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings ALTER COLUMN booking_id SET DEFAULT nextval('public.bookings_booking_id_seq'::regclass);


--
-- TOC entry 4866 (class 2604 OID 16646)
-- Name: clients client_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN client_id SET DEFAULT nextval('public.clients_client_id_seq'::regclass);


--
-- TOC entry 4867 (class 2604 OID 16659)
-- Name: rooms room_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN room_id SET DEFAULT nextval('public.rooms_room_id_seq'::regclass);


--
-- TOC entry 5031 (class 0 OID 16670)
-- Dependencies: 224
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.bookings VALUES (1, 1, 1, '2024-01-10', '2024-01-15', 'Предоплата внесена');
INSERT INTO public.bookings VALUES (2, 2, 3, '2024-01-12', '2024-01-18', 'Завтрак включен');
INSERT INTO public.bookings VALUES (3, 3, 2, '2024-01-14', '2024-01-16', 'Бизнес-клиент');
INSERT INTO public.bookings VALUES (4, 4, 5, '2024-01-15', '2024-01-20', 'С детьми');
INSERT INTO public.bookings VALUES (5, 5, 4, '2024-01-16', '2024-01-19', 'Командировка');


--
-- TOC entry 5027 (class 0 OID 16643)
-- Dependencies: 220
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.clients VALUES (1, 'Иванов', 'Алексей', 'Петрович', '4510 123456', 'Постоянный клиент');
INSERT INTO public.clients VALUES (2, 'Петрова', 'Мария', 'Сергеевна', '4511 654321', 'Требует повышенного комфорта');
INSERT INTO public.clients VALUES (3, 'Сидоров', 'Дмитрий', 'Иванович', '4512 789012', 'Бизнес-поездка');
INSERT INTO public.clients VALUES (4, 'Козлова', 'Елена', 'Викторовна', '4513 345678', 'Отдых с семьей');
INSERT INTO public.clients VALUES (5, 'Николаев', 'Андрей', 'Олегович', '4514 901234', 'Командировка');


--
-- TOC entry 5029 (class 0 OID 16656)
-- Dependencies: 222
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rooms VALUES (1, '101', 2, 'стандарт', 2500.00);
INSERT INTO public.rooms VALUES (2, '102', 2, 'стандарт', 2500.00);
INSERT INTO public.rooms VALUES (3, '201', 3, 'полулюкс', 4500.00);
INSERT INTO public.rooms VALUES (4, '202', 3, 'полулюкс', 4500.00);
INSERT INTO public.rooms VALUES (5, '301', 4, 'люкс', 7500.00);
INSERT INTO public.rooms VALUES (6, '302', 2, 'люкс', 8000.00);


--
-- TOC entry 5040 (class 0 OID 0)
-- Dependencies: 223
-- Name: bookings_booking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_booking_id_seq', 5, true);


--
-- TOC entry 5041 (class 0 OID 0)
-- Dependencies: 219
-- Name: clients_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_client_id_seq', 5, true);


--
-- TOC entry 5042 (class 0 OID 0)
-- Dependencies: 221
-- Name: rooms_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_room_id_seq', 6, true);


--
-- TOC entry 4876 (class 2606 OID 16679)
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (booking_id);


--
-- TOC entry 4870 (class 2606 OID 16654)
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (client_id);


--
-- TOC entry 4872 (class 2606 OID 16666)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (room_id);


--
-- TOC entry 4874 (class 2606 OID 16668)
-- Name: rooms rooms_room_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_room_number_key UNIQUE (room_number);


--
-- TOC entry 4877 (class 2606 OID 16680)
-- Name: bookings bookings_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);


--
-- TOC entry 4878 (class 2606 OID 16685)
-- Name: bookings bookings_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(room_id);


-- Completed on 2025-10-19 16:25:07

--
-- PostgreSQL database dump complete
--

\unrestrict V2xEiWEYi7wcnEU3eGsh73pL29iwVCnM5roKjgoe6iRUspNLOdwR2ZYMDue2hUb

