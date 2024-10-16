-- Table: public.course

-- DROP TABLE IF EXISTS public.course;

CREATE TABLE IF NOT EXISTS public.course
(
    courseid integer NOT NULL,
    title character varying(100) COLLATE pg_catalog."default" NOT NULL,
    credits integer NOT NULL,
    departmentid integer NOT NULL,
    CONSTRAINT course_pkey PRIMARY KEY (courseid),
    CONSTRAINT fk_course_department FOREIGN KEY (departmentid)
        REFERENCES public.department (departmentid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.course
    OWNER to postgres;


-- Table: public.courseinstructor

-- DROP TABLE IF EXISTS public.courseinstructor;

CREATE TABLE IF NOT EXISTS public.courseinstructor
(
    courseid integer NOT NULL,
    personid integer NOT NULL,
    CONSTRAINT courseinstructor_pkey PRIMARY KEY (courseid, personid),
    CONSTRAINT fk_courseinstructor_course FOREIGN KEY (courseid)
        REFERENCES public.course (courseid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_courseinstructor_person FOREIGN KEY (personid)
        REFERENCES public.person (personid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.courseinstructor
    OWNER to postgres;

-- Table: public.department

-- DROP TABLE IF EXISTS public.department;

CREATE TABLE IF NOT EXISTS public.department
(
    departmentid integer NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    budget numeric NOT NULL,
    startdate timestamp without time zone NOT NULL,
    administrator integer,
    CONSTRAINT department_pkey PRIMARY KEY (departmentid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.department
    OWNER to postgres;

-- Table: public.officeassignment

-- DROP TABLE IF EXISTS public.officeassignment;

CREATE TABLE IF NOT EXISTS public.officeassignment
(
    instructorid integer NOT NULL,
    location character varying(50) COLLATE pg_catalog."default" NOT NULL,
    "timestamp" bytea NOT NULL,
    CONSTRAINT officeassignment_pkey PRIMARY KEY (instructorid),
    CONSTRAINT fk_officeassignment_person FOREIGN KEY (instructorid)
        REFERENCES public.person (personid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.officeassignment
    OWNER to postgres;

-- Table: public.onlinecourse

-- DROP TABLE IF EXISTS public.onlinecourse;

CREATE TABLE IF NOT EXISTS public.onlinecourse
(
    courseid integer NOT NULL,
    url character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT onlinecourse_pkey PRIMARY KEY (courseid),
    CONSTRAINT fk_onlinecourse_course FOREIGN KEY (courseid)
        REFERENCES public.course (courseid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.onlinecourse
    OWNER to postgres;

-- Table: public.onsitecourse

-- DROP TABLE IF EXISTS public.onsitecourse;

CREATE TABLE IF NOT EXISTS public.onsitecourse
(
    courseid integer NOT NULL,
    location character varying(50) COLLATE pg_catalog."default" NOT NULL,
    days character varying(50) COLLATE pg_catalog."default" NOT NULL,
    "time" time without time zone NOT NULL,
    CONSTRAINT onsitecourse_pkey PRIMARY KEY (courseid),
    CONSTRAINT fk_onsitecourse_course FOREIGN KEY (courseid)
        REFERENCES public.course (courseid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.onsitecourse
    OWNER to postgres;

-- Table: public.person

-- DROP TABLE IF EXISTS public.person;

CREATE TABLE IF NOT EXISTS public.person
(
    personid integer NOT NULL DEFAULT nextval('person_personid_seq'::regclass),
    lastname character varying(50) COLLATE pg_catalog."default" NOT NULL,
    firstname character varying(50) COLLATE pg_catalog."default" NOT NULL,
    hiredate timestamp without time zone,
    enrollmentdate timestamp without time zone,
    discriminator character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_pkey PRIMARY KEY (personid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.person
    OWNER to postgres;

-- Table: public.studentgrade

-- DROP TABLE IF EXISTS public.studentgrade;

CREATE TABLE IF NOT EXISTS public.studentgrade
(
    enrollmentid integer NOT NULL DEFAULT nextval('studentgrade_enrollmentid_seq'::regclass),
    courseid integer NOT NULL,
    studentid integer NOT NULL,
    grade numeric(3,2),
    CONSTRAINT studentgrade_pkey PRIMARY KEY (enrollmentid),
    CONSTRAINT fk_studentgrade_course FOREIGN KEY (courseid)
        REFERENCES public.course (courseid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_studentgrade_student FOREIGN KEY (studentid)
        REFERENCES public.person (personid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.studentgrade
    OWNER to postgres;