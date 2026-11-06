#!/usr/bin/env python3
"""Apply typesetting-only changes, without altering mathematical content."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT/'chapters').glob('*.tex'):
 s=p.read_text()
 def fix(env):
  return re.sub(r'"([^"\n]*)"',lambda m:'"'+(m[1] if m[1].startswith('{') and m[1].endswith('}') else '{'+m[1]+'}')+'"',env[0])
 s=re.sub(r'\\begin\{tikzcd\}.*?\\end\{tikzcd\}',fix,s,flags=re.S)
 s=re.sub(r'\\item\[([^\n]*?)\](?=\s)',lambda m:'\\item[{'+m[1]+'}]' if not(m[1].startswith('{') and m[1].endswith('}')) else m[0],s)
 if p.name=='01a.tex':
  s=s.replace(r''' \Hom(T,X)\to\Hom(T,Y)\to\Hom(T,Z),\qquad
 \Hom(Z,T)\to\Hom(Y,T)\to\Hom(X,T).''',r''' \begin{gathered}
 \Hom(T,X)\to\Hom(T,Y)\to\Hom(T,Z),\\[3pt]
 \Hom(Z,T)\to\Hom(Y,T)\to\Hom(X,T).
 \end{gathered}''').replace(r''' 0\to\Hom^{-1}(Z,S)\to\Hom(Z,X)\to\Hom(Z,Y),\qquad
 0\to\Hom(Z,N)\to\Hom^{-1}(Z,S)\to0.''',r''' \begin{gathered}
 0\to\Hom^{-1}(Z,S)\to\Hom(Z,X)\to\Hom(Z,Y),\\[3pt]
 0\to\Hom(Z,N)\to\Hom^{-1}(Z,S)\to0.
 \end{gathered}''')
 if p.name=='02.tex':
  s=s.replace(r'预\term{sheaf}{层} $U\mapsto\Hom_{\D(U,\mathcal O)}(K|_U,L|_U)$ 是\term{sheaf}{层}。',r'预\term{sheaf}{层}\[U\longmapsto\Hom_{\D(U,\mathcal O)}(K|_U,L|_U)\]是\term{sheaf}{层}。')
  s=s.replace(r'(\tau_{<t}i^*j_*A,A,\tau_{\geq t}i^*j_*A)',r'(\tau_{<t}i^*j_*A,\allowbreak A,\allowbreak\tau_{\geq t}i^*j_*A)')
 if p.name=='03.tex':
  s=s.replace(r'(V,\mathcal O),{}^p\D',r'(V,\mathcal O),\allowbreak{}^p\D').replace(r'(X,\mathcal O),{}^p\D',r'(X,\mathcal O),\allowbreak{}^p\D').replace(r'(X,\Z),{}^{p^+}\D',r'(X,\Z),\allowbreak{}^{p^+}\D')
 if p.name=='04.tex':
  s=s.replace(r'$(f_![d],f^![-d])$',r'$(f_![d],\allowbreak f^![-d])$').replace(r'$(f^*[d],f_*[-d])$',r'$(f^*[d],\allowbreak f_*[-d])$').replace(r'$R\mathcal Hom(f^*K,f^*L)=R\mathcal Hom(f^*K[d],f^*L[d])$',r'\[R\mathcal Hom(f^*K,f^*L)=R\mathcal Hom(f^*K[d],f^*L[d])\]').replace(r'\displaystyle\sup\left\{\prod_{a\in A}d_a\;\middle|\; A\subset[2,n],\ |A|=n-(q+1)-1\right\}',r'\displaystyle\sup_{\substack{A\subset[2,n]\\ |A|=n-(q+1)-1}}\prod_{a\in A}d_a')
 if p.name=='06.tex':
  s=s.replace(r'$(h_*Rh^!,\id,Rj_*j^*)$',r'$(h_*Rh^!,\allowbreak\id,\allowbreak Rj_*j^*)$')
 p.write_text(s)
