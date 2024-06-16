import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

# 폰트 파일 경로를 절대 경로로 설정
font_path = "C:/Users/sgrhe/OneDrive/문서/2024-1학기/실무웹클라이언트/minju_O2B2WEB-main/O2B2WEB-main/cradle-to-grave/home/fonts/NanumGothic.ttf"

# NanumGothic 폰트를 reportlab에 등록
if not os.path.exists(font_path):
    raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {font_path}")
pdfmetrics.registerFont(TTFont('NanumGothic', font_path))

def create_pdf(resume_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    # 기본 스타일에 NanumGothic 폰트 적용
    normal_style = ParagraphStyle(
        name='Normal',
        parent=styles['Normal'],
        fontName='NanumGothic',
        fontSize=12,
        leading=18
    )

    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Title'],
        fontName='NanumGothic',
        fontSize=18,
        spaceAfter=14
    )

    section_title_style = ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontName='NanumGothic',
        fontSize=14,
        spaceBefore=10,
        spaceAfter=10
    )

    resume_text_style = ParagraphStyle(
        name='ResumeText',
        parent=styles['Normal'],
        fontName='NanumGothic',
        fontSize=12,
        leading=20  # 줄 간격을 약간 더 넓게 설정
    )

    content = []

    # 이력서 제목
    title = Paragraph(f"{resume_data['name']}의 이력서", title_style)
    content.append(title)
    content.append(Spacer(1, 0.2 * inch))

    # 직무
    jobs = Paragraph(f"직무: {', '.join(resume_data['jobs'])}", normal_style)
    content.append(jobs)
    content.append(Spacer(1, 0.2 * inch))

    # 경력
    experience = Paragraph(f"경력: {resume_data['start_year']} - {resume_data['end_year']}", normal_style)
    content.append(experience)
    content.append(Spacer(1, 0.2 * inch))

    # 연락처
    contact = Paragraph(f"연락처: {resume_data['contact']}", normal_style)
    content.append(contact)
    content.append(Spacer(1, 0.2 * inch))

    # 학력
    education = Paragraph(f"학력: {resume_data['education']}", normal_style)
    content.append(education)
    content.append(Spacer(1, 0.2 * inch))

    # 자격증
    cert = Paragraph(f"자격증: {resume_data['cert']}", normal_style)
    content.append(cert)
    content.append(Spacer(1, 0.2 * inch))

    # URL
    url = Paragraph(f"URL: {resume_data['url']}", normal_style)
    content.append(url)
    content.append(Spacer(1, 0.2 * inch))

    # 회사
    company = Paragraph(f"회사: {resume_data['company']}", normal_style)
    content.append(company)
    content.append(Spacer(1, 0.2 * inch))

    # 경험
    experience = Paragraph(f"경험: {resume_data['experience']}", normal_style)
    content.append(experience)
    content.append(Spacer(1, 0.2 * inch))

    # 기술
    skills = Paragraph(f"기술: {', '.join(resume_data['skills'])}", normal_style)
    content.append(skills)
    content.append(Spacer(1, 0.2 * inch))

    # 기술 수준
    skill_levels = [[Paragraph(f"{skill}", normal_style), Paragraph(f"{level}", normal_style)] for skill, level in resume_data['skill_levels'].items()]
    skill_table = Table(skill_levels, colWidths=[2 * inch, 4 * inch])
    skill_table.setStyle(TableStyle([
       # ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
      #  ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(skill_table)
    content.append(Spacer(1, 0.2 * inch))

    # 요약
    summary = Paragraph(f"요약: {resume_data['summary']}", normal_style)
    content.append(summary)
    content.append(Spacer(1, 0.2 * inch))

    # AI가 생성한 이력서 텍스트
    resume_text = Paragraph("AI가 생성한 이력서 텍스트:", section_title_style)
    content.append(resume_text)
    content.append(Spacer(1, 0.2 * inch))
    text_object = Paragraph(resume_data['resume_text'].replace('\n', '<br/>'), resume_text_style)
    content.append(text_object)

    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()
