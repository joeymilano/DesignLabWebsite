"""Bilingual content for the main pages. Consumed by scripts/build-site.py.

Every user-facing string is either plain (same in both languages) or B(zh, en).
Facts here come from the pre-redesign homepage; do not invent new claims.
"""


def B(zh, en):
    return {"zh": zh, "en": en}


TB = "https://item.taobao.com/item.htm?id="
SHOP = "https://m.tb.cn/h.7JpsJZMWJLsNTwq"
XHS = "https://xhslink.com/m/3SgVLnRsIGw"
EMAIL = "super666joey@gmail.com"

# ---------------------------------------------------------------- shared

SCHOOLS = [
    ("RCA", "Royal College of Art", "London"),
    ("UCL", "University College London", "London"),
    ("Columbia", "Columbia University", "New York"),
    ("UPenn", "University of Pennsylvania", "Philadelphia"),
    ("Cornell", "Cornell University", "Ithaca"),
    ("MIT", "Massachusetts Institute of Technology", "Cambridge"),
    ("CMU", "Carnegie Mellon University", "Pittsburgh"),
    ("PoliMi", "Politecnico di Milano", "Milan"),
    ("TU Delft", "Delft University of Technology", "Delft"),
    ("PolyU", "Hong Kong Polytechnic University", "Hong Kong"),
    ("Parsons", "Parsons School of Design", "New York"),
    ("Aalto", "Aalto University", "Helsinki"),
    ("UAL", "University of the Arts London", "London"),
    ("UCLA", "University of California, Los Angeles", "Los Angeles"),
    ("RMIT", "RMIT University", "Melbourne"),
    ("LCF", "London College of Fashion", "London"),
]

STUDIO_STATS = [
    ("$", 100, "M+", B("业务操盘经验", "Business impact")),
    ("", B(4, 400), B("亿+", "M+"), B("用户级产品经验", "Users on products we've shaped")),
    ("", 14, B("天", " days"), B("AI MVP 上线", "AI MVP to launch")),
    ("", 20, "+", B("已交付数字产品", "Digital products shipped")),
]
ACADEMY_STATS = [
    ("", 6, B("年", " yrs"), B("专注作品集辅导", "Portfolio mentoring")),
    ("", 6000, "+", B("服务案例", "Projects delivered")),
    ("", 600, "+", B("名校 Offer", "Offers from top schools")),
    ("", 98.6, "%", B("学员好评率", "Positive reviews")),
]

PEOPLE = [
    dict(key="joey", img="joey", name="Joey", biz="sa",
         role=B("AI 产品 / 游戏 / 数字媒体", "AI product / Games / Digital media"),
         edu=B("米兰理工大学 · 产品设计硕士", "MSc Product Design, Politecnico di Milano"),
         note=B("硅谷高级产品设计师 · 独立全栈开发者", "Sr. product designer, Silicon Valley · Indie full-stack")),
    dict(key="xue", img="xue", name=B("学小嵩", "Xiaosong"), biz="a",
         role=B("系统设计策略 / 插画 / 3D", "Systems strategy / Illustration / 3D"),
         edu=B("奥斯陆建筑与设计学院 · 设计硕士", "MDes, Oslo School of Architecture and Design"),
         note=B("学科第一毕业 · Normann Copenhagen", "Top of class · Normann Copenhagen")),
    dict(key="jackie", img="jackie", name="Jackie", biz="a",
         role=B("交互 / HCI / 工业 / 服务设计", "Interaction / HCI / Industrial / Service"),
         edu=B("格拉斯哥大学 HCI 博士 · RMIT 硕士", "PhD HCI, Glasgow · MDes, RMIT"),
         note=B("学生去向 MIT · CMU · RCA · 米理", "Students to MIT · CMU · RCA · PoliMi")),
    dict(key="cheng", img="cheng", name=B("程越", "Cheng Yue"), biz="as",
         role=B("3D / MG 动画 / 平面 / VI", "3D / Motion / Graphic / Identity"),
         edu=B("马兰欧尼男装设计 · 英国皇家艺术学院", "Menswear, Istituto Marangoni · RCA"),
         note=B("POP MART · LVMH · 优衣库 · CROCS", "POP MART · LVMH · Uniqlo · CROCS")),
    dict(key="jason", img="jason", name="Jason", biz="a",
         role=B("建筑 / 景观 / 城市设计", "Architecture / Landscape / Urban"),
         edu=B("加州大学伯克利分校 · 建筑硕士", "MArch, UC Berkeley"),
         note=B("学生去向 哥大 · 宾大 · 康奈尔 · UCL", "Students to Columbia · UPenn · Cornell · UCL")),
]

MENTOR_BIO = {
    "joey": B("5 年以上 AI 产品、游戏与数字媒体设计经验。曾主导制药研发 LIMS、AI 室内设计平台 CollovGPT 与携程酒店视频体验；独立完成 Finfold、BillVampire 及叙事卡牌 RPG《Pleasure Contract》。把真实产品方法带进交互、产品与数字媒体方向的作品集辅导。",
              "5+ years designing AI products, games and digital media. Led a pharmaceutical LIMS, CollovGPT and Ctrip's hotel video experience; independently shipped Finfold, BillVampire and the narrative card RPG Pleasure Contract. Brings real product methods into interaction, product and digital-media portfolios."),
    "xue": B("以学科第一的成绩毕业，推崇研究方法与全局系统思维。教学注重学生的独特性和细节，排版、配色、字体层级会反复调到位。",
             "Graduated top of class. Advocates research methodology and whole-system thinking. Teaching centres on each student's individuality and on detail — layout, colour and type hierarchy tuned until right."),
    "jackie": B("负责学生申请 MIT、CMU、RCA、伦艺、阿尔托、米兰理工、宾大等院校，并辅导博士申请港理工、哈佛、帝国理工等。RP 反馈能精确到研究问题是否够 sharp、方法论是否合适。",
                "Guided students to MIT, CMU, RCA, UAL, Aalto, Politecnico di Milano and UPenn, and PhD applicants to PolyU, Harvard and Imperial. RP feedback goes down to whether the research question is sharp and the method fits."),
    "cheng": B("学生成功申请伦敦时装学院、帕森斯、墨尔本皇家理工；与 LVMH 集团、优衣库、CROCS 等时尚品牌有商务合作经验。同时负责工作室的品牌与 VI 项目。",
               "Students admitted to London College of Fashion, Parsons and RMIT. Commercial work with LVMH, Uniqlo and CROCS. Also leads brand and identity projects for the studio."),
    "jason": B("熟悉北美和欧洲建筑、景观申请流程，擅长倒推时间线、取舍项目、快速出图。辅导学生录取康奈尔、哥伦比亚、宾大、UCLA、UCL。",
               "Knows North American and European architecture and landscape applications inside out — reverse-planning deadlines, choosing projects, producing visuals fast. Students admitted to Cornell, Columbia, UPenn, UCLA and UCL."),
}
MENTOR_TAGS = {
    "joey": ["AI Product", "Game Design", "UX/UI", "Full-stack"],
    "xue": ["Systems", "Illustration", "3D", "Layout"],
    "jackie": ["HCI", "Service Design", "PhD RP"],
    "cheng": ["3D", "Motion", "Identity", "Fashion"],
    "jason": ["Architecture", "Landscape", "Diagrams", "Rendering"],
}

# ---------------------------------------------------------------- work

# (slug, zh title, en title, category key)
STUDENT_WORK = [
    ("wearable-memory", "心理治疗可穿戴装置", "Therapeutic wearable", "product"),
    ("e-motorcycle", "电动摩托概念设计", "Electric motorcycle concept", "vehicle"),
    ("mars-research", "火星殖民居住研究", "Mars habitation research", "space"),
    ("dance-video-app", "舞蹈短视频剪辑 App", "Dance video editing app", "ux"),
    ("vehicle-lighting", "汽车灯光语言研究", "Automotive lighting language", "vehicle"),
    ("sky-city", "空中城市插画叙事", "Sky City — illustrated narrative", "visual"),
    ("kitchen-sink", "厨房水槽产品设计", "Kitchen sink product design", "product"),
    ("property-legal-app", "房产交易律师协作 App", "Property conveyancing app", "ux"),
    ("mars-modules", "火星模块化居住系统", "Modular Mars habitat", "space"),
    ("zeon-identity", "ZEON 品牌识别", "ZEON brand identity", "visual"),
    ("vehicle-hmi", "车载 HMI 界面", "In-vehicle HMI", "vehicle"),
    ("pet-locker", "宠物友好储物柜", "Pet-friendly locker", "product"),
    ("souffle-jewelry", "Soufflé 珠宝电商", "Soufflé jewellery e-commerce", "ux"),
    ("atlantic-collage", "The Atlantic 贫富拼贴", "The Atlantic — editorial collage", "visual"),
    ("head-wearables", "头部可穿戴形态研究", "Head-worn form study", "product"),
    ("journey-map", "用户体验旅程图", "Experience journey map", "ux"),
    ("spatial-audio", "Unity 沉浸式空间音频", "Unity spatial audio experience", "visual"),
    ("drone-render", "无人机 3D 渲染", "Drone 3D rendering", "product"),
    ("sustainable-app", "可持续生活 App", "Sustainable living app", "ux"),
    ("hotel-cover", "Philosophy Hotel 封面", "Philosophy Hotel cover", "visual"),
    ("realtime-visuals", "实时互动视觉", "Real-time interactive visuals", "visual"),
]
WORK_SIZE = {
    "wearable-memory": 1069, "e-motorcycle": 694, "mars-research": 1217, "mars-modules": 912,
    "vehicle-lighting": 935, "journey-map": 655, "sustainable-app": 627, "vehicle-hmi": 858,
    "kitchen-sink": 710, "pet-locker": 945, "head-wearables": 873, "dance-video-app": 1279,
    "property-legal-app": 1417, "souffle-jewelry": 1355, "atlantic-collage": 1119, "sky-city": 1108,
    "zeon-identity": 773, "hotel-cover": 726, "spatial-audio": 827, "realtime-visuals": 740,
    "drone-render": 984,
}
CATS = {
    "product": B("工业产品", "Product"),
    "vehicle": B("交通载具", "Transportation"),
    "space": B("建筑空间", "Architecture"),
    "ux": B("交互体验", "Interaction"),
    "visual": B("视觉媒体", "Visual & media"),
}

PRODUCTS = [
    dict(slug="finfold", name="Finfold", url="https://finfold.app", img="finfold-live", w=1249, h=703, year="2026",
         cat=B("AI 营销 SaaS", "AI marketing SaaS"),
         desc=B("AI 营销员工：一条产品更新，自动改写成小红书、X、公众号等 13 个平台的地道文案。",
                "An AI marketing hire: one product update, rewritten natively for 13 platforms from Xiaohongshu to X.")),
    dict(slug="billvampire", name="BillVampire", url="https://billvampire.com", img="billvampire-live", w=1266, h=712, year="2025",
         cat=B("AI 分账工具", "AI bill splitting"),
         desc=B("拍一张小票，几秒完成分账。从设计、开发到上线，全栈独立交付。",
                "Scan a receipt, split it in seconds. Designed, built and shipped end to end.")),
    dict(slug="joeyzhao", name="joeyzhao.cc", url="https://joeyzhao.cc", img="joeyzhao-live", w=1600, h=900, year="2025",
         cat=B("3D 交互网站", "3D interactive site"),
         desc=B("设计师 × 全栈开发者的个人站：实时 3D 场景，记录从概念到产品的全过程。",
                "A designer-developer's home on the web: a real-time 3D scene documenting concept to product.")),
]

CREDITS = [
    ("CollovGPT", B("AI 室内设计平台", "AI interior design platform"), B("产品设计", "Product design")),
    (B("制药研发 LIMS", "Pharmaceutical LIMS"), B("企业级 SaaS", "Enterprise SaaS"), B("产品与交互设计", "Product & UX")),
    (B("携程酒店视频体验", "Ctrip hotel video"), B("4 亿+ 用户级产品", "400M+ user product"), B("体验设计", "Experience design")),
    ("Pleasure Contract", B("叙事卡牌 RPG", "Narrative card RPG"), B("游戏设计与开发", "Game design & build")),
]

# ---------------------------------------------------------------- services

STUDIO_SERVICES = [
    dict(name=B("AI 应用 MVP", "AI app MVP"), price="5,000",
         desc=B("14 天把 AI 想法做成可上线的产品", "An AI idea to a live product in 14 days"),
         tags=[B("产品逻辑", "Product logic"), "UI/UX", "Frontend", "API", "Deploy"],
         detail="/services/ai-mvp", tb=None),
    dict(name=B("产品设计 × 全栈开发", "Product design × full-stack"), price="100",
         desc=B("AI 产品、SaaS、小程序、企业官网", "AI products, SaaS, mini-programs, websites"),
         tags=["AI", "SaaS", B("小程序", "Mini-program"), B("官网", "Website")],
         detail=None, tb="1034073567253"),
    dict(name=B("LOGO / 品牌 VI", "Logo & brand identity"), price="100",
         desc=B("商标、VI 系统、画册、包装", "Marks, identity systems, brochures, packaging"),
         tags=["Logo", "VI", B("画册", "Print"), B("包装", "Packaging")],
         detail="/services/logo-branding", tb="615300225900"),
    dict(name=B("工业设计 / 3D", "Industrial design / 3D"), price="50",
         desc=B("建模、手绘、渲染、排版 · Blender / Rhino", "Modelling, sketching, rendering · Blender / Rhino"),
         tags=["Rhino", "Blender", "KeyShot", B("3D 打印", "3D print")],
         detail="/services/industrial-design", tb="762456555696"),
]
ACADEMY_SERVICES = [
    dict(name=B("作品集原创设计", "Portfolio design"), price="100",
         desc=B("产品、交互、建筑、景观、环艺、服装 · 海外与国内考研", "Product, interaction, architecture, landscape, fashion"),
         tags=[B("产品", "Product"), B("交互", "UX"), B("建筑", "Architecture"), B("景观", "Landscape"), B("服装", "Fashion")],
         detail=B("/services/portfolio-design", "/en/design-portfolio/"), tb="803744173646"),
    dict(name=B("留学生作业辅导", "Coursework tutoring"), price="200",
         desc=B("课程作业、Studio 项目、毕业设计", "Coursework, studio projects, graduation work"),
         tags=["Coursework", "Studio", B("毕设", "Thesis")],
         detail="/services/portfolio-design", tb=None),
    dict(name=B("博士研究计划", "PhD research proposal"), price="100",
         desc=B("选校网申、RP 写作、面试、顶会期刊", "Supervisor match, RP writing, interviews, papers"),
         tags=["RP", B("选导师", "Supervisors"), B("面试", "Interview")],
         detail="/services/phd-research-proposal", tb="859327120560"),
    dict(name=B("线下个人艺术展", "Solo exhibition"), price="99.69",
         desc=B("上海线下策展，作品集之外的第二份证明", "Curated shows in Shanghai — proof beyond the portfolio"),
         tags=[B("策展", "Curation"), B("布展", "Install"), B("上海", "Shanghai")],
         detail=None, tb="999259878379"),
    dict(name=B("设计师求职辅导", "Designer career coaching"), price="100",
         desc=B("985 / 211 / 八大美院 / QS300 背景导师", "Mentors from top Chinese and QS300 schools"),
         tags=[B("简历", "CV"), B("作品集", "Portfolio"), B("面试", "Interview")],
         detail=None, tb="641877726592"),
]

STUDIO_STEPS = [
    (B("需求咨询", "Brief"), B("一句话讲清楚做什么、给谁用、何时上线。我们帮你判断范围和技术路线。", "Tell us what, for whom, and by when. We scope it and pick the stack.")),
    (B("方案定制", "Proposal"), B("给出功能清单、原型方向、报价与交付时间，确认后开工。", "A feature list, prototype direction, quote and timeline — then we start.")),
    (B("设计执行", "Design & build"), B("设计与开发并行推进，定期演示可点击的版本。", "Design and engineering in parallel, with clickable builds along the way.")),
    (B("修改完善", "Refine"), B("按真实使用反馈迭代，直到每个细节都达到预期。", "Iterate on real feedback until every detail is right.")),
    (B("交付验收", "Launch"), B("部署上线，交付源码与文档，提供后续支持。", "Deployed, with source, docs and ongoing support.")),
]
ACADEMY_STEPS = [
    (B("需求咨询", "Consult"), B("聊背景、目标院校和时间线，评估现有素材。", "Background, target schools and timeline; we review what you have.")),
    (B("方案定制", "Plan"), B("匹配导师，制定项目取舍与叙事策略，确认报价和交付时间。", "Mentor match, project selection and narrative strategy; quote and schedule.")),
    (B("设计执行", "Build"), B("导师一对一推进，定期 meeting，进度随时可见。", "One-to-one with your mentor, regular meetings, visible progress.")),
    (B("修改完善", "Refine"), B("排版、配色、字体层级反复打磨，直到满意为止。", "Layout, colour and type hierarchy refined until you're happy.")),
    (B("交付验收", "Submit"), B("交付完整源文件，陪你走完网申与面试。", "Full source files, and support through submission and interviews.")),
]

REVIEWS = [
    dict(who=B("L 同学", "Student L"), mentor="Joey", case="/cases/interaction-design-milano",
         result=B("米兰理工 · 代尔夫特理工 — 交互设计硕士", "Politecnico di Milano · TU Delft — MSc Interaction Design"),
         text=B("之前对比了四五家机构，最后选 1% 主要是因为 Joey 老师本人就是米理毕业的，聊了一次就觉得很对路。老师没有硬套模板，而是根据我自己的项目经历去提炼亮点，用户研究那块给了很清晰的框架，项目逻辑一下就通了。最后米兰理工和代尔夫特都给了 offer。",
                "I compared four or five agencies before going with 1%, mainly because Joey himself graduated from Politecnico di Milano — one conversation and I knew he was the right fit. He didn't force a template on me but pulled highlights from my own projects. The user research framework he suggested tightened my logic. Both Milano and Delft gave me offers.")),
    dict(who=B("W 同学", "Student W"), mentor="Jackie", case="/cases/architecture-ucl",
         result=B("UCL 伦敦大学学院 — 建筑设计硕士", "UCL — MArch Architecture"),
         text=B("本科是普通二本的环艺，一开始挺没信心。Jackie 老师看完作品说“素材够用，关键是怎么讲故事”，帮我把四个项目重新串了一遍。九月开始做，一月交，改了无数版，老师消息基本秒回。拿到 UCL offer 的时候真的愣了好久。",
                "My undergrad was interior design at a lesser-known school, so I wasn't confident. Jackie said \"you have enough material — it's about how you tell the story,\" and restructured all four projects with me. September to January, countless revisions, replies almost instant. When the UCL offer came I just stared at the screen.")),
    dict(who=B("Z 同学", "Student Z"), mentor="Jackie", case="/cases/phd-polyu",
         result=B("香港理工大学（全奖）— 设计学博士", "Hong Kong PolyU (full scholarship) — PhD Design"),
         text=B("博士申请身边很少有人能给有效建议，尤其是 RP。Jackie 老师本身是 Glasgow 的 HCI 博士，反馈能精确到研究问题够不够 sharp、方法论合不合适。选校也很务实，帮你匹配真正合适的导师。最后拿到港理工全奖。",
                "Few people can give useful advice on PhD applications, especially the RP. Jackie is a Glasgow HCI PhD herself — she'll pinpoint whether your research question is sharp enough and whether the method fits. Pragmatic about schools, matching you with the right supervisor. Fully funded at PolyU.")),
    dict(who=B("C 同学", "Student C"), mentor=B("学小嵩", "Xiaosong"), case="/cases/industrial-design-rca",
         result=B("皇家艺术学院 RCA — 工业设计硕士", "Royal College of Art — MA Industrial Design"),
         text=B("跨专业转工业设计，零基础做作品集。学小嵩老师特别稳，每次 meeting 前都把参考案例和思路整理好。她对排版要求很高，配色、字体层级、留白反复调到位。半年从零到拿下 RCA，现在回想还是觉得不真实。",
                "Switching into industrial design with zero portfolio, I was nervous. Xiaosong keeps things steady — references and direction mapped before every meeting. Her layout standards are genuinely high: colour, type hierarchy, whitespace, all tuned until right. Zero to RCA in six months still feels surreal.")),
    dict(who=B("H 同学", "Student H"), mentor="Jason", case="/cases/architecture-columbia-upenn",
         result=B("哥伦比亚大学 · 宾夕法尼亚大学 — 建筑设计硕士", "Columbia · UPenn — MArch Architecture"),
         text=B("考研出分后临时转留学，满打满算三个月。Jason 老师第一次通话就把 ddl 倒推了一遍：哪些学校还来得及、作品集怎么取舍、哪些项目能快速出图，全理清楚了。三个月后哥大和宾大都来了 offer。",
                "I pivoted to studying abroad with three months left. On our first call Jason reverse-engineered every deadline: which schools were still open, what to cut, which projects could produce visuals fast. Three months later Columbia and UPenn both came through.")),
]
BRAND_REVIEW = dict(
    who=B("M 女士", "Ms. M"), mentor=B("程越", "Cheng Yue"), case="/cases/branding-fashion",
    result=B("时尚买手店 — 品牌 LOGO + VI 全套", "Fashion boutique — logo + full identity"),
    text=B("之前找过两家设计公司出 LOGO，要么太保守要么太浮夸。程越老师第一轮方案就让我眼前一亮，她对时尚行业的理解是到位的，不需要反复解释品牌调性。定稿后合伙人直接说“就是这个感觉”，后来又加了一整套 VI。",
           "Two firms before had missed the mark — too safe or too flashy. Cheng Yue's first round already clicked; she understood the tone without it being over-explained. My partner saw the final and said \"that's exactly it.\" We went on to add a full identity system."))

STUDIO_RES = [
    ("/tools/landing-page-audit", B("Landing Page 审计", "Landing page audit"), B("免费诊断 SaaS 官网转化问题。", "Free conversion diagnosis for SaaS sites."), B("工具", "Tool")),
    ("/blog/ai-agent-mvp-guide", B("AI Agent MVP 指南", "AI agent MVP guide"), B("从想法到可用 Agent 的最短路径。", "The shortest path from idea to working agent."), B("文章", "Article")),
    ("/blog/ai-app-builder-vs-custom-development", B("AI 建站工具 vs 定制开发", "AI builders vs custom build"), B("什么时候该找团队，什么时候不用。", "When you need a team — and when you don't."), B("文章", "Article")),
    ("/blog/vibe-coding-to-production", B("从 Vibe Coding 到生产环境", "Vibe coding to production"), B("原型能跑，离上线还差什么。", "What stands between a prototype and production."), B("文章", "Article")),
]
ACADEMY_RES = [
    ("/tools/portfolio-reviewer", B("AI 作品集诊断", "AI portfolio review"), B("60 秒评估作品集竞争力 · ¥299", "Competitiveness check in 60 seconds · ¥299"), B("工具", "Tool")),
    ("/tools/school-matcher", B("选校匹配器", "School matcher"), B("6 个问题，找到适合你的学校。", "Six questions to your shortlist."), B("工具", "Tool")),
    ("/tools/portfolio-calculator", B("作品集费用计算器", "Portfolio cost calculator"), B("30 秒估算预算与时间。", "Budget and timeline in 30 seconds."), B("工具", "Tool")),
    ("/blog/portfolio-timeline", B("作品集时间规划", "Portfolio timeline"), B("倒推 DDL，每个月该做什么。", "Working back from the deadline, month by month."), B("文章", "Article")),
    ("/blog/portfolio-cost-guide", B("作品集费用指南", "Portfolio cost guide"), B("价格区间与避坑清单。", "Price ranges and what to avoid."), B("文章", "Article")),
    ("/blog/architecture-portfolio-guide-2027", B("建筑作品集指南 2027", "Architecture portfolio 2027"), B("北美与英国建筑申请要点。", "North America and UK architecture essentials."), B("文章", "Article")),
    ("/blog/uk-art-school-application-timeline-2027", B("英国艺术院校申请时间线", "UK art school timeline"), B("2027 Fall 各校节点。", "Key dates for Fall 2027."), B("文章", "Article")),
    ("/blog/art-study-abroad-portfolio-requirements-2027", B("各校作品集要求", "Portfolio requirements"), B("2027 艺术留学作品集要求汇总。", "2027 requirements, school by school."), B("文章", "Article")),
]
