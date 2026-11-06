from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
# volume, section, start page, English title, Chinese title, author, slug
rows=[
(1,1,3,'Reductive groups','约化群','T. A. Springer','springer'),
(1,1,29,'Reductive groups over local fields','局部域上的约化群','J. Tits','tits'),
(1,1,71,'Representations of reductive Lie groups','约化 Lie 群的表示','Nolan R. Wallach','wallach'),
(1,1,87,'Representations of GL2(R) and GL2(C)','GL₂(R) 与 GL₂(C) 的表示','A. W. Knapp','knapp'),
(1,1,93,'Normalizing factors, tempered representations, and L-groups','正规化因子、缓增表示与 L 群','A. W. Knapp and Gregg Zuckerman','knapp-zuckerman'),
(1,1,107,'Orbital integrals for GL2(R)','GL₂(R) 的轨道积分','D. Shelstad','shelstad-gl2'),
(1,1,111,'Representations of p-adic groups: A survey','p 进群的表示：综述','P. Cartier','cartier'),
(1,1,157,'Cuspidal unramified series for central simple algebras over local fields','局部域上中心单代数的尖点非分歧系列','Paul Gérardin','gerardin'),
(1,1,171,'Some remarks on the supercuspidal representations of p-adic semisimple groups','关于 p 进半单群超尖点表示的若干注记','G. Lusztig','lusztig'),
(1,2,179,'Decomposition of representations into tensor products','表示的张量积分解','D. Flath','flath'),
(1,2,185,'Classical and adelic automorphic forms. An introduction','经典自守形式与阿代尔自守形式导论','I. Piatetski-Shapiro','ps-intro'),
(1,2,189,'Automorphic forms and automorphic representations','自守形式与自守表示','A. Borel and H. Jacquet','borel-jacquet'),
(1,2,203,'On the notion of an automorphic representation. A supplement to the preceding paper','论自守表示的概念：前文的补充','R. P. Langlands','langlands-notion'),
(1,2,209,'Multiplicity one theorems','重数一定理','I. Piatetski-Shapiro','multiplicity'),
(1,2,213,'Forms of GL(2) from the analytic point of view','从分析观点看 GL(2) 上的形式','Stephen Gelbart and Hervé Jacquet','gelbart-jacquet'),
(1,2,253,'Eisenstein series and the trace formula','Eisenstein 级数与迹公式','James Arthur','arthur'),
(1,2,275,'Theta-series and invariant theory','Theta 级数与不变量理论','R. Howe','howe'),
(1,2,287,'Examples of dual reductive pairs','约化对偶对的例子','Stephen Gelbart','gelbart'),
(1,2,297,'On a relation between SL2 cusp forms and automorphic forms on orthogonal groups','SL₂ 尖点形式与正交群自守形式之间的关系','S. Rallis','rallis'),
(1,2,315,'A counterexample to the generalized Ramanujan conjecture for (quasi-)split groups','（拟）分裂群的广义 Ramanujan 猜想的一个反例','R. Howe and I. I. Piatetski-Shapiro','ramanujan'),
(2,3,3,'Number theoretic background','数论背景','J. Tate','tate'),
(2,3,27,'Automorphic L-functions','自守 L 函数','A. Borel','borel-l'),
(2,3,63,'Principal L-functions of the linear group','线性群的主 L 函数','Hervé Jacquet','jacquet-l'),
(2,3,87,'Automorphic L-functions for the symplectic group GSp4','辛群 GSp₄ 的自守 L 函数','Mark E. Novodvorsky','novodvorsky'),
(2,3,97,'On liftings of holomorphic cusp forms','论全纯尖点形式的提升','Takuro Shintani','shintani'),
(2,3,111,'Orbital integrals and base change','轨道积分与基变换','R. Kottwitz','kottwitz-base'),
(2,3,115,'The solution of a base change problem for GL(2) (following Langlands, Saito, Shintani)','GL(2) 一个基变换问题的解答（依照 Langlands、Saito、Shintani）','P. Gérardin and J.-P. Labesse','gerardin-labesse'),
(2,3,135,'Report on the local Langlands conjecture for GL2','GL₂ 的局部 Langlands 猜想报告','J. Tunnell','tunnell'),
(2,4,141,'The Hasse-Weil zeta-function of some moduli varieties of dimension greater than one','若干维数大于一的模簇的 Hasse–Weil zeta 函数','W. Casselman','casselman'),
(2,4,165,'Points on Shimura varieties mod p','模 p 的 Shimura 簇上的点','J. S. Milne','milne'),
(2,4,185,'Combinatorics and Shimura varieties mod p (based on lectures by Langlands)','组合学与模 p 的 Shimura 簇（据 Langlands 讲座）','R. Kottwitz','kottwitz-shimura'),
(2,4,193,'Notes on L-indistinguishability (based on a lecture by R. P. Langlands)','L 不可区分性札记（据 R. P. Langlands 讲座）','D. Shelstad','shelstad-l'),
(2,4,205,'Automorphic representations, Shimura varieties, and motives. Ein Märchen','自守表示、Shimura 簇与动机：一个童话','R. P. Langlands','langlands-motives'),
(2,4,247,'Variétés de Shimura : interprétation modulaire, et techniques de construction de modèles canoniques','Shimura 簇：模解释与典范模型的构造技术','Pierre Deligne','deligne-shimura'),
(2,4,291,'Congruence relations and Shimura curves','同余关系与 Shimura 曲线','Yasutaka Ihara','ihara'),
(2,4,313,'Valeurs de fonctions L et périodes d’intégrales','L 函数的值与积分的周期','P. Deligne','deligne-periods'),
(2,4,343,'Algebraicity of some products of values of the Gamma function','Gamma 函数若干值的乘积的代数性（附录）','N. Koblitz and A. Ogus','koblitz-ogus'),
(2,4,347,'An introduction to Drinfeld’s Shtuka','Drinfeld 的 shtuka 导论','D. A. Kazhdan','kazhdan'),
(2,4,357,'Automorphic forms on GL2 over function fields (after V. G. Drinfeld)','函数域上 GL₂ 的自守形式（依照 V. G. Drinfeld）','G. Harder and D. A. Kazhdan','harder-kazhdan')]
vols={v:json.loads((P/f'volume-{v}-pages.json').read_text()) for v in (1,2)}
entries=[]
for i,(v,s,n,en,zh,author,slug) in enumerate(rows,1):
 start=next(r['pdf_page'] for r in vols[v]['pages'] if r['printed_page']==n)
 nxt=rows[i] if i<len(rows) else None
 stop=next(r['pdf_page'] for r in vols[v]['pages'] if r['printed_page']==nxt[2])-1 if nxt and nxt[0]==v else (314 if v==1 else 371)
 selected=vols[v]['pages'][start-1:stop]
 # last printed page can be extracted reliably at article end
 end=selected[-1]['printed_page']
 item=dict(id=f'{i:02d}',volume=v,part=s,printed_start=n,printed_end=end,pdf_start=start,pdf_end=stop,title_original=en,title_zh=zh,author=author,slug=slug,file=f'chapters/{i:02d}-{slug}.tex',source_pdf=vols[v]['source'])
 entries.append(item)
 text='\n\n'.join(f'===== PDF PAGE {r["pdf_page"]} / PRINTED PAGE {r["printed_page"]} =====\n'+(P/r['text_file']).read_text() for r in selected)
 (P/'source-text'/f'{i:02d}-{slug}.txt').write_text(text)
(P/'articles.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
for e in entries: print(e['id'],e['slug'],'v',e['volume'],'print',e['printed_start'],e['printed_end'],'pdf',e['pdf_start'],e['pdf_end'])
