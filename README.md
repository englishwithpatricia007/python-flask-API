# E-commerce Flask API

Este projeto é uma API de e-commerce desenvolvida com Flask, utilizando autenticação de usuários, gerenciamento de produtos e carrinho de compras.

## Bibliotecas Utilizadas

- **Flask**: Framework principal para criação da API web.
- **Flask-SQLAlchemy**: ORM para integração e manipulação do banco de dados SQLite.
- **Flask-Login**: Gerenciamento de autenticação e sessão de usuários.
- **Flask-Cors**: Permite requisições de diferentes origens (Cross-Origin Resource Sharing).
- **Werkzeug**: Utilitário para WSGI e segurança de senhas (dependência do Flask).

## Como rodar

1. Instale as dependências:

```sh
   pip install -r requirements.txt
```

2. Execute a aplicação:

```sh
   python application.py
```

## Endpoints

### Autenticação de Usuário

- `POST /login`  
  Login do usuário.  
  **Body:** `{ "username": "usuario", "password": "senha" }`

- `POST /logout`  
  Logout do usuário autenticado.

### Produtos

- `GET /api/products`  
  Lista todos os produtos.

- `GET /api/products/<product_id>`  
  Detalhes de um produto específico.

- `POST /api/products/add`  
  Adiciona um novo produto (requer login).  
  **Body:** `{ "name": "nome", "price": valor, "description": "desc" }`

- `PUT /api/products/update/<product_id>`  
  Atualiza um produto existente (requer login).

- `DELETE /api/products/delete/<product_id>`  
  Remove um produto (requer login).

### Carrinho

- `POST /api/cart/add/<product_id>`  
  Adiciona um produto ao carrinho do usuário autenticado.

- `DELETE /api/cart/remove/<product_id>`  
  Remove um produto do carrinho.

- `GET /api/cart`  
  Lista os produtos do carrinho do usuário autenticado.

- `POST /api/cart/checkout`  
  Finaliza a compra (esvazia o carrinho).

---

**Banco de dados:**  
O projeto utiliza SQLite, com o arquivo localizado em `instance/ecommerce.db`.

Para criar um usuário:

```sh
flask shell
user = User(username="admin", password="123")
db.session.add(user)
exit()
```

---
