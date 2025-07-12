import json
import os
import re
from datetime import datetime

class Student:
    def __init__(self, student_id, name, birth_date, phone, address):
        self.student_id = student_id
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'birth_date': self.birth_date,
            'phone': self.phone,
            'address': self.address
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['student_id'],
            data['name'],
            data['birth_date'],
            data['phone'],
            data['address']
        )
    
    def __str__(self):
        return f"MSSV: {self.student_id} | Tên: {self.name} | Ngày sinh: {self.birth_date} | SĐT: {self.phone} | Địa chỉ: {self.address}"

class StudentManager:
    def __init__(self, data_file='student_data.json'):
        self.data_file = data_file
        self.students = []
        self.next_id_number = 1
        self.load_data()
    
    def load_data(self):
        """Tải dữ liệu từ file JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.students = [Student.from_dict(s) for s in data.get('students', [])]
                    self.next_id_number = data.get('next_id_number', 1)
            except Exception as e:
                print(f"Lỗi khi tải dữ liệu: {e}")
                self.students = []
                self.next_id_number = 1
    
    def save_data(self):
        """Lưu dữ liệu vào file JSON"""
        try:
            data = {
                'students': [s.to_dict() for s in self.students],
                'next_id_number': self.next_id_number
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Dữ liệu đã được lưu thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
    
    def normalize_name(self, name):
        """Chuẩn hóa tên: viết hoa chữ cái đầu, viết thường các chữ cái sau"""
        # Loại bỏ khoảng trắng thừa
        name = re.sub(r'\s+', ' ', name.strip())
        
        # Tách thành các từ và chuẩn hóa từng từ
        words = []
        for word in name.split():
            if word:  # Kiểm tra từ không rỗng
                # Viết hoa chữ cái đầu, viết thường các chữ cái sau
                normalized_word = word[0].upper() + word[1:].lower()
                words.append(normalized_word)
        
        return ' '.join(words)
    
    def normalize_date(self, date_input):
        """Chuẩn hóa ngày sinh về định dạng dd/mm/yyyy"""
        if not date_input:
            return None
        
        # Loại bỏ khoảng trắng
        date_input = date_input.strip()
        
        # Các định dạng có thể nhập
        date_formats = [
            '%d/%m/%Y',    # 01/01/2000
            '%d-%m-%Y',    # 01-01-2000
            '%d.%m.%Y',    # 01.01.2000
            '%d/%m/%y',    # 01/01/00
            '%d-%m-%y',    # 01-01-00
            '%d.%m.%y',    # 01.01.00
            '%Y-%m-%d',    # 2000-01-01
            '%Y/%m/%d',    # 2000/01/01
            '%Y.%m.%d',    # 2000.01.01
        ]
        
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_input, fmt)
                
                if date_obj.year < 50:  
                    date_obj = date_obj.replace(year=date_obj.year + 2000)
                elif date_obj.year < 100:  
                    date_obj = date_obj.replace(year=date_obj.year + 1900)
                
                
                current_year = datetime.now().year
                if date_obj.year < 1900 or date_obj.year > current_year:
                    continue
                
                return date_obj.strftime('%d/%m/%Y')
            except ValueError:
                continue
        
        return None
    
    def generate_student_id(self):
        """Tạo mã số sinh viên theo định dạng 24110XXX"""
        if self.next_id_number > 999:
            print("Đã hết mã số sinh viên khả dụng!")
            return None
        student_id = f"24110{self.next_id_number:03d}"
        self.next_id_number += 1
        return student_id
    
    def get_sort_key(self, name):
        """Tạo key để sắp xếp theo tên (lấy từ cuối cùng)"""
        words = name.strip().split()
        if len(words) > 1:
            return words[-1].lower() 
        return name.lower()
    
    def sort_students(self):
        """Sắp xếp sinh viên theo tên (từ cuối cùng) theo thứ tự alphabet"""
        self.students.sort(key=lambda s: self.get_sort_key(s.name))
    
    def add_student(self):
        """Thêm sinh viên mới"""
        print("\n=== THÊM SINH VIÊN MỚI ===")
        
        # Tạo mã số sinh viên
        student_id = self.generate_student_id()
        if not student_id:
            return
        
        # Nhập thông tin sinh viên
        name_input = input("Nhập họ tên: ").strip()
        if not name_input:
            print("Tên không được để trống!")
            return
        
        # Chuẩn hóa tên
        name = self.normalize_name(name_input)
        print(f"Tên đã chuẩn hóa: {name}")
        
        # Nhập và chuẩn hóa ngày sinh
        while True:
            birth_date_input = input("Nhập ngày sinh (nhiều định dạng được hỗ trợ: dd/mm/yyyy, dd-mm-yyyy, yyyy-mm-dd, ...): ").strip()
            if not birth_date_input:
                print("Ngày sinh không được để trống!")
                continue
            
            birth_date = self.normalize_date(birth_date_input)
            if birth_date:
                print(f"Ngày sinh đã chuẩn hóa: {birth_date}")
                break
            else:
                print("Định dạng ngày sinh không hợp lệ hoặc năm không hợp lý! Vui lòng nhập lại.")
                print("Ví dụ: 01/01/2000, 1-1-2000, 2000-01-01, ...")
        
        phone = input("Nhập số điện thoại: ").strip()
        if not phone:
            print("Số điện thoại không được để trống!")
            return
        
        address = input("Nhập địa chỉ: ").strip()
        if not address:
            print("Địa chỉ không được để trống!")
            return
        
        # Tạo sinh viên mới
        student = Student(student_id, name, birth_date, phone, address)
        self.students.append(student)
        self.sort_students()
        self.save_data()
        
        print(f"\nĐã thêm sinh viên thành công với MSSV: {student_id}")
        print(student)
    
    def validate_date(self, date_str):
        """Kiểm tra định dạng ngày"""
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False
    
    def display_students(self):
        """Hiển thị danh sách sinh viên"""
        if not self.students:
            print("\nDanh sách sinh viên trống!")
            return
        
        print(f"\n=== DANH SÁCH SINH VIÊN ({len(self.students)} sinh viên) ===")
        for i, student in enumerate(self.students, 1):
            print(f"{i:2d}. {student}")
    
    def search_student(self):
        """Tìm kiếm sinh viên"""
        print("\n=== TÌM KIẾM SINH VIÊN ===")
        print("1. Tìm theo MSSV")
        print("2. Tìm theo tên")
        print("3. Tìm theo số điện thoại")
        
        choice = input("Chọn cách tìm kiếm (1-3): ").strip()
        
        if choice == '1':
            student_id = input("Nhập MSSV: ").strip()
            results = [s for s in self.students if s.student_id == student_id]
        elif choice == '2':
            name = input("Nhập tên cần tìm: ").strip().lower()
            results = [s for s in self.students if name in s.name.lower()]
        elif choice == '3':
            phone = input("Nhập số điện thoại: ").strip()
            results = [s for s in self.students if phone in s.phone]
        else:
            print("Lựa chọn không hợp lệ!")
            return
        
        if results:
            print(f"\nTìm thấy {len(results)} kết quả:")
            for i, student in enumerate(results, 1):
                print(f"{i}. {student}")
        else:
            print("Không tìm thấy sinh viên nào!")
    
    def find_student_by_id(self, student_id):
        """Tìm sinh viên theo MSSV"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def edit_student(self):
        """Sửa thông tin sinh viên"""
        print("\n=== SỬA THÔNG TIN SINH VIÊN ===")
        student_id = input("Nhập MSSV của sinh viên cần sửa: ").strip()
        
        student = self.find_student_by_id(student_id)
        if not student:
            print("Không tìm thấy sinh viên với MSSV này!")
            return
        
        print(f"Thông tin hiện tại: {student}")
        print("\nNhập thông tin mới (Enter để giữ nguyên):")
        
        # Nhập thông tin mới
        new_name = input(f"Tên ({student.name}): ").strip()
        if new_name:
            student.name = new_name
        
        new_birth_date = input(f"Ngày sinh ({student.birth_date}): ").strip()
        if new_birth_date:
            if self.validate_date(new_birth_date):
                student.birth_date = new_birth_date
            else:
                print("Định dạng ngày sinh không hợp lệ! Giữ nguyên thông tin cũ.")
        
        new_phone = input(f"Số điện thoại ({student.phone}): ").strip()
        if new_phone:
            student.phone = new_phone
        
        new_address = input(f"Địa chỉ ({student.address}): ").strip()
        if new_address:
            student.address = new_address
        
        self.sort_students()
        self.save_data()
        print(f"\nĐã cập nhật thông tin sinh viên: {student}")
    
    def delete_student(self):
        """Xóa sinh viên"""
        print("\n=== XÓA SINH VIÊN ===")
        student_id = input("Nhập MSSV của sinh viên cần xóa: ").strip()
        
        student = self.find_student_by_id(student_id)
        if not student:
            print("Không tìm thấy sinh viên với MSSV này!")
            return
        
        print(f"Thông tin sinh viên: {student}")
        confirm = input("Bạn có chắc chắn muốn xóa sinh viên này? (y/N): ").strip().lower()
        
        if confirm == 'y':
            self.students.remove(student)
            self.save_data()
            print("Đã xóa sinh viên thành công!")
        else:
            print("Hủy thao tác xóa.")
    
    def statistics(self):
        """Thống kê sinh viên"""
        print(f"\n=== THỐNG KÊ ===")
        print(f"Tổng số sinh viên: {len(self.students)}")
        print(f"MSSV tiếp theo: {self.generate_student_id() if self.next_id_number <= 999 else 'Đã hết'}")
        
        if self.students:
            print(f"MSSV nhỏ nhất: {min(s.student_id for s in self.students)}")
            print(f"MSSV lớn nhất: {max(s.student_id for s in self.students)}")
    
    def run(self):
        """Chạy chương trình chính"""
        while True:
            print("\n" + "="*50)
            print("         Student Manage Program")
            print("="*50)
            print("1. Add Student")
            print("2. Show list student")
            print("3. Student Search")
            print("4. Edit information student")
            print("5. Delete Student")
            print("6. Statistics")
            print("0. Thoát")
            print("="*50)
            
            choice = input("Chọn chức năng (0-6): ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.display_students()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.edit_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                self.statistics()
            elif choice == '0':
                break
            else:
                print("Error. Please chose a valid otpiton ")
            
            input("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    manager = StudentManager()
    manager.run()