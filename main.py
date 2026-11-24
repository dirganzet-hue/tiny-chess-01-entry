import json,os,urllib.request as u
V=[0,100,320,330,500,900,0]
Y={1:'PPPPUUUUQQRSQQRUPPPXQOOPQQQNPPPP',2:'KLMMLNPPMPQRMPRSMPRSMPQRLNPPKLMM'}
n=(-33,-31,-18,-14,14,18,31,33)
d=(-17,-15,15,17)
o=(-16,-1,1,16)
g=d+o
D=[0,0,n,d,o,g,g]
b=[0]*128
s=1
c=0
e=-1
w=4
k=116
Z=Exception
def i(u):return (int(u[1])-1)*16+ord(u[0])-97
def J(q):return chr(97+(q&7))+str((q>>4)+1)
def j(m):return J(m[0])+J(m[1])+('q' if m[2] else '')
def I(u):return (i(u[:2]),i(u[2:4]),5-'QRBN'.index(u[4].upper()) if len(u)==5 else 0)
def F(f):
 global b,s,c,e,w,k;t=f.split();b=[0]*128
 for r,W in enumerate(t[0].split('/')):
  x=0
  for h in W:
   if h.isdigit():x+=int(h)
   else:
    v='PNBRQK'.index(h.upper())+1;b[(7-r)*16+x]=v if h.isupper() else -v;x+=1
 s=1 if t[1]=='w' else -1
 c=0
 for z,q in enumerate('KQkq'):c|=(q in t[2])<<z
 e=-1 if t[3]=='-' else i(t[3])
 w=b.index(6);k=b.index(-6)
def A(q,y):
 for z in(15,17):
  t=q-z*y
  if not(t&136)and b[t]==y:return 1
 for z in n+g:
  t=q+z
  if not(t&136)and b[t]==(2 if z in n else 6)*y:return 1
 for z in d+o:
  t=q+z
  while not(t&136):
   p=b[t]
   if p:
    if p==5*y or p==(3 if z in d else 4)*y:return 1
    break
   t+=z
 return 0
def G():
 m=[]
 for q in range(128):
  if q&136:continue
  p=b[q]
  if not p or(p>0)!=(s>0):continue
  a=abs(p)
  if a==1:
   z=16*s
   W=s>0
   j=7*W
   t=q+z
   if not b[t]:
    m.append((q,t,5*((t>>4)==j)))
    if(q>>4)==6-5*W:
     u=q+2*z
     if not b[u]:m.append((q,u,0))
   for z in(z-1,z+1):
    t=q+z
    if t&136:continue
    if b[t] and(b[t]>0)!=(s>0):m.append((q,t,5*((t>>4)==j)))
    elif t==e:m.append((q,t,0))
  else:
   for z in D[a]:
    t=q+z
    if a%4==2:
     if not(t&136)and(not b[t] or(b[t]>0)!=(s>0)):m.append((q,t,0))
    else:
     while not(t&136):
      if not b[t]:m.append((q,t,0))
      else:
       if(b[t]>0)!=(s>0):m.append((q,t,0))
       break
      t+=z
   if a==6:
    for R,T in(((1,q+2),(2,q-2)) if s>0 else((4,q+2),(8,q-2))):
     z=1 if T>q else -1
     if c&R and not b[q+z] and not b[q+2*z] and not(T<q and b[q+3*z]) and not A(q,-s) and not A(q+z,-s) and not A(q+2*z,-s):m.append((q,T,0))
 o=[]
 for v in m:
  u=M(v)
  q=w if s<0 else k
  if not A(q,s):o.append(v)
  U(v,u)
 return o
def M(m):
 global s,c,e,w,k
 f,t,r=m;p=b[f];v=b[t];q=t;x=y=-1
 if abs(p)==1 and t==e and not v:
  q=t-16*s
  v=b[q]
  b[q]=0
 if abs(p)==6 and abs(t-f)==2:x,y=(t+1,t-1)if t>f else(t-2,t+1);b[y]=b[x];b[x]=0
 u=(v,q,c,e,x,y,w,k,p)
 b[t]=r*s if r else p;b[f]=0
 if abs(p)==6:
  if s>0:w=t;c&=~3
  else:k=t;c&=~12
 for q,z in((0,2),(7,1),(112,8),(119,4)):
  if f==q or t==q:c&=~z
 if abs(p)==1 and abs(t-f)==32:e=f+16*s
 else:e=-1
 s=-s;return u
def U(m,u):
 global s,c,e,w,k
 v,q,z,j,x,y,W,K,p=u;f,t,r=m;s=-s;c,e,w,k=z,j,W,K;b[f]=p;b[t]=0
 if v:b[q]=v
 if x>=0:b[x]=b[y];b[y]=0
def E():
 t=0
 for q in range(128):
  if q&136:continue
  p=b[q]
  if p:
   a=abs(p)
   r=q>>4
   v=V[a]+ord(Y.get(a,'P'*32)[(r if p>0 else 7-r)*4+min(q&7,7-(q&7))])-80
   t+=v if p>0 else -v
 return t if s>0 else -t
def H(m):
 f,t,r=m;z=b[t]
 if not z and abs(b[f])==1 and t==e:z=s
 v=10*V[abs(z)]-V[abs(b[f])] if z else 0
 if r:v+=900
 return v
def X(d,a,z,y):
 global N;N+=1
 if N>12000:raise Z
 if d>0:
  m=G()
  if not m:return -100000+y if A(w if s>0 else k,-s) else 0
  m.sort(key=H,reverse=True)
  for q in m:
   u=M(q)
   t=-X(d-1,-z,-a,y+1)
   U(q,u)
   if t>a:a=t
   if a>=z:break
  return a
 t=E()
 if t>=z:return z
 if t>a:a=t
 o=[m for m in G() if b[m[1]] or m[2] or(abs(b[m[0]])==1 and m[1]==e)]
 o.sort(key=H,reverse=True)
 for m in o:
  u=M(m)
  t=-X(0,-z,-a,0)
  U(m,u)
  if t>a:a=t
  if a>=z:break
 return a
def R(l):
 global N;r=sorted(map(I,l));N=0;h=r[0]
 try:
  for d in range(1,7):
   o=None
   v=-10**9
   for m in r:
    u=M(m)
    t=-X(d-1,-10**9,10**9,1)
    U(m,u)
    if t>v:v=t;o=m
   h=o
 except Z:
  pass
 return j(h)
L=os.environ["MAKEFUN_ENV_URL"]
while 1:
 z=json.load(u.urlopen(L+"/game",b"{}"))
 if z["status"]=="done":break
 while z["status"]=="your_move":
  F(z["fen"])
  z=json.load(u.urlopen(L+"/move",json.dumps({"game":z["game"],"move":R(z["legal_moves"])}).encode()))
