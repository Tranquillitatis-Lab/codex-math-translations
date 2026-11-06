from pathlib import Path
import subprocess
P=Path(__file__).resolve().parents[1]
src=next(P.parent.glob('10 *.pdf'))
# Crop only mathematical diagrams; no prose or English column headings.
# Coordinates below refer to the 1750-high source rendering.
rows={66:[(840,1080),(1090,1300),(1310,1495)],67:[(300,455),(460,645),(650,875),(880,1087),(1095,1282),(1290,1497)],68:[(288,480),(490,675),(685,940),(948,1140),(1150,1310),(1320,1495)],69:[(291,495),(505,636),(648,860),(872,1120),(1130,1332),(1340,1475)],70:[(288,435),(445,605),(620,820),(830,995),(1010,1158),(1170,1330),(1342,1510)]}
for page,bounds in rows.items():
 for j,(top,bottom) in enumerate(bounds,1):
  # mathematical local index / relative diagram center column only
  x0=465 if page in (66,67,68) else 450
  x1=905 if page==66 else (815 if page==67 else (830 if page==68 else 805))
  scale=3000/1750
  prefix=P/'figures'/f'02-class-{page}-{j}'
  subprocess.run(['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','3000','-x',str(round(x0*scale)),'-y',str(round(top*scale)),'-W',str(round((x1-x0)*scale)),'-H',str(round((bottom-top)*scale)),'-png',str(src),str(prefix)],check=True)
