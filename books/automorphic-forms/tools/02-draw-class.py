from pathlib import Path
P=Path(__file__).resolve().parents[1]
def graph(name,pts,edges,labels={}):
 s=['\\begin{tikzpicture}[x=.43cm,y=.43cm,line width=.5pt]']
 for i,(x,y) in enumerate(pts):s.append(f'\\coordinate (n{i}) at ({x},{y});\\draw({x},{{{y}-.08}})--({x},{{{y}+.08}});')
 for i,j,m,arrow,dashed in edges:
  if m==1:s.append(f'\\draw[{"dashed" if dashed else "solid"}](n{i})--(n{j});')
  elif m==4:s.append(f'\\draw[line width=2pt](n{i})--(n{j});')
  else:
   for off in ([-.06,.06] if m==2 else [-.08,0,.08]):s.append(f'\\draw($(n{i})+(0,{off})$)--($(n{j})+(0,{off})$);')
  if arrow:
   a,b=(i,j) if arrow==1 else (j,i)
   s.append(f'\\draw[->]($(n{a})!.3!(n{b})$)--($(n{a})!.7!(n{b})$);')
 for i,t in labels.items():s.append(f'\\node[below]at($(n{i})+(0,-.12)$){{{t}}};')
 s+=['\\end{tikzpicture}'];(P/'figures'/f'02-class-split-{name}.tex').write_text('\n'.join(s))
pts=[(i,0) for i in range(6)]
chain=[(i,i+1,1,0,i==2) for i in range(5)]
graph('A1',[(0,0),(1,0)],[(0,1,4,0,False)],{0:'hs',1:'hs'})
fork=[(i,0)for i in range(5)]+[(5,.8),(5,-.8)]
e=[(0,1,2,-1,False),(1,2,1,0,False),(2,3,1,0,True),(3,4,1,0,False),(4,5,1,0,False),(4,6,1,0,False)]
graph('B',fork,e,{5:'hs',6:'hs'});graph('BC',fork,[(i,j,m,-a,d)for i,j,m,a,d in e],{5:'s',6:'s'})
for name,a,b,lab in [('C',1,-1,'hs'),('CB',-1,1,'s'),('CBC',-1,-1,'s')]:
 graph(name,pts,[(0,1,2,a,False)]+chain[1:4]+[(4,5,2,b,False)],{0:lab,5:lab})
graph('CBC1',[(0,0),(1,0)],[(0,1,4,-1,False)],{0:'s',1:'s'})
graph('D',[(-1,.8),(-1,-.8),(0,0),(1,0),(2,0),(3,0),(4,.8),(4,-.8)],[(0,2,1,0,False),(1,2,1,0,False),(2,3,1,0,False),(3,4,1,0,True),(4,5,1,0,False),(5,6,1,0,False),(5,7,1,0,False)],{0:'hs',1:'hs',6:'hs',7:'hs'})
graph('E6',[(0,0),(1,0),(2,0),(3,1),(4,2),(3,-1),(4,-2)],[(0,1,1,0,False),(1,2,1,0,False),(2,3,1,0,False),(3,4,1,0,False),(2,5,1,0,False),(5,6,1,0,False)],{0:'hs',4:'hs',6:'hs'})
for name,n,branch in [('E7',7,3),('E8',8,5)]:graph(name,[(i,0)for i in range(n)]+[(branch,1)],[(i,i+1,1,0,False)for i in range(n-1)]+[(branch,n,1,0,False)],{0:'hs',**({6:'hs'}if name=='E7'else{})})
for name,arr,lab in [('F4',1,'hs'),('F4I',-1,'s')]:graph(name,[(i,0)for i in range(5)],[(0,1,1,0,False),(1,2,1,0,False),(2,3,2,arr,False),(3,4,1,0,False)],{0:lab})
for name,arr,lab in [('G2',1,'hs'),('G2I',-1,'s')]:graph(name,[(i,0)for i in range(3)],[(0,1,1,0,False),(1,2,3,arr,False)],{0:lab})
