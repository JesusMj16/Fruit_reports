-- We create the table compradores whit id and name
CREATE TABLE compradores (
    id SERIAL PRIMARY KEY,
    nombre_comprador VARCHAR(70) NOT NULL
);
-- In this block of code im create the table fruits with the specifications work in class
CREATE TABLE frutas(
    id SERIAL PRIMARY KEY,
    nombre_fruta VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2)
);
CREATE TABLE compras(
    id_compra SERIAL PRIMARY KEY,
    id_fruta INTEGER REFERENCES frutas(id),
    id_comprador INTEGER REFERENCES compradores(id)
);
