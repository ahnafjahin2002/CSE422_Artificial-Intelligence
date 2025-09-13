#PART-1
import numpy as np
from queue import PriorityQueue

def m_solver(file_loc):
  lines=open(file_loc, 'r').read().strip().split('\n')
  d_line=lines[0].split()
  r, c=int(d_line[0]), int(d_line[1])
  st_pos=lines[1].split()
  st=(int(st_pos[0]), int(st_pos[1]))
  g_pos=lines[2].split()
  g=(int(g_pos[0]), int(g_pos[1]))
  m_line=[line.replace(' ', '') for line in lines[3:]]
  m_array=np.array([list(row) for row in m_line])
  return r, c, st, g, m_array

def h_n(pos1, pos2):
  return np.sum(np.abs(np.array(pos1) - np.array(pos2)))

def valid_move(p, d, m, t):
  r, c=p
  row, cl=d
  if 0<=r<row and 0<=c<cl:
    return m[r, c] == '0' and not t[r, c]
  return False

def path_track(p_line):
  output = ''
  for char in p_line:
    if char == 'X':
      output += 'U'
    elif char == 'Y':
      output += 'D'
    elif char == 'Z':
      output += 'R'
    elif char == 'M':
      output += 'L'
  return output

def a_algo(dim, st, g, maze):
  row, cl=dim
  priority_node=PriorityQueue()
  priority_node.put((h_n(st, g), 0, st, ''))
  checked = np.zeros((row, cl), dtype=bool)
  temp = {
      'X': (-1, 0),
      'Y': (1, 0),
      'Z': (0, 1),
      'M': (0, -1),
  }

  while not priority_node.empty():
    near, c, x, path=priority_node.get()
    if checked[x]:
      continue
    checked[x]=True

    if x==g:
      print(c)
      print(path_track(path))
      return

    for var in temp:
      dr, dc=temp[var]
      y=(x[0] + dr, x[1] + dc)
      if valid_move(y, (row, cl), maze, checked):
        g_n = c + 1
        f = g_n + h_n(y, g)
        priority_node.put((f, g_n, y, path + var))

  print(-1)

if __name__ == '__main__':
  files = ['input1.txt', 'input2.txt', 'input3.txt']
  for f in files:
    print(f"processing {f}")
    try:
      n_r, n_c, st_pt, end_pt, m_d = m_solver(f)
      a_algo((n_r, n_c), st_pt, end_pt, m_d)
    except Exception as ex:
      print(f"Failed on {f}: {ex}")
    print('=' * 30)

