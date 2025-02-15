from flask import Flask, request, send_file, render_template
from docxtpl import DocxTemplate
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Process form data into structured format
        form_data = process_form_data(request.form)

        # Generate the document
        doc_io = generate_docx(form_data)

        # Return the document as a downloadable file
        return send_file(
            doc_io,
            as_attachment=True,
            download_name="Completed_Curriculum.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    return render_template("index.html")

def process_form_data(form):
    """
    Convert form data into structured dictionary format
    """
    context = {}

    # Define categories to process
    categories = ["BSC", "ESC", "PCC", "ELECTIVE", "OEC", "MC", "EEC", "HSMC"]

    for category in categories:
        context[category] = []
        s_no = 1
        i = 1  # Dynamic row index

        while f"{category}_title_{i}" in form:
            context[category].append({
                "s_no": s_no,
                "title": form[f"{category}_title_{i}"],
                "sem": form.get(f"{category}_sem_{i}", ""),
                "ltpc": form.get(f"{category}_ltpc_{i}", ""),
            })
            s_no += 1
            i += 1

    # Process Semester-wise course tables
    for sem in range(1, 9):  # Semesters I to VIII
        key = f"course_table{sem}"
        context[key] = []
        s_no = 1
        i = 1

        while f"{key}_course_code_{i}" in form:
            context[key].append({
                "s_no": s_no,
                "type": form.get(f"{key}_type_{i}", ""),
                "course_code": form[f"{key}_course_code_{i}"],
                "course_title": form[f"{key}_course_title_{i}"],
                "l": form.get(f"{key}_l_{i}", ""),
                "t": form.get(f"{key}_t_{i}", ""),
                "p": form.get(f"{key}_p_{i}", ""),
                "c": form.get(f"{key}_c_{i}", ""),
            })
            s_no += 1
            i += 1

    # Process Document Version
    context["document_version"] = [{
        "version": form.get("doc_version", "1.0"),
        "date": form.get("doc_date", ""),
        "author": form.get("doc_author", ""),
        "approved_by": form.get("doc_approved", ""),
    }]

    return context

def generate_docx(context):
    """
    Generate a .docx document from the processed form data
    """


    context = {

    "BSC": [
        {"s_no": 1, "title": "Mathematics – I\nCalculus and Linear Algebra", "sem": "I", "ltpc": "3-2-0-4"},
        {"s_no": 2, "title": "Engineering Physics", "sem": "I", "ltpc": "3-0-2-4"},
        {"s_no": 3, "title": "Mathematics – II\nProbability and Statistics", "sem": "II", "ltpc": "3-2-0-4"},
        {"s_no": 4, "title": "Discrete Mathematics", "sem": "III", "ltpc": "3-2-0-4"},
    ],
    "ESC": [
        {"s_no": 1, "title": "C++ Programming", "sem": "I", "ltpc": "3-0-2-4"},
        {"s_no": 2, "title": "Digital System Design", "sem": "I", "ltpc": "3-0-2-4"},
        {"s_no": 3, "title": "Web Development Essentials", "sem": "II", "ltpc": "3-0-2-4"},
        {"s_no": 4, "title": "Foundation of Data Science", "sem": "III", "ltpc": "3-0-2-4"},
    ],
    "PCC": [
        {"s_no": 1, "title": "Artificial Intelligence", "sem": "I", "ltpc": "3-0-2-4"},
        {"s_no": 2, "title": "Data Structures using C++", "sem": "II", "ltpc": "3-0-2-4"},
        {"s_no": 3, "title": "Database Management Systems", "sem": "II", "ltpc": "3-0-2-4"},
        {"s_no": 4, "title": "Introduction to Java Programming", "sem": "II", "ltpc": "3-0-2-4"},
        {"s_no": 5, "title": "Operating Systems", "sem": "III", "ltpc": "3-0-2-4"},
        {"s_no": 6, "title": "Design and Analysis of Algorithms", "sem": "III", "ltpc": "3-0-2-4"},
        {"s_no": 7, "title": "Web Development Frameworks and Practices", "sem": "III", "ltpc": "3-0-2-4"},
        {"s_no": 8, "title": "Parallel programming through Python", "sem": "III", "ltpc": "3-0-2-4"},
        {"s_no": 9, "title": "Core Course Project-I", "sem": "III", "ltpc": "0-0-2-1"},
        {"s_no": 10, "title": "Computer Networks", "sem": "IV", "ltpc": "3-0-2-4"},
    ],
    "ELECTIVE": [
        {"s_no": 1, "title": "Professional Elective – I", "sem": "V", "ltpc": "3-0-2-3"},
        {"s_no": 2, "title": "Professional Elective – II", "sem": "V", "ltpc": "3-0-2-3"},
        {"s_no": 3, "title": "Professional Elective – III", "sem": "V", "ltpc": "3-0-2-3"},
        {"s_no": 4, "title": "Professional Elective – IV", "sem": "VI", "ltpc": "3-0-2-3"},
    ],
    "OEC": [
        {"s_no": 1, "title": "Open Elective – I", "sem": "VI", "ltpc": "3-0-0-3"},
        {"s_no": 2, "title": "Open Elective – II", "sem": "VII", "ltpc": "3-0-0-3"},
    ],
    "MC": [
        {"s_no": 1, "title": "Mandatory Course – I", "sem": "III", "ltpc": "2-0-0-0"},
        {"s_no": 2, "title": "Mandatory Course – II", "sem": "IV", "ltpc": "2-0-0-0"},
    ],
    "EEC": [
        {"s_no": 1, "title": "Employment Enhancement Course – I", "sem": "I", "l": "0", "t": "0", "p": "2", "c": "1"},
        {"s_no": 2, "title": "Employment Enhancement Course – II", "sem": "II", "l": "0", "t": "0", "p": "2", "c": "1"},
        {"s_no": 3, "title": "Employment Enhancement Course – III", "sem": "III", "l": "0", "t": "0", "p": "2", "c": "1"},
    ],


     "category_table": [
        {"s_no": 1, "category": "Humanities & Social Science Courses (HSMC)", "credits": 13},
        {"s_no": 2, "category": "Basic Science Courses (BSC)", "credits": 16},
        {"s_no": 3, "category": "Engineering Science Courses (ESC)", "credits": 16},
        {"s_no": 4, "category": "Program Core Courses (PCC)", "credits": 78},
        {"s_no": 5, "category": "Professional Elective Courses (PEC)", "credits": 18},
        {"s_no": 6, "category": "Open Elective Courses (OEC)", "credits": 6},
        {"s_no": 7, "category": "Employability Enhancement COURSES (EEC)", "credits": 21},
        {"s_no": 8, "category": "Mandatory Course (MC)", "credits": 0}
    ],


    "total_credits": 168 ,

    "credits_table": [
        {"hours_type": "1 Hour Lecture (L) per week", "credit_value": "1 Credit"},
        {"hours_type": "1 Hour Tutorial (T) per week", "credit_value": "1 Credit"},
        {"hours_type": "1 Hour Practical (P) per week", "credit_value": "0.5 Credit"},
    ],
    "regulation":2024,
    "HSMC": [
        {"s_no": 1, "title": "தமிழர் மரபு /Heritage of Tamils", "sem": "I", "ltpc": "1-0-0-1"},
        {"s_no": 2, "title": "Communicative English – I", "sem": "I", "ltpc": "3-0-2-4"},
        {"s_no": 3, "title": "தமிழரும் தொழில் நுட்பமும் /Tamil and Technology", "sem": "II", "ltpc": "1-0-0-1"},
        {"s_no": 4, "title": "Communicative English – II", "sem": "II", "ltpc": "3-0-2-4"},
        {"s_no": 5, "title": "Professional Ethics & Human Values", "sem": "VII", "ltpc": "3-0-0-3"},
    ],
    "suspects": [
        {
            "version": "1.0",
            "date": "2024-02-15",
            "author": "John Doe",
            "gopal": "Gopal Krishna",
            "approved": "Jane Smith"
        },
                {
            "version": "1.0",
            "date": "2024-02-15",
            "author": "John Doe",
            "gopal": "Gopal Krishna",
            "approved": "Jane Smith"
        }
    ],"course_table1": [
        {"s_no": 1, "type": "T", "course_code": "IP4101", "course_title": "Induction Program", "l": "", "t": "", "p": "", "c": ""},
        {"s_no": 2, "type": "T", "course_code": "MA4101", "course_title": "Mathematics – I\nCalculus and Linear Algebra", "l": 3, "t": 1, "p": 0, "c": 4},
        {"s_no": 3, "type": "T", "course_code": "HS4101", "course_title": "தமிழர்மரபு /Heritage of Tamils", "l": 1, "t": 0, "p": 0, "c": 1},
        {"s_no": 4, "type": "T&P", "course_code": "HS4102", "course_title": "Communicative English - I", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ],
    "course_table2": [
        {"s_no": 1, "type": "T", "course_code": "MA4201", "course_title": "Probability and Statistics", "l": 3, "t": 1, "p": 0, "c": 4},
        {"s_no": 2, "type": "T", "course_code": "HS4201", "course_title": "தமிழரும் தொழில் நுட்பமும் / Tamils and Technology", "l": 1, "t": 0, "p": 0, "c": 1},
        {"s_no": 3, "type": "T&P", "course_code": "HS4202", "course_title": "Communicative English – II", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 4, "type": "T&P", "course_code": "AM4201", "course_title": "Web Development Essentials", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ],
    "course_table3": [
        {"s_no": 1, "type": "T", "course_code": "MA4301", "course_title": "Discrete Mathematics", "l": 3, "t": 1, "p": 0, "c": 4},
        {"s_no": 2, "type": "T&P", "course_code": "AM4301", "course_title": "Operating Systems", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 3, "type": "T&P", "course_code": "HS4202", "course_title": "Communicative English – II", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 4, "type": "T&P", "course_code": "AM4201", "course_title": "Web Development Essentials", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ],
    "course_table4": [
        {"s_no": 1, "type": "T", "course_code": "AM4401", "course_title": "Computing Theory & Compiler Design", "l": 3, "t": 0, "p": 0, "c": 3},
        {"s_no": 2, "type": "T&P", "course_code": "AM4301", "course_title": "Operating Systems", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 3, "type": "T&P", "course_code": "HS4202", "course_title": "Communicative English – II", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 4, "type": "T&P", "course_code": "AM4201", "course_title": "Web Development Essentials", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ],
    "course_table5": [
        {"s_no": 1, "type": "T&P", "course_code": "AM4501", "course_title": "Natural Language Processing", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 2, "type": "T&P", "course_code": "AM4301", "course_title": "Operating Systems", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 3, "type": "T&P", "course_code": "HS4202", "course_title": "Communicative English – II", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 4, "type": "T&P", "course_code": "AM4201", "course_title": "Web Development Essentials", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ],
    "course_table6": [
        {"s_no": 1, "type": "T", "course_code": "AM4601", "course_title": "Machine Learning Operations", "l": 3, "t": 0, "p": 0, "c": 3},
        {"s_no": 2, "type": "T&P", "course_code": "AM4301", "course_title": "Operating Systems", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 3, "type": "T&P", "course_code": "HS4202", "course_title": "Communicative English – II", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 4, "type": "T&P", "course_code": "AM4201", "course_title": "Web Development Essentials", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ],
    "course_table7": [
        {"s_no": 1, "type": "T", "course_code": "HS4703", "course_title": "Professional Ethics and Universal Human Values", "l": 3, "t": 0, "p": 0, "c": 3},
        {"s_no": 2, "type": "T&P", "course_code": "AM4301", "course_title": "Operating Systems", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 3, "type": "T&P", "course_code": "HS4202", "course_title": "Communicative English – II", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 4, "type": "T&P", "course_code": "AM4201", "course_title": "Web Development Essentials", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ],
    "course_table8": [
        {"s_no": 1, "type": "P", "course_code": "AM4801", "course_title": "Project Phase-II", "l": 0, "t": 0, "p": 12, "c": 6},
        {"s_no": 2, "type": "T&P", "course_code": "AM4301", "course_title": "Operating Systems", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 3, "type": "T&P", "course_code": "HS4202", "course_title": "Communicative English – II", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 4, "type": "T&P", "course_code": "AM4201", "course_title": "Web Development Essentials", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 5, "type": "T&P", "course_code": "PH4101", "course_title": "Engineering Physics", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 6, "type": "T&P", "course_code": "AM4101", "course_title": "Artificial Intelligence", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 7, "type": "T&P", "course_code": "EC4111", "course_title": "Digital System Design", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 8, "type": "T&P", "course_code": "CS4102", "course_title": "C++ Programming", "l": 3, "t": 0, "p": 2, "c": 4},
        {"s_no": 9, "type": "P", "course_code": "ES4101", "course_title": "Employability Enhancement Skills - I", "l": 0, "t": 0, "p": 2, "c": 1},
    ]
}


    template_path = "curriculum_template.docx"
    doc = DocxTemplate(template_path)

    # Render the template with the collected context
    doc.render(context)

    # Save the document in memory
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    return doc_io

if __name__ == "__main__":
    app.run(debug=True)
