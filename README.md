# technical-test-ahtglobal

## 🎯 Project's main features
- CRUD operations 
- Data validation for unique identifiers
- Error handling and logging
- Unit + integration tests with pytest
- Docker containerization
- SQLAlchemy ORM integration
- Blueprint-based routing

## 🏗 Project Structure
```
technical-test-ahtglobal/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── inventory.py         # Routes and business logic
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database configuration
│   ├── static/
│   │   ├── css/             # Bootstrap CSS dist files
│   │   ├── js/              # Bootstrap js dist files
|   |   └── images/          # Images folder
│   └── templates/
│       ├── base.html        # Base template
│       ├── 404.html         # Error page
│       └── crud/
│           ├── list.html    # Product listing
│           ├── create.html  # Add product form
│           ├── edit.html    # Edit product form
│           └── delete.html  # Delete confirmation
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration
│   └── test_inventory.py   # Test suite
├── Dockerfile              # Container definition
├── docker-compose.yml      # Container orchestration
├── pyproject.toml          # Poetry dependencies
├── poetry.lock             # Locked dependencies
└── README.md               # Project documentation
```

## 🛠 Tech Stack
- **Framework**: Flask
- **Database**: MySQL + SQLAlchemy
- **Testing**: pytest + unittest.mock
- **Dependencies**: Poetry
- **Containerization**: Docker + Docker Compose
- **Logging**: Python's built-in logging module

## 🚀 Getting Started
Spinning up the containers with:
```
docker-compose up --build -d
```

## 🧪 Running Tests
```bash
# Run all tests
docker exec technical-test-ahtglobal-web-1 poetry run pytest tests/ -v

# Run specific test file
docker exec technical-test-ahtglobal-web-1 poetry run pytest tests/test_inventory.py -v
```

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all devices |
| GET/POST | `/add` | Add new device |
| GET/POST | `/edit/<id>` | Edit existing device |
| GET/POST | `/delete/<id>` | Delete device |

## 🔒 Data Validation
- Unique MAC addresses
- Unique serial numbers
- Proper error handling for duplicates

### Product Listing
![Product Listing](https://i.imgur.com/cUl2CcM.png)
*Main interface showing the list of devices with actions for edit and delete*
### Edit Product
![Edit Product](https://i.imgur.com/P7u2A9e.png)
*Edit interface for updating device information with form validation*
### Delete Confirmation
![Delete Product](https://i.imgur.com/6oAMYax.png)
*Safety confirmation dialog before removing a device from inventory*
### Error Handling
![404 Not Found](https://i.imgur.com/hnNN47T.png)
*Custom 404 error page when attempting to access non-existent devices*

## 👤 Author
Jean Paul Sierra Boom