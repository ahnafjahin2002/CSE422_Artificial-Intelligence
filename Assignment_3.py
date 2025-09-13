#Task1

def fx1 (file_path):
  with open(file_path, 'r') as f:
    var=f.readline().strip().split(',')
    temp=f.readline().strip()
    x=list(map(int, f.readline().strip().split()))
  x=x[-len(temp):]
  return var, temp, x

def fx2(y, temp, x):
  z=0
  for i in range(max(len(y), len(temp))):
    if i<len(y):
      a=ord(y[i])
    else:
      a=0

    if i<len(temp):
      b=ord(temp[i])
    else:
      b=0
    if i<len(x):
      weight=x[i]
    else:
      weight=1
    z -= weight*abs(a-b)
  return z

def fx3(var, y, a, b, z, temp, x):
  if not var:
    return fx2(y, temp, x), y

  score=float('-inf') if a else float('inf')
  best = ''

  for i in range(len(var)):
    k=var[i]
    next_var=var[:i]+var[i+1:]
    next_y=y+k
    val,seq=fx3(next_var, next_y, not a, b, z, temp, x)

    if a:
      if val>score:
        score, best=val, seq
      b=max(b, score)
    else:
      if val<score:
        score, best=val, seq
      z=min(z, score)
    if z<=b:
      break

  return score, best

def fx4():
  var, temp, x=fx1('input.txt')
  score, seq=fx3(var, '', True, float('-inf'), float('inf'), temp, x)
  print("Best gene sequence generated:", seq)
  print("Utility score:", score)
fx4()
