import importlib.resources as resources
import json

urls = json.loads(resources.read_text('api', 'urls.json'))
agents = resources.read_text('api', 'agents.csv').split('\n')
