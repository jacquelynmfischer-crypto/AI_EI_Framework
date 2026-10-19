"""Four original low-poly (faceted) robot characters for the AI EI personality types."""
import math, random
W, H = 600, 720

def hx(c): c=c.lstrip('#'); return [int(c[i:i+2],16) for i in (0,2,4)]
def shade(c, f):
    r,g,b=hx(c)
    if f>=1: r,g,b=[min(255,int(v+(255-v)*(f-1))) for v in (r,g,b)]
    else: r,g,b=[int(v*f) for v in (r,g,b)]
    return f'#{r:02x}{g:02x}{b:02x}'

TONES=[1.0,0.9,1.12,0.8,1.06,0.86,1.16,0.93]
def fan(pts, base, center=None, tones=TONES, stroke=True, ph=0):
    if center is None:
        center=(sum(p[0] for p in pts)/len(pts)+3, sum(p[1] for p in pts)/len(pts)-4)
    out=[]
    n=len(pts)
    for i in range(n):
        a,b=pts[i],pts[(i+1)%n]
        col=shade(base,tones[(i+ph)%len(tones)])
        out.append(f'<polygon points="{center[0]:.1f},{center[1]:.1f} {a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f}" fill="{col}" stroke="{col}" stroke-width="0.8" stroke-linejoin="round"/>')
    return ''.join(out)

def box(x,y,w,h,base,cut=14,ph=0):
    pts=[(x+cut,y),(x+w-cut,y),(x+w,y+cut),(x+w,y+h-cut),(x+w-cut,y+h),(x+cut,y+h),(x,y+h-cut),(x,y+cut)]
    return fan(pts,base,ph=ph)

def tri(pts,col): return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{col}" stroke="{col}" stroke-width="0.8" stroke-linejoin="round"/>'

def scene(bgtop, mount, snow, seed):
    random.seed(seed)
    s=f'<rect width="{W}" height="{H}" fill="{bgtop}"/>'
    # mountains
    peaks=[(-40,430,120,200,300,430),(180,430,330,150,520,430),(380,430,520,220,700,430)]
    for i,(x1,y1,x2,y2,x3,y3) in enumerate(peaks):
        s+=tri([(x1,y1),(x2,y2),(x3,y3)],shade(mount,1.0-0.06*i))
        s+=tri([(x2,y2),(x3,y3),(x2+20,y3)],shade(mount,0.84))
        s+=tri([(x2,y2),(x2-34,y2+60),(x2+30,y2+52)],'#f7fbff')
    # snow ground
    s+=f'<polygon points="0,430 600,430 600,{H} 0,{H}" fill="{snow}"/>'
    for i in range(14):
        x=random.randint(0,560); y=random.randint(450,700); w=random.randint(40,110)
        s+=tri([(x,y),(x+w,y+random.randint(-6,6)),(x+w/2,y+random.randint(14,26))],shade(snow,random.choice([0.95,0.9,1.0])))
    # pines
    for x,y,sc in [(40,470,1.0),(110,450,0.7),(520,470,1.05),(570,440,0.75),(470,445,0.65)]:
        s+=tri([(x-34*sc,y),(x+34*sc,y),(x,y-110*sc)],'#4f9a78')
        s+=tri([(x,y-110*sc),(x+34*sc,y),(x+4*sc,y)],'#3b7d60')
        s+=tri([(x-26*sc,y-50*sc),(x+26*sc,y-50*sc),(x,y-140*sc)],'#5cae88')
        s+=tri([(x,y-140*sc),(x+26*sc,y-50*sc),(x+3*sc,y-50*sc)],'#448a6b')
        s+=f'<rect x="{x-5*sc}" y="{y}" width="{10*sc}" height="{20*sc}" fill="#6b4a3a"/>'
    # rocks
    for x,y in [(60,640),(500,655)]:
        s+=fan([(x,y),(x+20,y-26),(x+58,y-34),(x+84,y-4),(x+60,y+14),(x+10,y+14)],'#b9c2cc')
    return s

def robot(body, light, dark, plate, accent, eyes, ant, prop, torso_icon, mouth=''):
    s=f'<ellipse cx="300" cy="668" rx="130" ry="16" fill="#8aa0b5" opacity=".35"/>'
    # legs
    s+=box(226,548,50,92,dark,cut=10)+box(324,548,50,92,dark,cut=10)
    s+=fan([(208,632),(284,632),(292,660),(204,660)],body)+fan([(316,632),(392,632),(396,660),(308,660)],body,ph=2)
    # arms
    s+=fan([(150,392),(184,386),(168,500),(128,494)],dark,ph=1)+fan([(416,386),(450,392),(472,494),(432,500)],dark,ph=3)
    s+=fan([(124,494),(172,500),(166,536),(128,534)],body,ph=2)+fan([(428,500),(476,494),(472,534),(434,536)],body,ph=4)
    # torso
    s+=fan([(186,372),(414,372),(436,440),(410,560),(190,560),(164,440)],body)
    s+=fan([(236,404),(364,404),(378,480),(222,480)],plate,ph=1)
    s+=torso_icon
    # neck + head
    s+=box(270,340,60,40,dark,cut=8)
    head=[(196,160),(404,160),(454,206),(454,296),(412,350),(188,350),(146,296),(146,206)]
    s+=fan(head,body,center=(300,246))
    s+=box(112,214,38,78,dark,cut=10)+box(450,214,38,78,dark,cut=10)
    face=[(206,190),(394,190),(424,222),(424,288),(392,326),(208,326),(176,288),(176,222)]
    s+=fan(face,plate,center=(300,258),tones=[1.0,0.93,1.05,0.9,1.02,0.95,1.06,0.92])
    s+=eyes+mouth+ant+prop
    return s

def diamond(cx,cy,r,col): return tri([(cx,cy-r),(cx+r,cy),(cx,cy+r)],col)+tri([(cx,cy-r),(cx-r,cy),(cx,cy+r)],shade(col,0.8))
def hexeye(cx,cy,r,col):
    pts=[(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a))) for a in range(0,360,60)]
    return fan(pts,col,center=(cx,cy))
def svg(inner): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><clipPath id="c"><rect width="{W}" height="{H}" rx="30"/></clipPath></defs><g clip-path="url(#c)">{inner}</g></svg>'

chars=[]
# 1 Verifier: Claude orange + cream
O,Ol,Od,Cr,Dk="#D97757","#F2A27F","#A8502F","#FAF0E2","#5A2E1E"
eyes=hexeye(256,258,22,Dk)+hexeye(344,258,22,Dk)+tri([(246,246),(256,236),(262,248)],'#fff')+tri([(334,246),(344,236),(350,248)],'#fff')
mouth=tri([(272,298),(328,298),(300,314)],Dk)
ant=box(292,100,16,60,Dk,cut=4)+fan([(300,56),(330,78),(322,112),(278,112),(270,78)],Cr,center=(300,86))+f'<polyline points="284,86 297,100 318,72" fill="none" stroke="{O}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
icon=f'<polyline points="262,440 290,466 340,414" fill="none" stroke="{O}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
glass=fan([(430,430),(466,418),(500,444),(502,484),(468,508),(432,492)],Cr,center=(468,462))+fan([(442,440),(466,432),(490,450),(490,478),(468,494),(444,484)],'#bfe3f2',center=(466,464),tones=[1.0,.94,1.06,.9])+tri([(488,496),(506,484),(548,540)],Dk)+tri([(496,500),(506,484),(552,548),(536,552)],shade(Dk,.8))
chars.append(('1_the_verifier',scene('#F3E3D7','#E7B79D','#FBF3EA',1)+robot(O,Ol,Od,Cr,Dk,eyes,ant,glass,icon,mouth)))

# 2 Hedger: GPT green + white
G,Gl,Gd,Wh,Dg="#10A37F","#59CDAB","#0B6B54","#F3FBF8","#0A4A3B"
eyes=hexeye(256,258,22,Dg)+tri([(318,238),(372,222),(372,236),(318,250)],Dg)+hexeye(346,262,16,Dg)+tri([(250,240),(262,230),(266,244)],'#fff')
mouth=f'<polyline points="270,306 286,296 302,306 318,296 334,306" fill="none" stroke="{Dg}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
ant=f'<polyline points="300,160 300,128 336,104" fill="none" stroke="{Dg}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'+fan([(340,62),(370,78),(370,112),(340,128),(310,112),(310,78)],Wh,center=(340,95))+f'<text x="340" y="108" font-family="Georgia,serif" font-size="40" font-weight="bold" text-anchor="middle" fill="{G}">?</text>'
icon=f'<polyline points="258,462 300,430 342,462" fill="none" stroke="{G}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><polyline points="258,436 300,404 342,436" fill="none" stroke="{Gl}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" opacity=".0"/>'
bub=fan([(24,66),(54,36),(196,36),(226,66),(226,116),(196,146),(112,146),(80,182),(84,146),(54,146),(24,116)],Wh,center=(124,92),tones=[1.0,.97,1.03,.95,1.0,.97,1.02,.96,1.0,.98,1.0])+f'<text x="125" y="104" font-family="Georgia,serif" font-size="34" font-style="italic" text-anchor="middle" fill="{Dg}">maybe…</text>'
chars.append(('2_the_hedger',scene('#DDF2EA','#9BD4C0','#F5FBF8',2)+robot(G,Gl,Gd,Wh,Dg,eyes,ant,bub,icon,mouth)))

# 3 Pragmatist: DeepSeek blue + white
B,Bl,Bd,W3,Dn="#4D6BFE","#8FA2FF","#2E43C4","#F2F5FF","#16227A"
eyes=tri([(224,246),(290,246),(290,278),(236,278)],Dn)+tri([(310,246),(376,246),(364,278),(310,278)],Dn)+tri([(236,254),(264,254),(264,266),(240,266)],'#B7C5FF')+tri([(322,254),(350,254),(346,266),(322,266)],'#B7C5FF')+f'<polyline points="204,222 290,242" stroke="{Dn}" stroke-width="12" stroke-linecap="round"/><polyline points="396,222 310,242" stroke="{Dn}" stroke-width="12" stroke-linecap="round"/>'
mouth=f'<line x1="266" y1="304" x2="334" y2="304" stroke="{Dn}" stroke-width="10" stroke-linecap="round"/>'
bolt=tri([(318,40),(276,106),(304,106),(288,150),(340,84),(312,84)],'#FFD84D')+tri([(318,40),(312,84),(340,84)],'#E8B923')
ant=f'<line x1="300" y1="160" x2="300" y2="138" stroke="{Dn}" stroke-width="14" stroke-linecap="round"/>'+bolt
icon=f'<polyline points="262,420 338,420" stroke="{B}" stroke-width="12" stroke-linecap="round"/><polyline points="262,448 316,448" stroke="{B}" stroke-width="12" stroke-linecap="round"/>'
arrow=fan([(420,440),(470,440),(470,418),(520,462),(470,506),(470,484),(420,484)],W3,center=(468,462))
wrench=fan([(70,520),(94,540),(150,456),(126,438)],Dn)+fan([(120,418),(150,424),(162,452),(142,462),(130,446),(112,444),(104,430)],W3,center=(134,438))
chars.append(('3_the_decisive_pragmatist',scene('#E1E7FF','#A9B8F5','#F6F8FF',3)+robot(B,Bl,Bd,W3,Dn,eyes,ant,arrow+wrench,icon,mouth)))

# 4 Generalist: Grok black + white
K,Kl,Kd,Wt,Kk="#1C1F26","#4A505C","#0A0B0E","#FFFFFF","#000000"
eyes=hexeye(256,258,26,Wt)+hexeye(344,258,26,Wt)+hexeye(262,256,12,Kk)+hexeye(350,256,12,Kk)
mouth=fan([(250,294),(350,294),(332,322),(268,322)],Wt,center=(300,302),tones=[1,.9,1.05,.85])+f'<line x1="268" y1="302" x2="332" y2="302" stroke="{K}" stroke-width="4"/>'
ant=f'<line x1="300" y1="160" x2="300" y2="122" stroke="#8F95A0" stroke-width="14" stroke-linecap="round"/>'+fan([(300,66),(322,80),(322,106),(300,120),(278,106),(278,80)],Wt,center=(300,94))+f'<line x1="300" y1="80" x2="300" y2="108" stroke="{K}" stroke-width="7" stroke-linecap="round"/><line x1="286" y1="94" x2="314" y2="94" stroke="{K}" stroke-width="7" stroke-linecap="round"/>'
icon=f'<polyline points="258,424 300,456 342,424" fill="none" stroke="{Wt}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
mega=fan([(430,432),(520,396),(520,520),(430,484)],Wt,center=(480,460))+fan([(398,436),(432,436),(432,480),(398,480)],K,center=(414,458))+f'<polyline points="536,420 560,404 M536,458 566,458 M536,496 560,512" fill="none" stroke="{K}" stroke-width="8" stroke-linecap="round"/>'
globe=fan([(70,420),(106,404),(142,420),(150,460),(130,496),(94,500),(66,474),(62,440)],Wt,center=(106,452))+f'<polyline points="64,450 148,450" stroke="{K}" stroke-width="5"/><polyline points="106,402 90,450 106,498" fill="none" stroke="{K}" stroke-width="5"/><polyline points="106,402 122,450 106,498" fill="none" stroke="{K}" stroke-width="5"/>'
chars.append(('4_the_confident_generalist',scene('#E6E8EB','#B9BFC9','#F7F8F9',4)+robot(K,Kl,Kd,Kd,Wt,eyes,ant,f'<g transform="translate(-26 0)">{mega}</g>'+globe,icon,mouth)))

for name,inner in chars: open(f'{name}.svg','w').write(svg(inner))
print('ok')
