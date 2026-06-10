CREATE DATABASE RaizesDoNordeste;
GO

USE RaizesDoNordeste;
GO

CREATE TABLE PRODUTO(
    id_produto INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(100),
    preco DECIMAL(10,2)
);

INSERT INTO PRODUTO(nome, preco)
VALUES
('Cuscuz Completo',15.90),
('Tapioca de Queijo',12.50),
('Bolo de Macaxeira',8.00);
INSERT INTO PRODUTO (nome, preco)
VALUES
('Rapadura Tradicional', 8.90),
('Bolo de Rolo', 24.90),
('Queijo Coalho', 18.50),
('Manteiga de Garrafa', 22.90),
('Cuscuz Nordestino', 6.50),
('Carne de Sol', 49.90),
('Doce de Leite Artesanal', 15.90),
('Castanha de Caju', 12.90),
('Pimenta Nordestina', 9.90),
('Mel de Engenho', 19.90);

CREATE TABLE CLIENTE (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20)
);

INSERT INTO CLIENTE (nome, email, telefone)
VALUES
('Samuel Vitor', 'samuel@gmail.com', '3198982-3383');
INSERT INTO CLIENTE (nome, email, telefone)
VALUES
('João Pedro Silva', 'joao@email.com', '31999887766'),
('Maria Eduarda Souza', 'maria@email.com', '31988776655'),
('Lucas Henrique Santos', 'lucas@email.com', '31977665544'),
('Ana Clara Oliveira', 'ana@email.com', '31966554433'),
('Gabriel Costa Lima', 'gabriel@email.com', '31955443322');

CREATE TABLE PEDIDO (
    id_pedido INT IDENTITY(1,1) PRIMARY KEY,
    id_cliente INT NOT NULL,
    data_pedido DATETIME DEFAULT GETDATE(),
    status VARCHAR(30) DEFAULT 'PENDENTE',
    valor_total DECIMAL(10,2),

    FOREIGN KEY (id_cliente)
    REFERENCES CLIENTE(id_cliente)
);

CREATE TABLE PAGAMENTO (
    id_pagamento INT IDENTITY(1,1) PRIMARY KEY,
    id_pedido INT NOT NULL,
    status VARCHAR(20),
    data_pagamento DATETIME DEFAULT GETDATE(),
    metodo_pagamento VARCHAR(30),

    FOREIGN KEY (id_pedido)
    REFERENCES PEDIDO(id_pedido)
);

CREATE TABLE USUARIO (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(100)
);

INSERT INTO USUARIO (nome, email, senha)
VALUES
('Samuel Vitor', 'samuel@email.com', '123456'),
('Camila', 'camila@email.com', '654321');
