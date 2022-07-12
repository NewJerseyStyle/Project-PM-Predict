from enum import Enum
from . import nltk_sent
from . import deep_sent

class Engine(Enum):
  NLTK=1
  HUGGINGFACE=2

def main(engine=Engine.NLTK):
  assert isinstance(engine, Engine)
  
  if engine == Engine.NLTK:
      pass
#       nltk_sent.sentiment_analysis()
  elif engine == Engine.HUGGINGFACE:
      pass
#       deep_sent.sentiment_analysis()
  
