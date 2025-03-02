import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import base64

st.title("🚀 Professional Resume PDF Generator")
st.write("Fill in your details and generate a well-formatted, professional resume.")

# Input fields for the resume
name = st.text_input("Full Name", "Vibhas Garg")
email = st.text_input("Email", "vibhasgarg70@gmail.com")
phone = st.text_input("Phone Number", "+91 7876774542")
linkedin = st.text_input("LinkedIn Profile URL", "www.linkedin.com/in/vibhas-garg-193340246")

st.subheader("Career Objective")
career_objective = st.text_area("Enter your career objective",
                                "As an optimistic and keen learner, I am committed to a goal-oriented approach in life...")

st.subheader("Skills (Enter each skill on a new line)")
skills = st.text_area("Enter your skills", "C++\nPython\nReact.js\nHTML, CSS\nAWS\nAmazon Lex\nVideo Editing (Premiere Pro)")

st.subheader("Work Experience")
job_title = st.text_input("Job Title", "Intern")
company = st.text_input("Company", "Wipro")
work_experience = st.text_area("Work Experience",
                               "Gained hands-on experience in cloud management and AI-powered chatbot development...")

st.subheader("Projects")
num_projects = st.number_input("Number of Projects", min_value=1, max_value=5, value=3, step=1)

projects = []
for i in range(num_projects):
    st.write(f"**Project {i+1}**")
    project_title = st.text_input(f"Project Title {i+1}", f"Project {i+1}")
    project_description = st.text_area(f"Description (Optional) {i+1}", "")
    projects.append((project_title, project_description))

st.subheader("Certifications")
certifications = st.text_area("Enter your certifications (one per line)",
                              """Computational Theory: Language Principle & Finite Automata (Infosys Springboard) 
Introduction to Cloud Computing Theory (Infosys Springboard) 
TechA Python Developer Certification (Infosys Springboard)""")

st.subheader("Education")
degree = st.text_input("Degree", "Bachelor of Technology (B.Tech)")
university = st.text_input("University", "Jaypee University of Information Technology")
education_details = st.text_area("Education Details",
                                 """Class XII (Senior Secondary) - Durga Public School, Solan CBSE, 2020 (93.4%) 
Class X (Secondary) - Durga Public School, Solan CBSE, 2018 (84%)""")

def create_resume_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Formatting Helpers
    y_position = 750  # Start position
    line_gap = 18  # Space between lines
    section_gap = 30  # Space between sections
    bullet_gap = 14  # Space between bullet points
    left_margin = 80  # Left margin for alignment
    separator_width = 450  # Extended separation line width

    def draw_separator():
        """Draws a long horizontal line separator."""
        nonlocal y_position
        c.setStrokeColor(colors.grey)
        c.setLineWidth(1.2)
        c.line(left_margin, y_position, left_margin + separator_width, y_position)
        y_position -= section_gap

    # Header (Name & Contact)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(left_margin, y_position, name)
    y_position -= line_gap

    c.setFont("Helvetica", 10)  # Subtext (smaller font)
    c.setFillColor(colors.darkgray)
    c.drawString(left_margin, y_position, f"📧 {email}  |  📞 {phone}  |  🔗 {linkedin}")
    y_position -= section_gap
    c.setFillColor(colors.black)  # Reset text color

    draw_separator()

    # Career Objective
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y_position, "🎯 Career Objective")
    y_position -= line_gap
    c.setFont("Helvetica", 12)
    c.drawString(left_margin, y_position, career_objective[:100])  # Short preview for layout
    y_position -= section_gap

    draw_separator()

    # Skills (Bullet Points)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y_position, "🛠 Skills")
    y_position -= line_gap
    c.setFont("Helvetica", 12)
    for skill in skills.split("\n"):
        c.drawString(left_margin + 15, y_position, f"• {skill}")
        y_position -= bullet_gap
    y_position -= section_gap

    draw_separator()

    # Work Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y_position, "💼 Work Experience")
    y_position -= line_gap
    c.setFont("Helvetica", 12)
    c.drawString(left_margin, y_position, f"{job_title} at {company}")
    y_position -= bullet_gap
    c.drawString(left_margin, y_position, work_experience[:100])
    y_position -= section_gap

    draw_separator()

    # Projects
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y_position, "🚀 Projects")
    y_position -= line_gap
    c.setFont("Helvetica", 12)
    for project_title, project_description in projects:
        c.drawString(left_margin + 15, y_position, f"• {project_title}")
        y_position -= bullet_gap
        if project_description:
            c.setFont("Helvetica-Oblique", 11)
            c.drawString(left_margin + 30, y_position, f"  {project_description[:100]}")
            y_position -= bullet_gap
        y_position -= bullet_gap
    y_position -= section_gap

    draw_separator()

    # Certifications
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y_position, "📜 Certifications")
    y_position -= line_gap
    c.setFont("Helvetica", 12)
    for cert in certifications.split("\n"):
        c.drawString(left_margin + 15, y_position, f"• {cert}")
        y_position -= bullet_gap
    y_position -= section_gap

    draw_separator()

    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y_position, "🎓 Education")
    y_position -= line_gap
    c.setFont("Helvetica", 12)
    c.drawString(left_margin, y_position, f"{degree}, {university}")
    y_position -= bullet_gap
    for edu in education_details.split("\n"):
        c.drawString(left_margin + 15, y_position, f"• {edu}")
        y_position -= bullet_gap

    c.save()
    buffer.seek(0)
    return buffer

if st.button("Generate Resume PDF"):
    pdf_buffer = create_resume_pdf()

    # Convert PDF to Base64 for preview
    pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    # Download button
    st.download_button(label="⬇ Download Resume PDF", data=pdf_buffer, file_name="Resume.pdf", mime="application/pdf")
