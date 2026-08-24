--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)
-- Dumped by pg_dump version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: relations_minified; Type: TABLE; Schema: public; Owner: metricsuser
--

CREATE TABLE public.relations_minified (
    ecosystem character varying,
    package character varying,
    package_version public.semver,
    dependency character varying,
    dependency_constraint character varying,
    dependency_version public.semver,
    dependency_highest_version character varying,
    interval_start timestamp without time zone,
    interval_end timestamp without time zone,
    outdated boolean,
    is_regular boolean,
    vulnerable boolean DEFAULT false,
    constraint_type text DEFAULT 'unclassified'::text,
    age_of_interval numeric,
    expo_weight numeric,
    inverse_weight numeric
);


ALTER TABLE public.relations_minified OWNER TO metricsuser;

--
-- Name: idx_relations_minified_age_of_interval; Type: INDEX; Schema: public; Owner: metricsuser
--

CREATE INDEX idx_relations_minified_age_of_interval ON public.relations_minified USING btree (age_of_interval);


--
-- Name: idx_relations_minified_expo_weight; Type: INDEX; Schema: public; Owner: metricsuser
--

CREATE INDEX idx_relations_minified_expo_weight ON public.relations_minified USING btree (expo_weight);


--
-- Name: idx_relations_minified_inverse_weight; Type: INDEX; Schema: public; Owner: metricsuser
--

CREATE INDEX idx_relations_minified_inverse_weight ON public.relations_minified USING btree (inverse_weight);


--
-- Name: relations_index_4; Type: INDEX; Schema: public; Owner: metricsuser
--

CREATE INDEX relations_index_4 ON public.relations_minified USING btree (constraint_type);


--
-- Name: relations_minified_index; Type: INDEX; Schema: public; Owner: metricsuser
--

CREATE INDEX relations_minified_index ON public.relations_minified USING btree (ecosystem, dependency, dependency_version, interval_start);


--
-- Name: relations_minified_index_2; Type: INDEX; Schema: public; Owner: metricsuser
--

CREATE INDEX relations_minified_index_2 ON public.relations_minified USING btree (ecosystem, package, dependency, outdated, is_regular, vulnerable);


--
-- Name: relations_minified_index_3; Type: INDEX; Schema: public; Owner: metricsuser
--

CREATE INDEX relations_minified_index_3 ON public.relations_minified USING btree (dependency_constraint);


--
-- PostgreSQL database dump complete
--

