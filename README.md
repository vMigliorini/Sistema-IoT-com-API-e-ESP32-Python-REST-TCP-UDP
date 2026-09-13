# Sistema IoT com API e ESP32

Sistema cliente-servidor desenvolvido em **Python**, utilizando **Flask**, banco de dados e comunicação em tempo real, com o objetivo de integrar dispositivos **ESP32** a uma aplicação centralizada para envio, processamento e visualização de dados.

> **Status:** Em desenvolvimento 🚧
> A camada de software do servidor e a estrutura para gerenciamento dos dispositivos já estão sendo desenvolvidas. A implementação do firmware e da comunicação física com o ESP32 será realizada em uma etapa posterior.

---

## 📌 Sobre o projeto

O projeto propõe uma arquitetura para integração entre dispositivos IoT e uma aplicação web.

A aplicação atua como camada central do sistema, sendo responsável por gerenciar usuários, dispositivos ESP32, salas de comunicação, mensagens e leituras provenientes dos dispositivos.

A arquitetura foi planejada para permitir que, futuramente, dispositivos ESP32 possam se conectar ao servidor, enviar dados de sensores e receber informações ou comandos através da infraestrutura disponibilizada pela aplicação.

Além da comunicação com dispositivos IoT, o projeto conta com recursos de comunicação em tempo real, permitindo trabalhar com eventos e atualização de informações sem a necessidade de requisições constantes por parte do cliente.

---

## 🎯 Objetivos

O projeto tem como principais objetivos:

* Desenvolver uma API utilizando Python e Flask;
* Criar uma estrutura para gerenciamento de dispositivos IoT;
* Permitir o cadastro e gerenciamento de dispositivos ESP32;
* Armazenar leituras provenientes dos dispositivos;
* Implementar comunicação em tempo real;
* Gerenciar usuários e salas de comunicação;
* Preparar a integração entre o servidor e dispositivos ESP32;
* Explorar diferentes mecanismos de comunicação utilizados em sistemas IoT;
* Criar uma arquitetura extensível para futuras funcionalidades.

---

## 🏗️ Arquitetura

A arquitetura atual pode ser representada de forma simplificada como:

```text
                         ┌──────────────────────┐
                         │     Cliente Web      │
                         │                      │
                         │ Interface / Usuário  │
                         └──────────┬───────────┘
                                    │
                           HTTP / Socket.IO
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │       Flask Server        │
                    │                           │
                    │  API / Views / Eventos   │
                    └─────────────┬─────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌─────────────┐     ┌──────────────┐    ┌─────────────┐
       │   Usuários  │     │  Dispositivos│    │    Salas    │
       │             │     │    ESP32     │    │             │
       └─────────────┘     └──────┬───────┘    └─────────────┘
                                  │
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Futuro ESP32 /  │
                         │ Sensores IoT    │
                         └─────────────────┘

                         ┌─────────────────┐
                         │    PostgreSQL   │
                         │   / Neon DB     │
                         └─────────────────┘
```

A integração com o ESP32 ainda não está implementada no estado atual do projeto.

---

## 🛠️ Tecnologias

### Backend

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-Bcrypt**
* **Flask-CORS**
* **Flask-SocketIO**
* **python-dotenv**
* **Eventlet**

### Banco de dados

* **PostgreSQL**
* **Neon Database**

### Comunicação

* **HTTP / REST**
* **WebSocket / Socket.IO**
* **TCP / UDP** — previstos no escopo de comunicação do projeto

### Hardware

* **ESP32** — integração prevista para a próxima etapa do projeto

---

## 📂 Estrutura do projeto

A estrutura atual do repositório está organizada da seguinte forma:

```text
Sistema-IoT-com-API-e-ESP32-Python-REST-TCP-UDP/
│
├── services/
│
├── static/
│
├── templates/
│
├── main.py
├── models.py
├── views.py
├── extensions.py
├── socket_events.py
│
├── .gitignore
└── README.md
```

### `main.py`

Arquivo responsável pela inicialização da aplicação Flask.

Entre suas responsabilidades estão:

* Inicialização do Flask;
* Configuração do CORS;
* Inicialização do SQLAlchemy;
* Inicialização do Bcrypt;
* Inicialização do Socket.IO;
* Carregamento das variáveis de ambiente;
* Registro das rotas;
* Criação das tabelas do banco de dados.

### `models.py`

Define os modelos utilizados pela aplicação e suas relações com o banco de dados.

Entre os principais modelos estão:

* `Usuario`
* `UsuarioChat`
* `EspDevice`
* `ChatRoom`
* `RoomDevice`
* `ChatMessage`
* `LeituraESP`

O modelo `LeituraESP`, por exemplo, permite associar uma leitura a um dispositivo, armazenando o tipo, valor e momento em que a leitura foi registrada.

---

## 👥 Usuários

O sistema possui uma estrutura de usuários com informações como:

* ID;
* Nome;
* E-mail;
* Cargo;
* Senha armazenada em formato de hash.

O projeto também possui diferentes categorias de cargos, incluindo:

* Engenheiro Civil;
* Engenheiro de Software;
* Engenheiro de Produção;
* Psicólogo;
* Gerente de Projetos.

---

## 📡 Dispositivos ESP32

Os dispositivos IoT são representados pela entidade `EspDevice`.

Cada dispositivo possui, atualmente, informações como:

```text
ID
Nome
Token
```

Além disso, existe uma relação entre os dispositivos e suas respectivas leituras.

A estrutura foi criada para permitir que, futuramente, um ESP32 seja identificado pelo servidor e possa enviar dados de sensores para serem armazenados e processados.

### ⚠️ Integração ainda não implementada

Apesar de existir a estrutura de banco de dados para representar dispositivos e suas leituras, a comunicação física com o ESP32 ainda está em desenvolvimento.

Portanto, nesta versão:

> **O ESP32 ainda não realiza efetivamente o envio de dados para o servidor.**

Essa integração será adicionada em uma etapa futura.

---

## 📊 Leituras IoT

O modelo `LeituraESP` foi criado para armazenar dados provenientes dos dispositivos.

Cada leitura possui:

| Campo       | Descrição                               |
| ----------- | --------------------------------------- |
| `id`        | Identificador da leitura                |
| `device_id` | Dispositivo responsável pela leitura    |
| `tipo`      | Tipo da informação coletada             |
| `valor`     | Valor da leitura                        |
| `timestamp` | Momento em que a leitura foi registrada |

Exemplo conceitual:

```json
{
    "device_id": 1,
    "tipo": "temperatura",
    "valor": 25.7
}
```

A definição final do formato das mensagens enviadas pelo ESP32 será estabelecida durante a implementação da camada IoT.

---

## 💬 Comunicação em tempo real

O projeto utiliza **Flask-SocketIO** para fornecer comunicação em tempo real.

Essa infraestrutura permite trabalhar com eventos entre o servidor e os clientes conectados, sendo especialmente útil para funcionalidades como:

* Mensagens;
* Atualização de salas;
* Estado de conexão;
* Atualizações de dispositivos;
* Futuras notificações de leituras IoT.

A utilização de eventos em tempo real também prepara o sistema para receber dados dos dispositivos IoT e refletir essas informações na aplicação sem depender exclusivamente de requisições periódicas.

---

## 🏠 Salas

O sistema possui o conceito de **salas**, representadas pelo modelo `ChatRoom`.

Cada sala pode possuir:

* Nome;
* Status;
* Data de criação;
* Usuários;
* Dispositivos associados;
* Mensagens.

Os dispositivos ESP32 podem ser relacionados às salas através da entidade `RoomDevice`.

Isso permite estruturar o sistema para cenários em que diferentes dispositivos pertencem a diferentes ambientes ou grupos.

---

## 🔐 Configuração

As configurações sensíveis da aplicação são obtidas através de variáveis de ambiente.

Entre elas estão:

```env
SECRET_KEY=
NEON_DB_URI=
FRONTEND_URL=
```

Recomenda-se utilizar um arquivo `.env.local` ou `.env` durante o desenvolvimento.

### Exemplo

```env
SECRET_KEY=sua_chave_secreta
NEON_DB_URI=sua_connection_string
FRONTEND_URL=http://localhost:3000
```

> **Nunca versione credenciais, tokens ou chaves privadas no repositório.**

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/vMigliorini/Sistema-IoT-com-API-e-ESP32-Python-REST-TCP-UDP.git
```

Entre na pasta:

```bash
cd Sistema-IoT-com-API-e-ESP32-Python-REST-TCP-UDP
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install flask
pip install flask-socketio
pip install flask-sqlalchemy
pip install flask-bcrypt
pip install flask-cors
pip install psycopg2-binary
pip install python-dotenv
pip install eventlet
pip install "python-socketio[client]"
```

Essas são as dependências atualmente documentadas no repositório.

---

## ▶️ Executando o projeto

Depois de configurar as variáveis de ambiente, execute:

```bash
python main.py
```

O servidor Flask será iniciado utilizando o Socket.IO.

Durante o desenvolvimento, o projeto está configurado para executar com:

```python
socketio.run(app, debug=True)
```

---

## 🔄 Fluxo previsto para a integração IoT

Quando a implementação do ESP32 for adicionada, o fluxo esperado será semelhante a:

```text
┌──────────────┐
│    ESP32     │
│              │
│   Sensores   │
└──────┬───────┘
       │
       │ Dados
       ▼
┌──────────────────────┐
│ Comunicação IoT      │
│ REST / TCP / UDP     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Flask API       │
│                      │
│ Validação / Process. │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      PostgreSQL      │
│                      │
│     Leituras ESP     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Aplicação Web     │
│                      │
│ Visualização / Dados │
└──────────────────────┘
```

---

## 🔌 Protocolos de comunicação

Um dos objetivos do projeto é explorar diferentes formas de comunicação utilizadas em sistemas distribuídos e IoT.

### REST

A API REST será utilizada como uma das formas de comunicação entre o dispositivo e o servidor.

Uma possível requisição futura poderá seguir o padrão:

```http
POST /api/device/readings
Content-Type: application/json
```

Com um payload semelhante a:

```json
{
    "device_id": 1,
    "tipo": "temperatura",
    "valor": 25.7
}
```

> A rota e o formato definitivo serão definidos durante a implementação da comunicação com o ESP32.

### TCP

O TCP poderá ser utilizado quando for necessária uma comunicação orientada à conexão e com maior garantia na entrega dos dados.

### UDP

O UDP poderá ser utilizado em cenários nos quais baixa latência e menor overhead sejam mais importantes do que a garantia de entrega de cada pacote.

---

## 🧪 Estado atual

| Componente                   | Status                |
| ---------------------------- | --------------------- |
| Estrutura Flask              | ✅ Implementado        |
| Banco de dados               | ✅ Implementado        |
| Modelos de usuários          | ✅ Implementado        |
| Modelo de dispositivos ESP32 | ✅ Implementado        |
| Modelo de leituras IoT       | ✅ Estruturado         |
| Salas                        | ✅ Implementado        |
| Mensagens                    | ✅ Estruturado         |
| Socket.IO                    | ✅ Implementado        |
| CORS                         | ✅ Configurado         |
| Autenticação/segurança       | 🚧 Em desenvolvimento |
| Comunicação REST com ESP32   | 🚧 Futuro             |
| Comunicação TCP              | 🚧 Futuro             |
| Comunicação UDP              | 🚧 Futuro             |
| Firmware ESP32               | 🚧 Futuro             |
| Sensores físicos             | 🚧 Futuro             |
| Integração completa IoT      | 🚧 Futuro             |

---

## 🗺️ Roadmap

### Backend

* [x] Estrutura inicial da aplicação Flask
* [x] Configuração do banco de dados
* [x] Modelagem de usuários
* [x] Modelagem de dispositivos
* [x] Modelagem de leituras
* [x] Estrutura de salas
* [x] Comunicação em tempo real com Socket.IO
* [ ] Refinamento da API
* [ ] Documentação dos endpoints
* [ ] Testes automatizados

### IoT

* [ ] Definir protocolo principal de comunicação
* [ ] Desenvolver firmware para ESP32
* [ ] Implementar conexão Wi-Fi
* [ ] Implementar autenticação do dispositivo
* [ ] Implementar envio de leituras
* [ ] Implementar comunicação REST
* [ ] Implementar comunicação TCP
* [ ] Implementar comunicação UDP
* [ ] Validar comunicação com o servidor
* [ ] Realizar testes com sensores físicos

### Integração

* [ ] Conectar ESP32 à API
* [ ] Persistir leituras reais
* [ ] Exibir dados em tempo real
* [ ] Monitorar status dos dispositivos
* [ ] Implementar tratamento de dispositivos offline
* [ ] Implementar mecanismos de segurança para comunicação IoT

---

## 🔒 Segurança

Como o projeto envolve dispositivos IoT e comunicação de rede, a segurança será considerada uma etapa importante da implementação.

Entre os mecanismos planejados estão:

* Autenticação dos dispositivos;
* Utilização de tokens;
* Proteção das credenciais;
* Validação dos dados recebidos;
* Controle de acesso;
* Comunicação segura;
* Tratamento de dispositivos não autorizados.

O modelo `EspDevice` já possui um campo destinado ao token do dispositivo, que poderá ser utilizado como parte do mecanismo de autenticação da futura camada IoT.

---

## 📚 Conceitos abordados

Este projeto explora conceitos relacionados a:

* Internet das Coisas (IoT);
* Sistemas cliente-servidor;
* APIs REST;
* Comunicação TCP/IP;
* Comunicação UDP;
* WebSockets;
* Comunicação em tempo real;
* Banco de dados relacionais;
* Desenvolvimento backend;
* Autenticação;
* Modelagem de dados;
* Sistemas distribuídos;
* Dispositivos embarcados;
* ESP32.

---

## 🚧 Projeto em desenvolvimento

Este projeto encontra-se em desenvolvimento.

A estrutura atual representa principalmente a **camada de software e backend** da solução. A implementação do dispositivo IoT, firmware do ESP32, sensores e comunicação efetiva entre o hardware e o servidor ainda será desenvolvida.

Portanto, a existência dos modelos `EspDevice` e `LeituraESP` representa a preparação da aplicação para a futura integração IoT, e não significa que o dispositivo físico já esteja integrado nesta versão.

---

## 📄 Licença

A licença do projeto ainda não foi definida.

---

## 👨‍💻 Autor

Desenvolvido por **vMigliorini**.

Repositório:

[Sistema IoT com API e ESP32 — GitHub](https://github.com/vMigliorini/Sistema-IoT-com-API-e-ESP32-Python-REST-TCP-UDP?utm_source=chatgpt.com)
