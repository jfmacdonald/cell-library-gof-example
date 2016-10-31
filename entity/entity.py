from abc import ABCMeta, abstractmethod
import json
import yaml

class Entity(metaclass=ABCMeta):

    @abstractmethod
    def _dictionary(self):
        pass

    def get_json(self, **opts):
        return self._dictionary().get_json(**opts)

    def get_yaml(self):
        return self._dictionary().get_yaml()

class Dictionary(dict):
    '''
    # doctests
    >>> e = Dictionary()
    >>> e.entity
    'dict'
    >>> e.mything = 'python'
    >>> e['mything']
    'python'
    >>> e.yourthing = ['poetry', 'photography', 'people']
    >>> e.yourthing
    ['poetry', 'photography', 'people']
    '''

    def __init__(self, entity={ 'entity': 'dict' }):
        super().__init__(entity)

    def __getattr__(self,name):
        if name in self:
            return self[name]
        else:
            return None

    def __setattr__(self,name,value):
        self[name] = value

    def __delattr__(self,name):
        if name in self:
            del self[name]

    def get_json(self, indent=2):
        'get JSON string representation'
        return json.dumps(dict(self),indent=indent)

    def set_json(self, string, **opts):
        'set from JSON string representation'
        try:
            d = json.loads(string, **opts)
            assert isinstance(d,dict)
            for key in d: self[key] = d[key]
            return self
        except Exception as e:
            return None

    def get_yaml(self):
        'get YAML string representation'
        return yaml.dump(dict(self),default_flow_style=False)

    def set_yaml(self, string):
        'set from YAML string representation'
        try:
            d = yaml.safe_load(string)
            assert isinstance(d,dict)
            for key in d: self[key] = d[key]
            return self
        except Exception as e:
            return None

if __name__ == '__main__':
    e = Dictionary()
    e.set_json('{ "foo": "bar", "fruit": ["apple","pear","lemon"] }')
    print(e.get_yaml())

