from flask import Flask, render_template, request, redirect, url_for
from StudentManage import StudentManager, Student

app = Flask(__name__)
manager = StudentManager()

@app.route('/')
def index():
    manager.sort_students()
    return render_template('index.html', students=manager.students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = manager.normalize_name(request.form['name'])
        birth_date = manager.normalize_date(request.form['birth_date'])
        phone = request.form['phone']
        address = request.form['address']

        student_id = manager.generate_student_id()
        if student_id:
            student = Student(student_id, name, birth_date, phone, address)
            manager.students.append(student)
            manager.sort_students()
            manager.save_data()
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = manager.find_student_by_id(student_id)
    if not student:
        return "Không tìm thấy sinh viên!", 404

    if request.method == 'POST':
        student.name = manager.normalize_name(request.form['name']) or student.name
        birth_date = manager.normalize_date(request.form['birth_date'])
        student.birth_date = birth_date if birth_date else student.birth_date
        student.phone = request.form['phone'] or student.phone
        student.address = request.form['address'] or student.address

        manager.sort_students()
        manager.save_data()
        return redirect(url_for('index'))
    
    return render_template('edit.html', student=student)

@app.route('/delete/<student_id>')
def delete_student(student_id):
    student = manager.find_student_by_id(student_id)
    if student:
        manager.students.remove(student)
        manager.save_data()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        results = [s for s in manager.students if keyword in s.name.lower() or keyword in s.student_id]
    return render_template('search.html', results=results)

@app.route('/stats')
def stats():
    return {
        "Tổng số sinh viên": len(manager.students),
        "MSSV tiếp theo": manager.generate_student_id() or "Hết MSSV",
        "MSSV nhỏ nhất": min([s.student_id for s in manager.students], default="N/A"),
        "MSSV lớn nhất": max([s.student_id for s in manager.students], default="N/A")
    }

if __name__ == '__main__':
    app.run(debug=True)
