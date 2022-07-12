from tinydb import TinyDB, Query
import numpy as np

def weighted_mean(x):
	return sum([np.prod(y) for y in x])/sum([np.prod(y, where=[True, False, True]) for y in x])


def weighted_median(x):
	y = [np.prod(y, where=[True, False, True]) for y in x]
	z = sum(y) / 2
	while sum(y) > z:
		y.pop()
	return x[len(y)][1]


def takeSecond(elem):
    return elem[1]


def run():
  ds_db = db.table('qips')
  results = []
  for ds in ds_db:
    l = []
    for i, p, s in zip(ds['i'], ds['p'], ds['s']):
      l.append([i, p, s])
    l.sort(key=takeSecond)
    x = np.array(l)
    results.append((ds['q'],
                    ((weighted_mean(x) + weighted_median(x)) / 2 +
                      max(weighted_mean(x),
                          weighted_median(x)))
                   ))
  results.sort(key=takeSecond)
  return results[:5]
