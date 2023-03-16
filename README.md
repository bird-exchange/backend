## Installation

```bash
git clone https://github.com/bird-exchange/backend.git
```

## Running

### One-time action (if not poetry)

```bash
pip install poetry
poetry config virtualenvs.in-project true
```

### Install dependecies

```bash
poetry init
poetry install
```

### Configure environment

Use `.env.default` to create `.env`

### Start database
```bash
make db.run
```

### Start minio
```bash
make minio.run
```

### Start application
```bash
make app.run
```
