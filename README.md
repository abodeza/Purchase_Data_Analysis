# Purchase Data Analysis

Analysis and categorization of purchase order data.

***Will be updated soon***
<!-- ## Description



## Demo
Link + screenshots

## Getting Started

### Prerequisites

* Used python 3.10
* Required libraries (listed in requirements.txt)

### Installation

```bash

```

### Configuration

```
API_URL = "http://localhost:8000"
```

## Running locally

```
REM ----- Setup -----
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

REM ----- Disambiguation data for Camel-tools -----
camel_data -i light

REM Create .streamlit folder
mkdir .streamlit

REM Copy example files - FILL IN YOUR SECRETS
copy .env.example .env
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

REM Delete example files to keep things clean
del .env.example
del .streamlit\secrets.toml.example

REM ----- Run Backend -----
uvicorn backend.api:app --reload --port 8000

REM ----- Run Frontend -----
streamlit run streamlit_app.py
```


## Project Structure

Placeholder

```
myproject/
├── __init__.py     # Makes myproject a Python package
├── app.py          # Main application entry point
├── config.py       # Configuration settings
├── models/         # Data models
│   ├── __init__.py
│   └── user.py
├── utils/          # Helper functions
│   ├── __init__.py
│   └── helpers.py
├── services/       # Business logic
│   ├── __init__.py
│   └── data_service.py
└── tests/          # Unit tests
    ├── __init__.py
    └── test_models.py
```


## [Optional] API Reference

Placeholder

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/users` | GET | Retrieve users list | `limit`, `offset` |
| `/api/users/:id` | GET | Get user by ID | `id` (required) |

## [Optional] Contributing

Guidelines for contributors:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request -->

## Author

Abdullah Alzahrani
- Email: [abdullah.alzahrani.p@gmail.com](mailto:abdullah.alzahrani.p@gmail.com)
- GitHub: [@abodeza](https://github.com/abodeza)
- LinkedIn: [a-a-alzahrani](https://linkedin.com/in/a-a-alzahrani)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
