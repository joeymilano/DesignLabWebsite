"""Import the supplied 2026 offer workbook without publishing the workbook itself."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path
import openpyxl
ROOT = Path(__file__).resolve().parent.parent
SCHOOL_NAMES = {
 'University of Leeds':'leeds','University of Southampton':'southampton',
 'University of Glasgow':'glasgow','University of Bristol':'bristol',
 'The University of Manchester':'manchester','University of Birmingham':'birmingham',
 'The University of Sheffield':'sheffield','The University of Nottingham':'nottingham',
 'Durham University':'durham','The University of Warwick':'warwick',"King's College London":'kcl',
}
NEW_SCHOOLS = [
 ('manchester','曼彻斯特大学','The University of Manchester','https://www.manchester.ac.uk/','https://assets.manchester.ac.uk/corporate/images/design/logo-university-of-manchester.png','png'),
 ('southampton','南安普顿大学','University of Southampton','https://www.southampton.ac.uk/','https://www.southampton.ac.uk/themes/custom/drupal_endeavour/images/logo/logo-uk.svg','svg'),
 ('birmingham','伯明翰大学','University of Birmingham','https://www.birmingham.ac.uk/','https://www.birmingham.ac.uk/Images/logos/uob/uob-uk-logo-light.svg','svg'),
 ('nottingham','诺丁汉大学','University of Nottingham','https://www.nottingham.ac.uk/','https://www.nottingham.ac.uk/etc.clientlibs/uon/clientlibs/clientlib-v2/resources/images/UoN-Logo-Dark.svg','svg'),
 ('durham','杜伦大学','Durham University','https://www.durham.ac.uk/','https://dur.ac.uk/media/durham-university/site-assets/image/logo-dark.svg','svg'),
 ('kcl','伦敦国王学院',"King's College London",'https://www.kcl.ac.uk/','https://www.kcl.ac.uk/SiteElements/2017/images/kcl-logo.svg','svg'),
]
def value(v):
 if v is None:return '未提供'
 if isinstance(v,(int,float)):
  if 0<v<1:return f'{v*100:.2f}'.rstrip('0').rstrip('.')+'%'
  return f'{v:g}'
 return str(v).strip()
def category(program):
 p=program.lower()
 if any(x in p for x in ['architecture','landscape','urban','cities','transport planning']):return 'urban'
 if any(x in p for x in ['fashion','textile']):return 'fashion'
 if 'systems design management' in p or any(x in p for x in ['communication networks','communications engineering','wireless communication','signal processing']):return 'other'
 if any(x in p for x in ['design','immersive','games','human computer interaction','human-computer interaction','creative technologies']):return 'design'
 if any(x in p for x in ['media','communication','digital culture','digital humanities','film','photography','journalism','advertising']):return 'media'
 if any(x in p for x in ['creative','culture','cultural','arts management','museum','music','fine art','performance','curation']):return 'culture'
 return 'other'
def build(source):
 existing=json.loads((ROOT/'assets/site/admissions/2027.json').read_text())
 schools=existing['schools']
 for s in schools:s['logo']=f'/assets/site/admissions/{s["id"]}.svg'
 schools += [dict(id=k,zh=zh,en=en,url=url,logoSource=logo,logo=f'/assets/site/admissions/{k}.{ext}') for k,zh,en,url,logo,ext in NEW_SCHOOLS]
 workbook=openpyxl.load_workbook(source,data_only=True,read_only=True)
 sheet=workbook.worksheets[0]
 rows=list(sheet.values)
 assert rows[1]==('序号','毕业/就读院校','毕业/就读专业','毕业时间','平均成绩','入学年份','入学季度','申请院校','申请专业','申请结果','Offer条件'),'Unexpected columns'
 new=[];raw=[]
 for rownum,r in enumerate(rows,1):
  if not isinstance(r[0],(int,float)):continue
  assert int(r[5])==2026 and r[9]=='CO' and all(v is not None for v in r),rownum
  school=SCHOOL_NAMES[r[7]]
  new.append(dict(id=f'2026-{school}-{int(r[0]):03}',school=school,origin=value(r[1]),degree='未提供',major=value(r[2]),graduationDate=r[3].date().isoformat(),grade=value(r[4]),year=value(r[5]),season=value(r[6]),program=value(r[8]),result=value(r[9]),condition=value(r[10]),category=category(value(r[8])),source='2026-uk-offers',sourceRow=rownum))
  raw.append(r)
 assert len(new)==900 and len({c['id'] for c in new})==900
 assert len(set(r[1:] for r in raw))==900,'Review duplicate source profiles'
 cases=existing['cases']+new
 # Keep historical cases and their established categories unchanged.
 assert len({c['id'] for c in cases})==len(cases)==1400
 for school in schools:
  school['count']=sum(c['school']==school['id'] for c in cases)
  school['countsByYear']={y:sum(c['school']==school['id'] and c['year']==y for c in cases) for y in ['2027','2026']}
  assert (ROOT/school['logo'].lstrip('/')).is_file(),school['id']
 data=dict(updated='2026-11-23',years=['2027','2026'],schools=schools,cases=cases)
 (ROOT/'assets/site/admissions/cases.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
 print(json.dumps({'total':len(cases),'added':len(new),'schoolCount':len(schools),'categories2026':dict(Counter(c['category'] for c in new)),'focusedTotal':sum(c['category']!='other' for c in cases)},ensure_ascii=False))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('source',type=Path);build(parser.parse_args().source)
