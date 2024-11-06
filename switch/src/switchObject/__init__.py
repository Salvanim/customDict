import copy
from types import UnionType

class Dict:

  def __init__(self, keys: list = None, values: list = None, loop: bool = True):
    self.keys = keys if keys is not None else []
    self.values = values if values is not None else []
    self.loop = loop

    while len(self.keys) < len(self.values):
      self.values.pop()

    while len(self.keys) > len(self.values):
      self.keys.pop()

    self.__oKeys = copy.deepcopy(keys)
    self.__oValues = copy.deepcopy(values)
    self.__oLoop = copy.deepcopy(loop)
    self.isReversed = False
    self.selector = -1

  @classmethod
  def dict(self, dictionary):
    if isinstance(dictionary, Dict):
      return dictionary
    return Dict(list(dictionary.keys()), list(dictionary.values()))

  @classmethod
  def asArg(self, *args):
    evenArgs = []
    oddArgs = []
    for i, arg in enumerate(args):
      if i % 2 == 0:
        evenArgs.append(arg)
      else:
        oddArgs.append(arg)
    return Dict(evenArgs, oddArgs)

  def __deepcopy__(self, memo):
        copied = Dict(copy.deepcopy(self.keys, memo),
                     copy.deepcopy(self.values, memo),
                     copy.deepcopy(self.loop, memo))
        copied.isReversed = self.isReversed
        copied.__oKeys = copy.deepcopy(self.__oKeys, memo)
        copied.__oValues = copy.deepcopy(self.__oValues, memo)
        copied.__oLoop = copy.deepcopy(self.__oLoop, memo)
        return copied

  def origin(self):
     return Dict(self.__oKeys, self.__oValues, self.__oLoop)

  def __reduce__(self):
        return (self.__class__, (self.keys, self.values, self.loop))

  def __len__(self):
    return len(self.keys)

  def Loop(self, loop):
    self.loop = loop

  def keyIndex(self, key):
    return self.keys.index(key)

  def __getitem__(self, key):
    end = Dict()
    if isinstance(key, slice):
      start = key.start
      ending = key.stop
      step = key.step
      if start == None:
        start = 0
      if ending == None:
        ending = len(self)
      if step == None:
        step = 1
      for i in range(start, ending, step):
        end += Dict([self.keys[i]], [self.values[i]])
    else:
      if key in self.keys:
        return self.values[self.keyIndex(key)]
      else:
        if (key > len(self.keys) and self.loop):
          key = key % len(self.keys)
        end = Dict([self.keys[key]], [self.values[key]], self.loop)
    return end

  def __call__(self, *args, **kwargs):
        if args:
            self.update(*args)
        if kwargs:
            self.update(kwargs)
        return self

  def isItterable(self, object, exclude=[str]):
    try:
      object = iter(object)
    except:
       return False
    if type(object) in exclude:
       return False
    return True

  def __setitem__(self, key, value):
    if self.isItterable(key):
      for k in key:
        if k in self.keys:
            self.values[self.keyIndex(k)] = value
        else:
            self.keys.append(k)
            self.values.append(value)
    else:
       iteratingKeys = copy.deepcopy(self.keys)
       for k in iteratingKeys:

          if k == key:
            self.values[self.keyIndex(key)] = value
          else:
            self.keys.append(key)
            self.values.append(value)

  def __add__(self, other):
    copiedSelf = self.__copy__()
    copiedOther = other
    if isinstance(other, Dict):
      copiedOther = other.__copy__()
      for key in copiedOther.keys:
        copiedSelf[key] = copiedOther[key]
    elif isinstance(other, dict):
      for key in copiedOther.keys():
        copiedSelf[key] = copiedOther[key]
    else:
      for key in copiedSelf.keys:
        copiedSelf[key] += copiedOther
    return copiedSelf

  def __mul__(self, other):
    return self.multAll(other)

  def __truediv__(self, other):
    return self.divAll(other)

  def __floordiv__(self, other):
    return self.floordivAll(other)

  def __mod__(self, other):
    return self.modAll(other)

  def __pow__(self, other):
    return self.powAll(other)

  def __sub__(self, other):
    copiedSelf = self.__copy__()
    copiedOther = other

    if copiedSelf < copiedOther:
      temp = copiedSelf
      copiedSelf = copiedOther
      copiedOther = temp

    for key in copiedOther.keys:
      if key in copiedSelf.keys:
        del copiedSelf[key]
    return copiedSelf

  def __delitem__(self, key):
    self.values.pop(self.keyIndex(key))
    self.keys.pop(self.keyIndex(key))

  def __str__(self):
    outString = "{"
    i = 0
    while i < len(self.keys):
      outString += f"{self.keys[i]}: {self.values[i]}"
      if i < len(self.keys) - 1:
        outString += ", "
      i += 1
    return outString + "}"

  def __eq__(self, value):
    for key in self.keys:
      if key not in value.keys or self[key] != value[key]:
        return False
    return True

  def __ne__(self, value):
     return not(self==value)

  def __gt__(self, other):
    if len(self.keys) > len(other.keys):
      return True
    return False

  def __lt__(self, other):
    if len(self.keys) < len(other.keys):
      return True
    return False

  def __ge__(self, other):
    return self == other or self > other

  def __le__(self, other):
    return self == other or self < other

  def __contains__(self, key):
    return key in self.keys or key in self.values

  def __sizeof__(self):
    return len(self)

  def __iter__(self):
    return iter(self.keys)

  def reverse(self):
    self.keys = self.keys[::-1]
    self.values = self.values[::-1]
    return self

  def flip(self):
    temp = self.keys
    self.keys = self.values
    self.values = temp
    return self

  def __invert__(self):
     self.flip()
     return self

  def __neg__(self):
     self.reverse()
     self.isReversed = True
     return self

  def __pos__(self):
     return self

  def __abs__(self):
    if self.isReversed:
      self.reverse()
    return self
  def __next__(self):
        if not hasattr(self, '_iter_index'):
            self._iter_index = 0
        if self._iter_index < len(self.keys):
            result = (self.keys[self._iter_index], self.values[self._iter_index])
            self._iter_index += 1
            return result
        else:
            del self._iter_index
            raise StopIteration

  def shiftValues(self, n):
    self.values = self.values[n:] + self.values[:n]
    return self

  def shiftKeys(self, n):
    self.keys = self.keys[n:] + self.keys[:n]
    return self.keys

  def shift(self, n):
    self.shiftValues(n)
    self.shiftKeys(n)
    return self

  def __rshift__(self, other):
     self.shift(other)
     return self

  def __lshift__(self, other):
     self.shift(-1 * other)
     return self

  def slice(self, start=0, end=None, step=None):
    return self[slice(start, end, step)]

  def pop(self, i=None):
    if i == None:
      popedValue = self.values[len(self.keys)]
      self.keys.pop()
      self.values.pop()
    else:
      popedValue = self.values[i]
      self.keys.pop(i)
      self.values.pop(i)
    return popedValue

  def remove(self, key):
    self.pop(self.keyIndex(key))
  def clear(self):
    self.keys = []
    self.values = []

  def append(self, key, value):
    self.keys.append(key)
    self.values.append(value)

  def asDict(self):
    endDict = {}
    for i in range(len(self.keys)):
      endDict[self.keys[i]] = self.values[i]
    return endDict

  def update(self, dictionary, **kwargs):
    if dictionary:
        if isinstance(dictionary, Dict):
            for key in dictionary.keys:
                self[key] = dictionary[key]
        else:
            for key, value in dictionary.items():
                self[key] = value
    for key, value in kwargs.items():
        self[key] = value

  def fromkeys(cls, iterable, value=None):
    return cls(list(iterable), [value] * len(iterable))

  def copy(self):
        return Dict(self.keys.copy(), self.values.copy(), self.loop)

  def __copy__(self):
        return self.copy()

  def __repr__(self):
        return f"Dict(keys={self.keys}, values={self.values}, loop={self.loop}, selector={self.selector})"

  def __sizeof__(self):
        return len(self)

  def __contains__(self, key):
        return key in self.keys

  def __iter__(self):
        return iter(self.keys)

  def popitem(self):
    if not self.keys:
        raise KeyError("popitem(): dictionary is empty")
    key = self.keys.pop()
    value = self.values.pop()
    return (key, value)

  def get(self, key, default=None):
    return self[key] if key in self.keys else default

  def setdefault(self, key, default=None):
    if key not in self.keys:
        self[key] = default
    return self[key]

  def keys(self):
    return self.keys

  def values(self):
    return self.values

  def items(self):
    return zip(self.keys, self.values)

  def __hash__(self):
    return hash(tuple(self.items()))

  def subAll(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    for k in copySelf:
        if type(copySelf[k]) != type(value):
          try:
            copySelf[k] = type(value)(copySelf[k])
            copySelf[k] -= value
          except:
            try:
              for v in value:
                if type(value) in [list, str]:
                  copySelf.subAll(v, True)
                else:
                  copySelf.subAll(value[v], True)
            except:
              break
        else:
           copySelf[k] -= value
    return copySelf

  def subAllKey(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    i = 0
    for k in copySelf:
        if type(copySelf.keys[i]) != type(value):
           try:
            copySelf.keys[i] = type(value)(copySelf.keys[i])
            copySelf.keys[i] -= value
           except:
              try:
                 copySelf.keys[i] -= type(copySelf.keys[i])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.subAllKey(v, True)
                    else:
                      copySelf.subAllKey(value[v], True)
                except:
                  None
        else:
           copySelf.keys[i] -= value
        i += 1
    return copySelf

  def addAll(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    for k in copySelf:
        if type(copySelf[k]) != type(value):
           try:
            copySelf[k] = type(value)(copySelf[k])
            copySelf[k] += value
           except:
              try:
                 copySelf[k] += type(copySelf[k])(value)
              except:
                try:
                  for v in value:
                    if not(self.isItterable(value)):
                      copySelf.addAll(v, True)
                    else:
                      copySelf.addAll(value[v], True)
                except:
                  break
        else:
           copySelf[k] += value
    return copySelf

  def addAllKey(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    i = 0
    for k in copySelf:
        if type(copySelf.keys[i]) != type(value):
           try:
            copySelf.keys[i] = type(value)(copySelf.keys[i])
            copySelf.keys[i] += value
           except:
              try:
                 copySelf.keys[i] += type(copySelf.keys[i])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.addAllKey(v, True)
                    else:
                      copySelf.addAllKey(value[v], True)
                except:
                  None
        else:
           copySelf.keys[i] += value
        i += 1
    return copySelf

  def multAllKey(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    i = 0
    for k in copySelf:
        if type(copySelf.keys[i]) != type(value):
           try:
            copySelf.keys[i] = type(value)(copySelf.keys[i])
            copySelf.keys[i] *= value
           except:
              try:
                 copySelf.keys[i] += type(copySelf.keys[i])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.multAllKey(v, True)
                    else:
                      copySelf.multAllKey(value[v], True)
                except:
                  None
        else:
           copySelf.keys[i] *= value
        i += 1
    return copySelf

  def multAll(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    for k in copySelf:
        if type(copySelf[k]) != type(value):
           try:
            copySelf[k] = type(value)(copySelf[k])
            copySelf[k] *= value
           except:
              try:
                 copySelf[k] += type(copySelf[k])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.multAll(v, True)
                    else:
                      copySelf.multAll(value[v], True)
                except:
                  None
        else:
           copySelf[k] *= value
    return copySelf

  def divAll(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    for k in copySelf:
        if type(copySelf[k]) != type(value):
           try:
            copySelf[k] = type(value)(copySelf[k])
            copySelf[k] /= value
           except:
              try:
                 copySelf[k] += type(copySelf[k])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.divAll(v, True)
                    else:
                      copySelf.divAll(value[v], True)
                except:
                  None
        else:
           copySelf[k] /= value
    return copySelf

  def divAllKey(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    i = 0
    for k in copySelf:
        if type(copySelf.keys[i]) != type(value):
           try:
            copySelf.keys[i] = type(value)(copySelf.keys[i])
            copySelf.keys[i] /= value
           except:
              try:
                copySelf.keys[i] += type(copySelf.keys[i])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.divAllKey(v, True)
                    else:
                      copySelf.divAllKey(value[v], True)
                except:
                  None
        else:
           copySelf.keys[i] /= value
        i += 1
    return copySelf

  def floordivAll(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    for k in copySelf:
        if type(copySelf[k]) != type(value):
           try:
            copySelf[k] = type(value)(copySelf[k])
            copySelf[k] //= value
           except:
              try:
                copySelf[k] += type(copySelf[k])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.floordivAll(v, True)
                    else:
                      copySelf.floordivAll(value[v], True)
                except:
                  None
        else:
           copySelf[k] //= value
        i += 1
    return copySelf

  def floordivAllKey(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    i = 0
    for k in copySelf:
        if type(copySelf.keys[i]) != type(value):
           try:
            copySelf.keys[i] = type(value)(copySelf.keys[i])
            copySelf.keys[i] //= value
           except:
              try:
                 copySelf.keys[i] += type(copySelf.keys[i])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.floordivAllKey(v, True)
                    else:
                      copySelf.floordivAllKey(value[v], True)
                except:
                  None
        else:
           copySelf.keys[i] //= value
        i += 1
    return copySelf

  def modAll(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    for k in copySelf:
        if type(copySelf[k]) != type(value):
           try:
            copySelf[k] = type(value)(copySelf[k])
            copySelf[k] %= value
           except:
              try:
                 copySelf[k] += type(copySelf[k])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.modAll(v, True)
                    else:
                      copySelf.modAll(value[v], True)
                except:
                  None
        else:
           copySelf[k] %= value
    return copySelf

  def modAllKey(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    i = 0
    for k in copySelf:
        if type(copySelf.keys[i]) != type(value):
           try:
            copySelf.keys[i] = type(value)(copySelf.keys[i])
            copySelf.keys[i] %= value
           except:
              try:
                 copySelf.keys[i] += type(copySelf.keys[i])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.modAllKey(v, True)
                    else:
                      copySelf.modAllKey(value[v], True)
                except:
                  None
        else:
          copySelf.keys[i] %= value
        i += 1
    return copySelf

  def powAll(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    for k in copySelf:
        if type(copySelf[k]) != type(value):
           try:
            copySelf[k] = type(value)(copySelf[k])
            copySelf[k] **= value
           except:
              try:
                 copySelf[k] += type(copySelf[k])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.modAll(v, True)
                    else:
                      copySelf.modAll(value[v], True)
                except:
                  None
        else:
           copySelf[k] **= value
    return copySelf

  def powAllKey(self, value, perm=False):
    copySelf = self.copy()
    if perm:
        copySelf = self
    i = 0
    for k in copySelf:
        if type(copySelf.keys[i]) != type(value):
           try:
            copySelf.keys[i] = type(value)(copySelf.keys[i])
            copySelf.keys[i] **= value
           except:
              try:
                 copySelf.keys[i] += type(copySelf.keys[i])(value)
              except:
                try:
                  for v in value:
                    if type(value) in [list, str]:
                      copySelf.powAllKey(v, True)
                    else:
                      copySelf.powAllKey(value[v], True)
                except:
                  None
        else:
          copySelf.keys[i] **= value
        i += 1
    return copySelf

  def __and__(self, other):
     return self + other

  def __iand__(self, other):
     self = self & other
     return self

  def __xor__(self, other):
     return [self, other]

  def __ixor__(self, other):
     self = self ^ other
     return self

  def __or__(self, other):
    if type(self) == type(other):
        return Dict(list(zip(self.keys, other.keys)), list(zip(self.values, other.values)), self.loop)
    else:
       return self ^ other

  def __ior__(self, other):
     self = self | other
     return self

  def __matmul__(self, other):
    allKeyList = [[self.addAllKey,self.addAll], [self.subAllKey,self.subAll], [self.multAllKey,self.multAll], [self.divAllKey,self.divAll], [self.floordivAllKey,self.floordivAll], [self.modAllKey,self.modAll], [self.powAllKey,self.powAll]]
    col = 0
    row = 0
    if type(other) == tuple and self.selector == -1:
      col = other[1]%len(allKeyList)
      row = other[0]
      self.selector = (row, col)
    elif self.selector == -1:
      self.selector = (other, 0)
    else:
      if type(self.selector) == tuple:
        returnValue = allKeyList[self.selector[0]][self.selector[1]](other)
      self.selector = -1
      return returnValue
    return self

  def __imatmul__(self,other):
     return self.__matmul__(other)
