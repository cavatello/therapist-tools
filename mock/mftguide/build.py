import json, subprocess, collections

ENTRIES = [
 ("California Institute of Integral Studies","OozCl_m-Fi8","program-overview",
  "The school's own walkthrough of its Integral Counseling Psychology MFT track, showing how CIIS blends mind, body and spirit into clinical training."),
 ("Pacifica Graduate Institute","00eO3lNxtho","program-overview",
  "Pacifica walks through exactly how its depth-psychology M.A. leads to MFT and LPCC licensure, so you can see the clinical path and not just the philosophy."),
 ("Sofia University","2VWvAGQRgAE","program-overview",
  "A five-minute spotlight on Sofia's M.A. in Counseling Psychology that lays out the transpersonal orientation students will actually be trained in."),
 ("The Wright Institute","hXozRAdGUlE","program-overview",
  "A detailed tour of the Wright Institute's M.A. in Counseling Psychology, the Berkeley program built specifically around clinical practice for MFT licensure."),
 ("Palo Alto University","kWVGYGZJnUs","student-voices",
  "An hour-long panel of current MA in Counseling students answering the practical questions about coursework, practicum and workload."),
 ("Pepperdine University (GSEP)","AW0dgjnjx-o","student-voices",
  "A student in the daytime MFT format describes what the Pepperdine clinical psychology M.A. is like day to day."),
 ("University of Southern California (Rossier)","IElr12ukb3I","program-overview",
  "A very short official spot confirming the shape of USC Rossier's M.S. in Marriage and Family Therapy - useful as a quick orientation, not a deep dive."),
 ("Alliant International University (CSPP)","BIifLvBeWPY","program-overview",
  "Alliant lays out how its MFT programs are structured across California campuses and what graduates go on to do."),
 ("San Diego State University","MTOjmbv6atc","faculty-talk",
  "An SDSU MFT faculty member describes the program's systemic and social-justice orientation, which is the clearest signal of how the department thinks."),
 ("San Jose State University","iwkj_fgLYDw","student-voices",
  "A Counselor Education student at SJSU's Lurie College talks through her own path into the program and what the cohort experience feels like."),
 ("California State University, Northridge","LVVMTyln5PM","student-voices",
  "A 26-minute conversation with a current CSUN M.A. in MFT student, the most candid look available at that program's day-to-day."),
 ("University of San Francisco","35l-Z9W8Q2U","info-session",
  "A full USF information session on the Marriage and Family Therapy M.A., covering admissions, curriculum and traineeship placement."),
 ("Santa Clara University","HDuyeofhmik","student-voices",
  "Current students in SCU's Counseling Psychology department describe why they chose it and what the training emphasises."),
 ("Saint Mary's College of California","RVjM7woep_U","program-overview",
  "An overview of the Kalmanovitz School of Education's graduate counseling program, the route to MFT licensure at Saint Mary's."),
 ("Antioch University Santa Barbara","c8PwO3ME7cc","program-overview",
  "Antioch Santa Barbara explains the structure and social-justice framing of its M.A. in Clinical Psychology, the MFT-licensure degree."),
 ("Pacific Oaks College","GPdjZI3Eitc","info-session",
  "A complete information session on Pacific Oaks' M.A. in MFT including the trauma-studies specialisation, with admissions and curriculum detail."),
 ("Dominican University of California","hrbgDTMjqhY","program-overview",
  "Dominican explains the pacing and flexibility of its M.S. in Counseling Psychology, aimed at students balancing work with the degree."),
 ("Chapman University","MA1y3EDU8h0","info-session",
  "A 24-minute admissions information session on Chapman's MFT program, walking through requirements, clinical training and timelines."),
 ("Loma Linda University","yfJn-ucfk3A","program-overview",
  "Loma Linda's Department of Counseling and Family Sciences introduces its Marital and Family Therapy programs and their faith-integrated approach."),
 ("Azusa Pacific University","Mw6MkvSW3xc","faculty-talk",
  "A short faculty introduction from an APU psychology professor who is a practising MFT, giving a sense of who teaches in the graduate program."),
 ("Point Loma Nazarene University","Wg1clgSWLZM","program-overview",
  "PLNU's overview of its M.A. in Clinical Counseling, the degree that leads to MFT and LPCC licensure at the San Diego campus."),
 ("Vanguard University","jTe75KIA550","program-overview",
  "Vanguard's overview of its graduate clinical psychology programs, which house the MFT-licensure track."),
 ("California Baptist University","arOYgpVoqfY","program-overview",
  "CBU explains the format and content of its online Master of Counseling Psychology, useful if you are weighing a distance option."),
 ("Fresno Pacific University","36ltIvqxmGE","program-overview",
  "A four-minute look at FPU's Marriage and Family Therapy program and its Central Valley clinical training context."),
 ("Hope International University","898929_75SE","program-overview",
  "A brief official introduction to HIU's Marriage and Family Therapy master's program in Fullerton."),
 ("University of La Verne","9-PgLDj-HYs","student-voices",
  "A La Verne MFT student describes in her own words what drew her to the program and how it has shaped her."),
 ("Concordia University Irvine (Townsend Institute)","kIb7wzcTv40","program-overview",
  "The Townsend Institute introduces its M.A. in Counseling (Clinical Mental Health), including its distinctive competency and mentorship model."),
 ("The Chicago School","dWgWqQC2nN8","program-overview",
  "The Chicago School's own overview of its Marital and Family Therapy program and the systemic training it provides."),
 ("Touro University Worldwide","LgKDTIAzXPQ","program-overview",
  "A four-minute walkthrough of Touro Worldwide's fully online M.A. in Marriage and Family Therapy, including how clinical hours are handled."),
 ("Golden Gate University","xoXrVTfNXis","info-session",
  "A recent GGU information session covering its psychology programs, including the counseling psychology track toward MFT licensure."),
 ("Daybreak University","xZ-bOwroDsg","faculty-talk",
  "A distinguished professor in Daybreak's Marriage and Family Therapy program introduces herself, giving a sense of the faculty behind this small couple-therapy-focused school."),
]

def oembed(vid):
    r = subprocess.run(["curl","-s","-w","|HTTP%{http_code}",
        f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"],
        capture_output=True, text=True, timeout=60).stdout
    body, code = r.rsplit("|HTTP",1)
    if code.strip() != "200":
        return None
    return json.loads(body)

out = collections.OrderedDict()
failed = []
for school, vid, kind, why in ENTRIES:
    d = oembed(vid)
    if not d:
        failed.append((school, vid)); continue
    out[school] = {"id": vid, "title": d["title"], "channel": d["author_name"], "why": why, "kind": kind}

with open("/home/claude/work/mftguide/videos.json","w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("written:", len(out))
print("failed:", failed)
