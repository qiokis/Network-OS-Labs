--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

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
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    address character varying(50) NOT NULL
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_id_seq OWNER TO postgres;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id bigint NOT NULL,
    number integer NOT NULL,
    date date NOT NULL,
    product_id integer NOT NULL,
    received integer NOT NULL,
    customer_id integer NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id bigint NOT NULL,
    product_name character varying(50) NOT NULL,
    brand_name character varying(50) NOT NULL,
    model_name character varying(50) NOT NULL,
    description character varying(50),
    price numeric,
    remains integer
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (id, name, address) FROM stdin;
35	╨Ч╨Р╨Ю ╨Я╨╡╤В╤А╨╛╨▓-╨Т╨╛╨┤╨║╨╕╨╜ ╨╕ ╤Б╤Л╨╜╨╛╨▓╤М╤П	╨│. ╨Ш╤А╨║╤Г╤В╤Б╨║ ╤Г╨╗. ╨Ф╨╛╨╜╤Б╨║╨░╤П 57
36	╨и╤Г╤И╨░╤А╨╕╨╜ ╤Н╨╜╨┤ ╨║╨╛╨╝╨┐╨░╨╜╨╕	╨│. ╨Ш╤А╨║╤Г╤В╤Б╨║ ╤Г╨╗. ╨С╨░╤В╨░╤А╨╡╨╣╨╜╨░╤П 48
37	╨Ю╨Р╨Ю ╨Ш╨╜╨║╨╗╤О╨╖╨╕╤П	╨│. ╨Ш╤А╨║╤Г╤В╤Б╨║ ╤Г╨╗. ╨а╨░╨▒╨╛╤З╨╡╨│╨╛ ╤И╤В╨░╨▒╨░ 75
39	╨Ч╨Р╨Ю ╨Р╤Д╤А╨╛╨┤╨╕╤В╨░	╨│. ╨Ш╤А╨║╤Г╤В╤Б╨║ ╤Г╨╗. ╨Р╨╗╨╡╨║╤Б╨░╨╜╨┤╤А╨░ ╨Э╨╡╨▓╤Б╨║╨╛╨│╨╛ 39
40	asda	htthf
31	╨з╨Я ╨Р╨┤╨░╨╝╨░ ╨У╨╛╤А╨╕╨┤╨╖╨╡	╨│. ╨Ш╤А╨║╤Г╤В╤Б╨║ ╤Г╨╗. ╨в╤А╨╕╨╗╨╕╤Б╤Б╨╡╤А╨░ 15
29	╨б╨╕╨┤╨╛╤А╨╛╨▓ ╨╕╨╜╨┤╨░╤Б╤В╤А╨╕╨╖	╨│. ╨Ш╤А╨║╤Г╤В╤Б╨║ ╤Г╨╗. ╨б╨╛╨▓╨╡╤В╤Б╨║╨░╤П ╨┤. 125 ╨╛╤Д. 17
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, number, date, product_id, received, customer_id) FROM stdin;
129	6	2010-01-08	4	2	29
130	6	2010-01-08	6	2	29
133	7	2010-01-08	5	5	31
134	7	2010-01-08	4	5	31
135	7	2010-01-08	6	5	31
138	8	2010-01-08	5	8	36
140	8	2010-01-08	6	3	36
143	9	2010-01-08	5	3	39
144	9	2010-01-08	4	5	39
145	9	2010-01-08	6	8	39
148	10	2010-01-08	5	30	37
149	10	2010-01-08	4	25	37
150	10	2010-01-08	6	25	37
157	12	2021-02-25	4	8	31
158	13	2021-02-27	5	6	39
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, product_name, brand_name, model_name, description, price, remains) FROM stdin;
6	╨Ь╨╛╨╖╨│╨╕	╨б╨╛╨╜╨╕	DDR-1024.56	╨Ь╤А╨░╨║	932.78	610
7	╨Ъdas	╨Ш╨╜╤В╨╡╨╗12	ad	asd	454.52	0
4	╨Ь╨░╤В╤М	╨б╨╕╨╝╨╡╨╜╤Б	PHJ-386	╨Ю╨▒╨░╨╗╨┤╨╡╨╜╨╜╤Л╨╡	2560.25	608
5	╨Ъ╤Г╨╗╨╡╤А	╨Ш╨╜╤В╨╡╨╗	╨Т╨Ч╨Я-321	╨Т╨░╤Й╨╡	454.50	243
\.


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_id_seq', 8, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 34, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 28, true);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

