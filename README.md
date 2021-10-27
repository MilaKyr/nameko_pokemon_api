# Pokemon API with command line interface 

Make sure the requirements have been installed:
`pip install -r requirements.txt`

To run:
```buildoutcfg
python run.py 
```

Or you can run with docker:
```buildoutcfg
docker build -t pokemon_api --rm .
docker run -it --name pokemon_api --rm pokemon_api
# and then in the shell
python run.py 
```
Tests:
```buildoutcfg
nameko test
pytest --cov=app tests/
```