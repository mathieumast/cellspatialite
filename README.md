# Prerequisites
- python
- pip
- virtualenv


# Install dependencies in virtualenv
```sh
~ virtualenv venv --no-site-packages
~ source venv/bin/activate
~ pip install -r requirements.txt
~ deactivate
```

# Run cellspatialite with virtalenv
```sh
~ source venv/bin/activate
~ python cellspatialite.py
~ deactivate
```

# Install cellspatialite
```sh
~ sudo python setup.py install
```
