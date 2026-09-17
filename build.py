# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import build_screen, CSS, HEAD, FOOT, esc
from screens_a import A
from screens_b import B
from screens_c import C, D
from screens_e import E, F

OUT = os.path.dirname(os.path.abspath(__file__))

PAGES = [
  ('page-1','1. 가입 · 로그인 · 인증', A),
  ('page-2','2. 홈 · 카드 관리',       B),
  ('page-3','3. 충전 · 잔액이전 · QR결제', C + D),
  ('page-4','4. 해외송금',            E),
  ('page-5','5. 거래내역 · MY · 설정 · 공통', F),
]

ALL = [s for _,_,g in PAGES for s in g]
stems = [s['f'] for s in ALL]
assert len(set(x.lower() for x in stems)) == len(stems), "중복 파일명"

# ---------- Main : 화면 맵 ----------
def build_main():
    cols = ''
    groups = [('1. 가입 · 로그인 · 인증',A),('2. 홈 · 카드 관리',B),('3. 충전 · 결제',C+D),('4. 해외송금 · 거래내역 · 설정',E+F)]
    for title, g in groups:
        items=''
        for s in g:
            cls = ' class="n"' if s['src']!='명세' else ''
            items += '<div class="mi"><b'+cls+'>'+esc(s['id'])+'</b>'+esc(s['name'])+'</div>'
        cols += '<div class="mapcol"><h3>'+esc(title)+'</h3>'+items+'</div>'
    body = ('<div class="mapwrap"><h1>송금 + 선불 통합 앱 — 화면 와이어프레임</h1>'
      '<p class="sub">「송금선불 통합 (정밀) 2026. 9. 16. 기능명세」의 42개 화면(SC-001~042)에, 명세서에서 이동 대상으로만 언급되고 정의가 없는 화면과 '
      '앱 서비스를 완성하는 데 필요한 화면을 더해 총 '+str(len(ALL))+'개 화면으로 구성했습니다.<br>'
      '화면 ID는 하나의 SC- 체계로 통합했습니다. <b>SC-001~SC-042</b>는 기능명세서의 번호를 그대로 유지하고, 보완한 화면은 <b>SC-043</b>부터 플로우 순서대로 이어서 부여했습니다.<br>'
      '상단 페이지 메뉴에서 플로우별로 이동할 수 있습니다. 각 화면 하단의 ACTION / EXCEPTION 블록에 명세서의 동작·예외를 그대로 옮겨 두었습니다.</p>'
      '<div class="mapgrid">'+cols+'</div>'
      '<div class="lg"><span><i>명세</i> 기능명세서에 정의된 화면</span><span><i>참조</i> 명세서에 이동 대상으로만 언급 — 신규 정의 필요</span>'
      '<span><i>추가</i> 앱 완성을 위해 보완한 화면 (SC-043~SC-098)</span><span>파란색 ID · 명세서에 없던 화면</span></div></div>')
    return HEAD % CSS + body + '\n' + FOOT

files = {}
files['Main.dc.html'] = build_main()
sizes = {}
for s in ALL:
    html, h = build_screen(s)
    files[s['f']+'.dc.html'] = html
    sizes[s['f']] = h

# ---------- canvas.json ----------
W, GAP_X, GAP_Y, PER_ROW = 390, 90, 150, 6
artboards = []
y_cursor = 0
# Main on page-1
MAIN_W, MAIN_H = 1180, 760
artboards.append({'file':'Main.dc.html','x':0,'y':0,'w':MAIN_W,'h':MAIN_H,'title':'개요 · 화면 맵','page':'page-1'})

page_y = {'page-1': MAIN_H + 200}
for pid, pname, grp in PAGES:
    y = page_y.get(pid, 0)
    for i in range(0, len(grp), PER_ROW):
        row = grp[i:i+PER_ROW]
        rowh = max(sizes[s['f']] for s in row)
        for j, s in enumerate(row):
            artboards.append({'file':s['f']+'.dc.html','x':j*(W+GAP_X),'y':y,
                              'w':W,'h':sizes[s['f']],'title':s['id']+'  '+s['name'],'page':pid})
        y += rowh + GAP_Y

annotations = [
 {'id':'note-flow-1','x':0,'y':MAIN_H+60,'w':1180,'page':'page-1',
  'text':'가입 플로우: 스플래시 → 홈(로그인 전) → 회원가입 → 유입설문 → 약관동의 → 휴대폰 본인인증 → 주소 → 기본정보 → eKYC(유스비) → 계좌 1원 인증 → 패턴 설정 → PIN 설정 → 가입 완료\n기가입 회원은 휴대폰 인증 단계에서 “이미 가입된 정보입니다.” 얼럿으로 분기하며, 통합 약관 재동의(A-011)를 거칩니다.'},
 {'id':'note-flow-2','x':0,'y':-110,'w':1180,'page':'page-2',
  'text':'카드 플로우: 홈 잔액합계 → 카드 관리 → 카드 상세 → (상세보기는 PIN 인증 경유) / 실물카드 등록은 QR 스캔 → 정보 확인 → 카드명 입력 → 등록 완료 순으로 진행됩니다.'},
 {'id':'note-flow-3','x':0,'y':-110,'w':1180,'page':'page-3',
  'text':'충전은 월렛 잔액에 가산되며, 카드에서 사용하려면 잔액이전(월렛↔카드)이 필요합니다. QR결제는 스캔 → 금액 입력 → 카드 선택 → PIN → 완료/실패 순서입니다.'},
 {'id':'note-flow-4','x':0,'y':-110,'w':1180,'page':'page-4',
  'text':'해외송금(E-001~E-008)은 기능명세서에 “송금 보내기(기존 디벙크송금) 화면으로 이동한다”로만 언급되어 있어 화면 정의가 없습니다. 기존 디벙크 송금 앱의 실제 화면과 대조해 확정이 필요합니다.'},
 {'id':'note-flow-5','x':0,'y':-110,'w':1180,'page':'page-5',
  'text':'MY(SC-037)에서 링크되는 9개 하위 화면(인증 및 보안·계좌 관리·알림 설정·언어 설정·공지사항·약관·ABOUT US·한도 조회)은 모두 명세서에 이동 대상만 있고 구성 정의가 없어 신규 정의했습니다.'},
]

canvas = {'artboards':artboards,'annotations':annotations,
          'pages':[{'id':p,'name':n} for p,n,_ in PAGES],
          'launch':{'view':'canvas','page':'page-1'}}
files['canvas.json'] = json.dumps(canvas, ensure_ascii=False, indent=2)

for name, content in files.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)

print('screens:', len(ALL), '| files:', len(files))
for pid, pname, grp in PAGES:
    print('  %-8s %-28s %d' % (pid, pname, len(grp)))
