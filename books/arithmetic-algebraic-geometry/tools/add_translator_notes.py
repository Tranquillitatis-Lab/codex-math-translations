#!/usr/bin/env python3
"""按收到的29项勘误说明定位并插入译者补注；保留正文原有陈述。"""
from pathlib import Path
import json, re, zipfile
ROOT=Path(__file__).resolve().parent.parent
sources={p.name:p.read_text() for p in (ROOT/'chapters').glob('*.tex')}
locations=[]
def attach(num,name,needle,location):
    token=rf'\translatornote{{{num}}}'
    s=sources[name]
    if token not in s:
        if s.count(needle)!=1:raise ValueError(f'补注{num}定位不唯一：{name} {s.count(needle)} {needle}')
        sources[name]=s.replace(needle,needle+token,1)
    locations.append({'number':num,'file':'chapters/'+name,'location':location})
def ref(num,name,needle):
    token=rf'\translatornoteref{{{num}}}'
    if token not in sources[name]:
        if sources[name].count(needle)!=1:raise ValueError(f'补注{num}关联位置不唯一：{name}')
        sources[name]=sources[name].replace(needle,needle+token,1)
def within(num,name,needle,prefix,location):
    token=rf'\translatornote{{{num}}}'
    if token not in sources[name]:
        if sources[name].count(needle)!=1:raise ValueError(f'补注{num}区段不唯一')
        sources[name]=sources[name].replace(needle,needle.replace(prefix,prefix+token,1),1)
    locations.append({'number':num,'file':'chapters/'+name,'location':location})

attach(1,'01-colliot-a.tex',r'映射 $\Pic(X)\longrightarrow\Pic(\bar X)^G$ 就是同构。','第一篇，命题1.1后的Picard下降论证')
attach(2,'01-colliot-a.tex',r'则挠群 $\CH^2(X)_{\mathrm{tors}}$ 的\term{指数有界}{finite exponent}{exposant fini}。','第一篇，定理6.4及其证明')
ref(2,'02-colliot-b.tex','这一结论就成立。[CR1] 已证明了这一点，下面简述其中的主要论证。')
attach(3,'02-colliot-b.tex','自然复合同态','第一篇，备注8.4.2')
attach(4,'02-colliot-b.tex','是 $k$ 中的单位根群，因而有限。','第一篇，定理9.1证明的第二个交换图及说明')
ref(4,'02-colliot-b.tex','所以，利用谱序列的函子性，得到正合列交换图')
attach(5,'03-kato-a.tex',r'$\Gal(\overline{\mathbb Q}_\ell/\mathbb Q_\ell)$ 的表示。定义','第二篇，I §2.2.3(3)')
attach(6,'04-kato-b.tex','固定素数 $p$，令','第二篇，I §2.2.4')
attach(7,'04-kato-b.tex',r'\item $(m,r)\ne(1,0),(2\dim X,\dim X+1)$。','第二篇，I 猜想2.2.7(ii)及§2.2.6(4)')
ref(7,'04-kato-b.tex',r'\item 在 2.2.7 的假设 (i)、(ii) 下，可以证明')
attach(8,'04-kato-b.tex','2.2.7(4) 就是 Lichtenbaum 猜想','第二篇，I §2.2.9')
attach(9,'04-kato-b.tex','当且仅当 $N$ 为合数','第二篇，I §3.3.5')
attach(10,'05-kato-c.tex',r'作为 $\Spec(\Lambda)\longrightarrow\mathbb Z$ 的函数，等于','第二篇，I 引理3.5.5')
attach(11,'05-kato-c.tex','其中 $q$ 为 $F$ 的剩余域的阶。','第二篇，II §2.1.4')
attach(12,'05-kato-c.tex',r'因此在 $\Omega^1(G)$ 上有 $\Tr_\pi\circ[\pi]^*=\pi$。','第二篇，II §2.2.5')
attach(13,'06-kato-d.tex',r'对任意 $n\geq0$，下图交换','第二篇，II 引理2.2.8及§2.2.10证明末行')
ref(13,'06-kato-d.tex',r'及 2.2.9，最后这个余循环的类等于 $\mu_{\xi,n}(dh/h)$ 在'+'\n'+r'$H^1(K_n,\kaJ/p^m)$ 中的像。')
attach(14,'06-kato-d.tex',r'其中 $\chi_G$ 是在 $T$ 上的作用。','第二篇，II §2.3.1')
attach(15,'06-kato-d.tex',r'有 $\Lambda$ 模的典范同构','第二篇，III §1.2.5的de Rham同构')
attach(16,'06-kato-d.tex',r"令 $a$ 为由如下定义的 $a':\Omega'\otimes\mathbb R\xrightarrow{\sim}\Sigma'\otimes\mathbb R$",'第二篇，III §1.2.5的辅助映射a\u2032')
attach(17,'06-kato-d.tex',r'令 $T=T_pE$。','第二篇，III 定理1.2.6证明中的局部计算')
attach(18,'06-kato-d.tex',r'只需在 $A=\mathbb Q[\Gal(L/K)]$','第二篇，III 定理1.2.6证明中的系数代数')
attach(19,'07-vojta-a.tex',r'\item 对秩为 $M$ 的 $M\times N$ 矩阵 $A$，定义 $h(A)$ 为由 $A$ 的所有 $M\times M$ 子式组成的向量的高度。','第三篇，定义2.3(d)及定理2.4')
ref(19,'07-vojta-a.tex',r'则其核有一组基 $\{\boldsymbol x_1,\ldots,\boldsymbol x_{N-M}\}$，满足')
attach(20,'07-vojta-a.tex','因此由 Hirzebruch Riemann--Roch 定理','第三篇，§7第一阶段的Riemann--Roch下界')
within(21,'07-vojta-a.tex',r'其中'+'\n'+r'\['+'\n'+r'0\le a+b\le d\delta_1', '其中','第三篇，§7第二阶段的单项式范围')
attach(22,'07-vojta-a.tex',r'在 $n$ 维复流形 $X$ 上固定一个测度 $\nu$。','第三篇，引理8.1')
attach(23,'07-vojta-a.tex','类似地，可把这一列延长为正合列','第三篇，Faltings复形(9.3)')
attach(24,'08-vojta-b.tex',r"使 $\gamma$ 的范数成为 $\mathcal O(e_1,\ldots,e_n)$ 的一个整截面 $\gamma'$",'第三篇，式(13.10)及推论18.3证明')
ref(24,'08-vojta-b.tex',r'故 $e_i=d_iN/N_i$。')
within(25,'08-vojta-b.tex','例如，\n'+r'\['+'\n'+r'\Gamma_1=\Gamma\!\left(\mathscr W,d(2n-2+\epsilon)', '例如','第三篇，命题14.1证明中的Γ₁')
attach(26,'08-vojta-b.tex','注意，此赋值不必离散。','第三篇，引理15.3及其前置设定')
ref(26,'08-vojta-b.tex','是一个多项式向量，并以')
attach(27,'08-vojta-b.tex',r'是由 $\mathbb C^m$ 到 $\mathbb C$ 的 $C^2$ 函数组成的向量','第三篇，引理15.8')
attach(28,'08-vojta-b.tex',r'并给定 $\epsilon_3>0$。','第三篇，定理18.1、推论18.3及式(18.2)、(18.4)')
ref(28,'08-vojta-b.tex',r'设 $\gamma$ 是 $\mathcal O(dL_{-\epsilon,s})$ 的一个非零\term{整体截面}{global section}{section globale}')
attach(29,'08-vojta-b.tex',r"于是消去分母后，$\gamma$ 的范数 $\gamma'$ 的度量满足",'第三篇，范数估计(18.5)及后续对数估计')

# 先保存修改前源码，再一次写入定位好的全部分块。
backup=ROOT/'annotations/before-translator-notes-2026-11-05.zip'
if not backup.exists():
    paths=list((ROOT/'chapters').glob('*.tex'))+[ROOT/n for n in ['main.tex','frontmatter.tex','reading-notes.tex','Makefile','README.txt']]
    with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
        for p in paths:z.write(p,p.relative_to(ROOT))
for name,text in sources.items():(ROOT/'chapters'/name).write_text(text)
(ROOT/'annotations/note-locations.json').write_text(json.dumps(locations,ensure_ascii=False,indent=2))
print(f'已按说明的原编号写入{len(locations)}条译者补注，并在相关的重复位置加入跳转提示。')
