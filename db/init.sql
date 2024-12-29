-- Tabla: user
CREATE TABLE IF NOT EXISTS public."user" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Tabla: subject
CREATE TABLE IF NOT EXISTS public."subject" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by INT,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES "user"(id) ON DELETE SET NULL
);

-- Tabla: node
CREATE TABLE IF NOT EXISTS public."node" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by INT,
    name VARCHAR(255) NOT NULL,
    subject_id INT,
    parent_id INT,
    FOREIGN KEY (created_by) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES node(id) ON DELETE CASCADE
);

-- Tabla: question
CREATE TABLE IF NOT EXISTS public."question" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by INT,
    title VARCHAR(255) NOT NULL,
    difficulty INT NOT NULL,
    "time" INT NOT NULL,
    parametrized BOOLEAN NOT NULL DEFAULT FALSE,
    active BOOLEAN NOT NULL,
    subject_id INT,
    "type" VARCHAR(50) CHECK ("type" IN ('test', 'desarrollo')) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(id) ON DELETE CASCADE
);

-- Tabla de asociación node_question_association
CREATE TABLE IF NOT EXISTS public."node_question_association" (
    node_id INT,
    question_id INT,
    PRIMARY KEY (node_id, question_id),
    FOREIGN KEY (node_id) REFERENCES node(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
);

-- Tabla: answer
CREATE TABLE IF NOT EXISTS public."answer" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by INT,
    body TEXT NOT NULL,
    points INT CHECK (points >= -100 AND points <= 100) NOT NULL,
    question_id INT,
    FOREIGN KEY (created_by) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
);

-- Tabla: question_parameter
CREATE TABLE IF NOT EXISTS public."question_parameter" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by INT,
    question_id INT,
    "value" VARCHAR(255) NOT NULL,
    "position" INT NOT NULL,
    "group" INT NOT NULL,
    FOREIGN KEY (created_by) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
);

-- Tabla: exam
CREATE TABLE IF NOT EXISTS public."exam" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by INT,
    title VARCHAR(255) NOT NULL,
    subject_id INT,
    created_on TIMESTAMP NOT NULL,
    FOREIGN KEY (created_by) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(id) ON DELETE CASCADE
);

-- Tabla de asociación exam_question_association
CREATE TABLE IF NOT EXISTS public."exam_question_association" (
    question_id INT,
    exam_id INT,
    section_id INT,
    "group" INT,
    PRIMARY KEY (question_id, exam_id),
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exam(id) ON DELETE CASCADE
);

-- Tabla: result
CREATE TABLE IF NOT EXISTS public."result" (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by INT,
    question_id INT,
    exam_id INT,
    "time" VARCHAR(255) NOT NULL,
    taker VARCHAR(255) NOT NULL,
    points INT CHECK (points >= -100 AND points <= 100) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exam(id) ON DELETE CASCADE
);
