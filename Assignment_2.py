#Task-1

import random

x=25
y=6
z=15
mp=0.1

a=1000
b=2
c=1

comp={
    'ALU':(5,5),
    'Cache':(7,4),
    'ControlUnit':(4,4),
    'RegisterFile':(6,6),
    'Decoder':(5,3),
    'FloatingUnit': (5,5)
}
order=list(comp)
links=[
    ('RegisterFile', 'ALU'),
    ('ControlUnit', 'ALU'),
    ('ALU', 'Cache'),
    ('RegisterFile','FloatingUnit'),
    ('Cache', 'Decoder'),
    ('Decoder', 'FloatingUnit')
]

def mid(p, label):
  w, h=comp[label]
  return (p[0]+w/2, p[1]+h/2)

def dist(p1, p2):
  return ((p1[0]-p2[0])**2+ (p1[1]-p2[1])**2)**0.5

def w_len(arr):
  total=0
  for u,v in links:
    i= order.index(u)
    j= order.index(v)
    c1= mid(arr[i],u)
    c2= mid(arr[j],v)
    total+= dist(c1,c2)
  return total

def area(arr):
  minx = miny = float('inf')
  maxx = maxy = 0
  for idx, (x0, y0) in enumerate(arr):
    w, h = comp[order[idx]]
    minx = min(minx, x0)
    miny = min(miny, y0)
    maxx = max(maxx, x0 + w)
    maxy = max(maxy, y0 + h)
  return (maxx - minx) * (maxy - miny)

def ov(pos1,pos2,n1,n2):
  x1,y1= pos1
  x2,y2= pos2
  w1,h1= comp[n1]
  w2,h2= comp[n2]
  if x1+w1<= x2 or x2+w2<=x1:
    return False
  if y1+h1<=y2 or y2+h2<=y1:
    return False
  return True

def ov_count(layout):
  cnt= 0
  for i in range(len(layout)):
    for j in range(i+1, len(layout)):
      if ov(layout[i], layout[j], order[i], order[j]):
        cnt+=1
  return cnt

def fitness(sol):
  ovl=ov_count(sol)
  wire=w_len(sol)
  box= area(sol)
  penalty=a*ovl+b*wire+c*box
  return -penalty

def rnd_sol():
  sol=[]
  for var in order:
    x_coord= random.randint(0,x)
    y_coord= random.randint(0,x)
    pos=(x_coord,y_coord)
    sol.append(pos)
  return sol

def xover(p1,p2):
  pt=random.randint(1, len(p1)-1)
  return p1[:pt]+p2[pt:], p2[:pt]+p1[pt:]

def mutate(entity):
  if random.random()<mp:
    idx=random.randint(0, len(entity)-1)
    new_x=random.randint(0,x)
    new_y=random.randint(0,y)
    entity[idx]=(new_x, new_y)
  return entity

def run():
  pop=[]
  for var in range(y):
    temp=rnd_sol()
    pop.append(temp)

  for gen in range(z):
    ranked =[]
    for sol in pop:
      score=fitness(sol)
      pair=(score, sol)
      ranked.append(pair)
    ranked.sort(reverse=True, key=lambda itm: itm[0])

    nxt=[]
    elite1=ranked[0][1]
    elite2=ranked[1][1]
    nxt.append(elite1)
    nxt.append(elite2)

    while len(nxt)<y:
      chosen=random.sample(ranked[:4], 2)
      p1=chosen[0][1]
      p2=chosen[1][1]
      child1, child2=xover(p1,p2)
      m1=mutate(child1)
      nxt.append(m1)
      if len(nxt)<y:
        m2=mutate(child2)
        nxt.append(m2)
    pop=[]
    for entity in nxt:
      pop.append(entity)

  best= None
  highest= None
  for sol in pop:
    val= fitness(sol)
    if best is None or val> highest:
      best=sol
      highest=val
  return best, highest


def show(layout, score):
  print(f"best total fitness value      : {score:.2f}")
  print(f"total wiring length           : {w_len(layout):.2f}")
  print(f"the total bounding box area  : {area(layout):.2f}")
  print(f"the total overlap counts      : {ov_count(layout)}")
  print("\nPositions:")
  for name, pos in zip(order, layout):
    print(f"{name:<16}: {pos}")


if __name__ == "__main__":
    res, scr = run()
    show(res, scr)


