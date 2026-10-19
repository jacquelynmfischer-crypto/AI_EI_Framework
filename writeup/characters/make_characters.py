"""Four original low-poly (faceted) robot characters for the AI EI personality types, v2:
distinct silhouettes, poses and large props."""
import math, random
W, H = 600, 720

def hx(c): c=c.lstrip('#'); return [int(c[i:i+2],16) for i in (0,2,4)]
def shade(c, f):
    r,g,b=hx(c)
    if f>=1: r,g,b=[min(255,int(v+(255-v)*(f-1))) for v in (r,g,b)]
    else: r,g,b=[int(v*f) for v in (r,g,b)]
    return f'#{r:02x}{g:02x}{b:02x}'
T=[1.0,0.9,1.12,0.8,1.06,0.86,1.16,0.93]
def P(pts): return " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
def tri(pts,col): return f'<polygon points="{P(pts)}" fill="{col}" stroke="{col}" stroke-width="0.8" stroke-linejoin="round"/>'
def fan(pts, base, center=None, tones=T, ph=0):
    n=len(pts)
    if center is None: center=(sum(p[0] for p in pts)/n+3, sum(p[1] for p in pts)/n-4)
    return ''.join(tri([center,pts[i],pts[(i+1)%n]],shade(base,tones[(i+ph)%len(tones)])) for i in range(n))
def box(x,y,w,h,base,cut=12,ph=0):
    return fan([(x+cut,y),(x+w-cut,y),(x+w,y+cut),(x+w,y+h-cut),(x+w-cut,y+h),(x+cut,y+h),(x,y+h-cut),(x,y+cut)],base,ph=ph)
def hexpoly(cx,cy,r,rot=0): return [(cx+r*math.cos(math.radians(a+rot)),cy+r*math.sin(math.radians(a+rot))) for a in range(0,360,60)]
def hexeye(cx,cy,r,col): return fan(hexpoly(cx,cy,r),col,center=(cx,cy))
def limb(a,b,w,base):
    (x1,y1),(x2,y2)=a,b; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1; nx,ny=-dy/L*w/2,dx/L*w/2
    p1,p2,p3,p4=(x1+nx,y1+ny),(x2+nx,y2+ny),(x2-nx,y2-ny),(x1-nx,y1-ny)
    return tri([p1,p2,a if False else ((x2),(y2))],shade(base,1.12))+tri([p1,(x2,y2),(x1,y1)],shade(base,1.12))+tri([(x1,y1),(x2,y2),p3],shade(base,0.82))+tri([(x1,y1),p3,p4],shade(base,0.82))
def joint(c,r,col): return fan(hexpoly(c[0],c[1],r),col,center=c)
def hand(c,r,col): return fan(hexpoly(c[0],c[1],r,30),col,center=c)
def arm(sh,el,ha,w,base,hcol):
    return limb(sh,el,w,base)+limb(el,ha,w*0.9,base)+joint(el,w*0.6,hcol)+hand(ha,w*0.85,hcol)
def svg(inner,extra=''): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><clipPath id="c"><rect width="{W}" height="{H}" rx="30"/></clipPath></defs><g clip-path="url(#c)">{inner}</g></svg>'

def scene(bgtop, mount, snow, seed, trees=True):
    random.seed(seed)
    s=f'<rect width="{W}" height="{H}" fill="{bgtop}"/>'
    for i,(x1,x2,x3,y2) in enumerate([(-40,120,300,200),(180,330,520,150),(380,520,700,220)]):
        s+=tri([(x1,430),(x2,y2),(x3,430)],shade(mount,1.0-0.06*i))+tri([(x2,y2),(x3,430),(x2+20,430)],shade(mount,0.84))+tri([(x2,y2),(x2-34,y2+60),(x2+30,y2+52)],'#f7fbff')
    s+=f'<polygon points="0,430 600,430 600,{H} 0,{H}" fill="{snow}"/>'
    for i in range(14):
        x=random.randint(0,560); y=random.randint(450,700); w=random.randint(40,110)
        s+=tri([(x,y),(x+w,y+random.randint(-6,6)),(x+w/2,y+random.randint(14,26))],shade(snow,random.choice([0.95,0.9,1.0])))
    if trees:
        for x,y,sc in [(40,470,1.0),(104,448,0.66),(548,462,1.0),(488,444,0.62)]:
            s+=tri([(x-34*sc,y),(x+34*sc,y),(x,y-110*sc)],'#4f9a78')+tri([(x,y-110*sc),(x+34*sc,y),(x+4*sc,y)],'#3b7d60')+tri([(x-26*sc,y-50*sc),(x+26*sc,y-50*sc),(x,y-140*sc)],'#5cae88')+tri([(x,y-140*sc),(x+26*sc,y-50*sc),(x+3*sc,y-50*sc)],'#448a6b')+f'<rect x="{x-5*sc}" y="{y}" width="{10*sc}" height="{20*sc}" fill="#6b4a3a"/>'
    return s
def shadow(cx=300,rx=130): return f'<ellipse cx="{cx}" cy="676" rx="{rx}" ry="15" fill="#6f879c" opacity=".35"/>'
def foot(x,y,w,col,flip=1): return fan([(x,y),(x+w*flip,y),(x+(w+10)*flip,y+28),(x-8*flip,y+28)],col)
def tx(x,y,t,size,col,style='normal',weight='bold',anchor='middle',fam='Georgia,serif'): return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-style="{style}" font-weight="{weight}" text-anchor="{anchor}" fill="{col}">{t}</text>'
chars=[]

# ---------- 1 VERIFIER (orange/cream): tall, upright, inspects a checklist with a big magnifier
O,Ol,Od,Cr,Dk="#D97757","#F2A27F","#A8502F","#FAF0E2","#5A2E1E"
s=scene('#F3E3D7','#E7B79D','#FBF3EA',1)+shadow()
s+=box(236,520,46,120,Od,cut=8)+box(318,520,46,120,Od,cut=8)+foot(222,636,70,O)+foot(308,636,70,O)
s+=fan([(222,372),(378,372),(392,440),(374,540),(226,540),(208,440)],O)                      # slim torso
s+=fan([(246,404),(354,404),(364,470),(236,470)],Cr,ph=1)+f'<polyline points="262,436 290,460 338,414" fill="none" stroke="{O}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
s+=box(272,338,56,40,Dk,cut=8)
# clipboard held at left, pen-checking
cb=fan([(70,408),(206,408),(206,596),(70,596)],"#8a5a3c",center=(138,500))+fan([(82,430),(194,430),(194,584),(82,584)],Cr,center=(138,506),tones=[1,.97,1.03,.96])+box(110,396,56,28,'#B0B6BF',cut=6)
for i,yy in enumerate((460,498,536)):
    cb+=f'<polyline points="96,{yy} 106,{yy+10} 124,{yy-10}" fill="none" stroke="{O}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><line x1="136" y1="{yy}" x2="182" y2="{yy}" stroke="{Dk}" stroke-width="6" stroke-linecap="round"/>'
s+=arm((226,392),(184,452),(154,500),30,O,Ol)+cb
# head
s+=fan([(190,168),(410,168),(446,216),(446,300),(404,346),(196,346),(154,300),(154,216)],O,center=(300,252))
s+=box(120,224,36,70,Dk,cut=8)+box(444,224,36,70,Dk,cut=8)
s+=fan([(204,194),(396,194),(424,224),(424,290),(392,326),(208,326),(176,290),(176,224)],Cr,center=(300,260),tones=[1,.94,1.05,.9,1.02,.95,1.06,.92])
for cx in (256,344): s+=fan(hexpoly(cx,262,36),'#cfe7f0',center=(cx,262),tones=[1.0,.92,1.05,.9,1.02,.95])+fan(hexpoly(cx,262,36),Dk,center=(cx,262),tones=[1])*0 + f'<polygon points="{P(hexpoly(cx,262,36))}" fill="none" stroke="{Dk}" stroke-width="7" stroke-linejoin="round"/>'+hexeye(cx,262,14,Dk)+tri([(cx-6,254),(cx,247),(cx+4,256)],'#fff')
s+=f'<line x1="292" y1="262" x2="308" y2="262" stroke="{Dk}" stroke-width="6"/>'+tri([(276,306),(324,306),(300,318)],Dk)
s+=box(293,104,14,64,Dk,cut=4)+fan(hexpoly(300,84,28),Cr,center=(300,84))+f'<polyline points="288,84 297,96 314,72" fill="none" stroke="{O}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
# big magnifier held up on the right, lens over checklist-like page
s+=arm((380,394),(446,448),(486,396),30,O,Ol)
lens_c=(506,318)
s+=limb((488,382),(520,340),20,Dk)
s+=fan(hexpoly(lens_c[0],lens_c[1],74,0),Dk,center=lens_c)+fan(hexpoly(lens_c[0],lens_c[1],58,0),'#cfeaf6',center=(lens_c[0]-4,lens_c[1]-6),tones=[1.1,.95,1.06,.9,1.02,.97])+tri([(lens_c[0]-30,lens_c[1]-24),(lens_c[0]-6,lens_c[1]-38),(lens_c[0]-18,lens_c[1]-8)],'#ffffff')
s+=f'<polyline points="{lens_c[0]-24},{lens_c[1]+6} {lens_c[0]-6},{lens_c[1]+26} {lens_c[0]+28},{lens_c[1]-18}" fill="none" stroke="{O}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
chars.append(('1_the_verifier',svg(s)))

# ---------- 2 HEDGER (green/white): round, squat, shrugging, head tilted, signpost pointing both ways
G,Gl,Gd,Wh,Dg="#10A37F","#59CDAB","#0B6B54","#F3FBF8","#0A4A3B"
s=scene('#DDF2EA','#9BD4C0','#F5FBF8',2)+shadow(280,150)
# signpost at right
s+=box(532,500,16,150,'#8a6a4a',cut=4)
s+=fan([(466,526),(530,526),(552,548),(530,570),(466,570)],Wh,center=(508,548),tones=[1,.95,1.05,.92,1.0])+tx(504,558,'yes?',24,Dg,'italic')
s+=fan([(592,584),(548,584),(534,604),(548,624),(592,624)],Wh,center=(564,604),tones=[1,.95,1.05,.92,1.0])+tx(568,613,'no?',22,Dg,'italic')
# legs short
s+=box(208,560,52,84,Gd,cut=8)+box(340,560,52,84,Gd,cut=8)+foot(192,640,82,G)+foot(326,640,82,G)
# pear body
s+=fan([(206,400),(394,400),(450,470),(458,560),(300,600),(142,560),(150,470)],G,center=(300,500))
s+=fan([(228,448),(372,448),(396,540),(204,540)],Wh,ph=1)+f'<polyline points="256,500 300,470 344,500" fill="none" stroke="{G}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><polyline points="262,520 300,498 338,520" fill="none" stroke="{Gl}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
# shrug arms: elbows out low, hands up palms open
s+=arm((190,424),(108,476),(76,404),32,G,Gl)+arm((410,424),(492,476),(524,404),32,G,Gl)
# head (tilted)
hd=box(176,176,248,164,G,cut=44)+box(130,216,40,70,Gd,cut=10)+box(430,216,40,70,Gd,cut=10)
hd+=fan([(202,200),(398,200),(414,226),(414,290),(390,318),(210,318),(186,290),(186,226)],Wh,center=(300,258),tones=[1,.94,1.05,.9,1.02,.95,1.06,.92])
hd+=hexeye(256,256,22,Dg)+tri([(250,238),(262,228),(266,242)],'#fff')+tri([(322,240),(376,222),(376,236),(322,252)],Dg)+hexeye(348,266,16,Dg)
hd+=f'<polyline points="262,300 282,288 302,300 322,288 342,300" fill="none" stroke="{Dg}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
hd+=f'<polyline points="300,176 300,140 336,116" fill="none" stroke="{Dg}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'+fan(hexpoly(342,92,30),Wh,center=(342,92))+tx(342,106,'?',40,G)
s+=box(272,340,56,34,Gd,cut=8)+f'<g transform="rotate(-9 300 330)">{hd}</g>'
# thought cloud of caveats
cl=fan([(44,70),(72,36),(150,28),(214,40),(250,78),(232,126),(168,142),(90,138),(48,112)],Wh,center=(148,86),tones=[1,.97,1.03,.95,1.0,.97,1.02,.96])
cl+=tx(146,66,'maybe…',24,Dg,'italic')+tx(146,92,'unless…',24,Dg,'italic')+tx(146,118,'if…',24,Dg,'italic')+fan(hexpoly(236,164,10),Wh,center=(236,164))+fan(hexpoly(262,194,6),Wh,center=(262,194))
s+=cl
chars.append(('2_the_hedger',svg(s)))

# ---------- 3 PRAGMATIST (blue/white/yellow): mid-stride, hard hat, wrench on shoulder, toolbox
B,Bl,Bd,W3,Dn="#4D6BFE","#8FA2FF","#2E43C4","#F2F5FF","#16227A"
Y,Yd="#FFD84D","#E0AC1C"
s=scene('#E1E7FF','#A9B8F5','#F6F8FF',3)+shadow(300,150)
# speed lines
for yy,ln in [(420,70),(470,100),(520,60),(570,90)]: s+=f'<line x1="{20}" y1="{yy}" x2="{20+ln}" y2="{yy}" stroke="{Bl}" stroke-width="7" stroke-linecap="round" opacity=".7"/>'
g=''
# back leg & front leg (stride)
g+=limb((262,540),(226,600),46,Bd)+box(176,596,70,34,B,cut=8)
g+=limb((338,540),(386,590),46,Bd)+box(372,586,90,36,B,cut=8)
# torso: broad shoulders, tapered
g+=fan([(160,378),(440,378),(402,470),(386,556),(214,556),(198,470)],B,center=(300,456))
g+=fan([(238,420),(362,420),(362,486),(238,486)],W3,ph=1)+f'<line x1="258" y1="440" x2="342" y2="440" stroke="{B}" stroke-width="11" stroke-linecap="round"/><line x1="258" y1="466" x2="320" y2="466" stroke="{B}" stroke-width="11" stroke-linecap="round"/>'
# swinging back arm with toolbox
g+=arm((176,402),(126,456),(104,520),34,B,Bl)
tb=fan([(52,520),(160,520),(166,600),(46,600)],Y,center=(104,566))+box(84,500,40,24,Yd,cut=6)+f'<line x1="46" y1="552" x2="166" y2="552" stroke="{Yd}" stroke-width="7"/>'+fan(hexpoly(104,566,12),Dn,center=(104,566))
g+=tb
# head: squarer, narrower, hard hat
g+=box(274,340,52,40,Dn,cut=8)
g+=fan([(206,178),(394,178),(420,214),(420,300),(386,348),(214,348),(180,300),(180,214)],B,center=(300,262))
g+=box(150,230,34,62,Dn,cut=8)+box(416,230,34,62,Dn,cut=8)
g+=fan([(214,206),(386,206),(404,232),(404,296),(378,326),(222,326),(196,296),(196,232)],W3,center=(300,268),tones=[1,.94,1.05,.9,1.02,.95,1.06,.92])
g+=tri([(222,254),(292,254),(292,286),(236,286)],Dn)+tri([(308,254),(378,254),(364,286),(308,286)],Dn)+tri([(236,262),(266,262),(266,274),(240,274)],'#B7C5FF')+tri([(322,262),(352,262),(346,274),(322,274)],'#B7C5FF')
g+=f'<polyline points="208,230 292,252" stroke="{Dn}" stroke-width="12" stroke-linecap="round"/><polyline points="392,230 308,252" stroke="{Dn}" stroke-width="12" stroke-linecap="round"/><line x1="268" y1="308" x2="336" y2="308" stroke="{Dn}" stroke-width="10" stroke-linecap="round"/>'
# hard hat
g+=fan([(190,196),(206,140),(300,112),(394,140),(410,196)],Y,center=(300,160),tones=[1.05,.95,1.12,.85,1.0])+fan([(168,196),(432,196),(446,214),(154,214)],Yd,center=(300,205),tones=[1,.9,1.1,.95])
g+=tri([(300,126),(316,172),(284,172)],Yd)+tri([(322,134),(298,168),(326,168)],B)
# front arm: wrench raised over shoulder
g+=arm((424,402),(480,440),(468,380),34,B,Bl)
g+=limb((466,384),(520,250),22,Dn)+fan([(486,208),(522,196),(550,214),(552,250),(534,268),(520,244),(504,244),(494,262),(476,248),(474,222)],W3,center=(514,232),tones=[1,.9,1.1,.85,1.0,.9,1.05,.95,1.0,.9])
s+=f'<g transform="rotate(5 300 400)">{g}</g>'
chars.append(('3_the_decisive_pragmatist',svg(s)))

# ---------- 4 GENERALIST (black/white): big dome head, skinny, leaning back, shouting into a megaphone, orbiting icons
K,Kl,Kd,Wt,Kk="#1C1F26","#4A505C","#0A0B0E","#FFFFFF","#000000"
Gy="#8F95A0"
s=scene('#E6E8EB','#B9BFC9','#F7F8F9',4)+shadow(290,120)
g=''
# skinny legs, one up on tiptoe
g+=limb((262,546),(250,626),22,Kd)+limb((338,546),(364,616),22,Kd)+foot(222,624,64,K)+fan([(344,616),(408,622),(414,646),(340,642)],K)
# small slim torso
g+=fan([(236,396),(364,396),(380,470),(352,552),(248,552),(220,470)],K,center=(300,470))
g+=fan([(262,424),(338,424),(338,486),(262,486)],Kl,ph=2)+f'<polyline points="270,444 300,472 330,444" fill="none" stroke="{Wt}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
# globe arm (left, held out palm up)
g+=arm((236,412),(164,450),(124,424),24,Kl,Wt)
gl=fan(hexpoly(110,370,50),Wt,center=(104,364),tones=[1,.9,1.06,.86,1.0,.94])+f'<polyline points="60,370 160,370" stroke="{K}" stroke-width="5"/><polyline points="110,320 88,370 110,420" fill="none" stroke="{K}" stroke-width="5"/><polyline points="110,320 134,370 110,420" fill="none" stroke="{K}" stroke-width="5"/>'
g+=gl
# neck and BIG round head
g+=box(278,356,44,40,Kd,cut=6)
g+=fan([(190,150),(300,118),(410,150),(450,240),(420,330),(300,364),(180,330),(150,240)],K,center=(300,244),tones=[1.0,.88,1.14,.8,1.08,.86,1.18,.93])
g+=box(120,214,36,64,Kd,cut=8)+box(444,214,36,64,Kd,cut=8)
g+=fan([(202,188),(398,188),(424,236),(398,312),(300,334),(202,312),(176,236)],Kd,center=(300,252),tones=[1,.9,1.06,.8,1.02,.92,1.0])
g+=hexeye(252,246,32,Wt)+hexeye(348,246,32,Wt)+hexeye(260,244,14,Kk)+hexeye(356,244,14,Kk)
g+=fan([(240,284),(360,284),(340,324),(260,324)],Wt,center=(300,296),tones=[1,.9,1.05,.85])+f'<line x1="262" y1="302" x2="338" y2="302" stroke="{K}" stroke-width="4"/>'
g+=f'<line x1="300" y1="122" x2="300" y2="82" stroke="{Gy}" stroke-width="14" stroke-linecap="round"/>'+fan(hexpoly(300,58,26),Wt,center=(300,58))+f'<line x1="300" y1="44" x2="300" y2="72" stroke="{K}" stroke-width="7" stroke-linecap="round"/><line x1="286" y1="58" x2="314" y2="58" stroke="{K}" stroke-width="7" stroke-linecap="round"/>'
# right arm raising megaphone to mouth (pointing right, up)
g+=arm((364,412),(420,448),(430,372),24,Kl,Wt)
mg=fan([(404,268),(404,330),(470,372),(470,226)],Wt,center=(440,298),tones=[1,.9,1.06,.86])+box(366,282,44,34,Kd,cut=6)+f'<polyline points="470,252 500,230 M470,300 512,300 M470,346 500,368" fill="none" stroke="{K}" stroke-width="9" stroke-linecap="round"/>'
g+=mg
s+=f'<g transform="rotate(-4 300 400)">{g}</g>'
# orbiting icons bursting out of the megaphone
for (cx,cy,ch) in [(536,196,'?'),(566,288,'✓'),(540,392,'★'),(470,150,'!'),(120,200,'♪'),(70,270,'?')]:
    s+=fan(hexpoly(cx,cy,26),Wt,center=(cx,cy))+f'<polygon points="{P(hexpoly(cx,cy,26))}" fill="none" stroke="{K}" stroke-width="4" stroke-linejoin="round"/>'+tx(cx,cy+11,ch,30,K,fam='Arial,sans-serif')
chars.append(('4_the_confident_generalist',svg(s)))

for name,inner in chars: open(f'{name}.svg','w').write(inner)
print('ok')
