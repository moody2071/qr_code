import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os
import qrcode
import random

# الحصول على مسار ملف التشغيل
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

# الحصول على اسم المستخدم
user_name = os.getlogin()

# تحديد مسار سطح المكتب
desktop_path = os.path.join("C:\\Users", user_name, "Desktop")

# متغير لتتبع حالة النوافذ المفتوحة
is_window_open = False



def open_unique_code_generator():
    global is_window_open
    if not is_window_open:
        is_window_open = True
        def generate_unique_codes(num_codes, length, start, end):
            unique_codes = set()  # مجموعة لتخزين الأكواد الفريدة

            while len(unique_codes) < num_codes:
                # إنشاء كود عشوائي
                code = start + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length)) + end
                unique_codes.add(code)  # إضافة الكود إلى المجموعة (تجاهل المكررات تلقائيًا)

            return list(unique_codes)

        def create_codes():
            try:
                num_codes_to_generate = int(entry_num_codes.get())
                code_length = int(entry_code_length.get())
                start = entry_start.get()
                end = entry_end.get()
                output_file = entry_output_file.get()

                # توليد الأكواد
                codes = generate_unique_codes(num_codes_to_generate, code_length, start, end)
                codes.sort()

                # كتابة الأكواد إلى ملف نصي
                with open(output_file, "w") as file:
                    for code in codes:
                        file.write(code + "\n")

                messagebox.showinfo("Success", "تم حفظ الأكواد في الملف المحدد")
            except ValueError:
                messagebox.showerror("Error", "يرجى إدخال قيم صحيحة.")
            except Exception as e:
                messagebox.showerror("Error", f"حدث خطأ: {e}")

        def browse_file():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            entry_output_file.delete(0, tk.END)  # مسح المحتوى الحالي
            entry_output_file.insert(0, file_path)  # إدخال المسار المحدد

        def on_closing():
            global is_window_open
            is_window_open = False  # تغيير قيمة المتغير عند الإغلاق
            root.destroy()

        # إنشاء نافذة التطبيق
        root = tk.Tk()
        root.title("مولد الأكواد الفريدة")

        # منع تغيير حجم النافذة
        root.resizable(False, False)  # False تعني غير قابلة للتغيير

        # تحديد موقع النافذة في منتصف الشاشة
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (250 // 2)
        y = (screen_height // 2) - (200 // 2)
        root.geometry(f"450x150+{x}+{y}")

        # الحصول على المسار الحالي
        default_output_path = os.path.join(desktop_path, "unique_codes.txt")

        # إضافة عناصر واجهة المستخدم مع قيم افتراضية
        tk.Label(root, text="عدد الأكواد:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_num_codes = tk.Entry(root)  # تحديد عرض الخانة
        entry_num_codes.insert(0, "6")  # قيمة افتراضية
        entry_num_codes.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(root, text="طول الكود:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        entry_code_length = tk.Entry(root)  # تحديد عرض الخانة
        entry_code_length.insert(0, "7")  # قيمة افتراضية
        entry_code_length.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        tk.Label(root, text="البداية الثابتة:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_start = tk.Entry(root)  # تحديد عرض الخانة
        entry_start.insert(0, "MB_")  # قيمة افتراضية
        entry_start.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        tk.Label(root, text="النهاية الثابتة:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        entry_end = tk.Entry(root)  # تحديد عرض الخانة
        entry_end.insert(0, "$")  # قيمة افتراضية
        entry_end.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # خانة لتحديد مكان إخراج التكست
        tk.Label(root, text="مكان الحفظ:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        entry_output_file = tk.Entry(root, width=40)  # تحديد عرض الخانة
        entry_output_file.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='w')
        entry_output_file.insert(0, default_output_path)  # إدخال المسار الافتراضي

        button_browse = tk.Button(root, text="استعراض", command=browse_file)
        button_browse.grid(row=2, column=3, padx=50, pady=5)

        # زر لإنشاء الأكواد
        button_generate = tk.Button(root, text="توليد وحفظ", command=create_codes)
        button_generate.grid(row=3, columnspan=5, pady=10)

        # ربط الحدث WM_DELETE_WINDOW بالدالة on_closing
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # تشغيل التطبيق
        root.mainloop()


def open_qr_code_generator():
    global is_window_open
    if not is_window_open:
        is_window_open = True
        def generate_unique_codes(num_codes, length, start, end):
            unique_codes = set()  # مجموعة لتخزين الأكواد الفريدة

            while len(unique_codes) < num_codes:
                # إنشاء كود عشوائي
                code = start + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length)) + end
                unique_codes.add(code)  # إضافة الكود إلى المجموعة (تجاهل المكررات تلقائيًا)

            return list(unique_codes)

        def create_codes():
            try:
                num_codes_to_generate = int(entry_num_codes.get())
                code_length = int(entry_code_length.get())
                start = entry_start.get()
                end = entry_end.get()
                output_file = entry_output_file.get()
                output_dir = entry_output_dir.get()  # الحصول على مسار حفظ الصور
                box_size = int(entry_box_size.get())  # الحصول على box_size
                border = int(entry_border.get())  # الحصول على border

                # توليد الأكواد
                codes = generate_unique_codes(num_codes_to_generate, code_length, start, end)
                codes.sort()

                # كتابة الأكواد إلى ملف نصي
                with open(output_file, "w") as file:
                    for code in codes:
                        file.write(code + "\n")

                messagebox.showinfo("Success", "تم حفظ الأكواد في الملف المحدد")

                # إنشاء رموز QR
                create_qr_codes(codes, output_dir, box_size, border)

            except ValueError:
                messagebox.showerror("Error", "يرجى إدخال قيم صحيحة.")
            except Exception as e:
                messagebox.showerror("Error", f"حدث خطأ: {e}")

        def create_qr_codes(codes, output_dir, box_size, border):
            # التأكد من وجود الدليل
            os.makedirs(output_dir, exist_ok=True)

            for code in codes:
                qr = qrcode.QRCode(
                    version=1,  # يمكنك تغيير النسخة حسب الحاجة
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=box_size,
                    border=border,
                )

                qr.add_data(code)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                img.save(f"{output_dir}/{code}.png")  # حفظ الصورة في المسار المحدد

            print("تم إنشاء الرموز بنجاح!")

        def browse_file():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            entry_output_file.delete(0, tk.END)  # مسح المحتوى الحالي
            entry_output_file.insert(0, file_path)  # إدخال المسار المحدد

        def browse_directory():
            dir_path = filedialog.askdirectory()
            entry_output_dir.delete(0, tk.END)  # مسح المحتوى الحالي
            entry_output_dir.insert(0, dir_path)  # إدخال مسار الدليل المحدد

        def on_closing():
            global is_window_open
            is_window_open = False  # تغيير قيمة المتغير عند الإغلاق
            root.destroy()

        # إنشاء نافذة التطبيق
        root = tk.Tk()
        root.title("انشاء رموز فريدة وتحويلها الى باركود")

        # منع تغيير حجم النافذة
        root.resizable(False, False)  # False تعني غير قابلة للتغيير

        # تحديد موقع النافذة في منتصف الشاشة
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (450 // 2)
        y = (screen_height // 2) - (300 // 2)
        root.geometry(f"450x240+{x}+{y}")

        # الحصول على المسار الحالي
        default_output_path = os.path.join(desktop_path, "unique_codes.txt")
        default_output_dir = os.path.join(desktop_path, "qr_codes")  # المسار الافتراضي لحفظ الصور

        # إضافة عناصر واجهة المستخدم مع قيم افتراضية
        tk.Label(root, text="عدد الأكواد:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_num_codes = tk.Entry(root, width=10)
        entry_num_codes.insert(0, "6")  # قيمة افتراضية
        entry_num_codes.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(root, text="طول الكود:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        entry_code_length = tk.Entry(root, width=10)
        entry_code_length.insert(0, "7")  # قيمة افتراضية
        entry_code_length.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        tk.Label(root, text="البداية الثابتة:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_start = tk.Entry(root, width=10)
        entry_start.insert(0, "MB_")  # قيمة افتراضية
        entry_start.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        tk.Label(root, text="النهاية الثابتة:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        entry_end = tk.Entry(root, width=10)
        entry_end.insert(0, "$")  # قيمة افتراضية
        entry_end.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # خانة لتحديد box_size
        tk.Label(root, text="حجم مربع QR:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        entry_box_size = tk.Entry(root, width=10)
        entry_box_size.insert(0, "25")  # قيمة افتراضية
        entry_box_size.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # خانة لتحديد border
        tk.Label(root, text="عرض الحدود:").grid(row=2, column=2, padx=5, pady=5, sticky='e')
        entry_border = tk.Entry(root, width=10)
        entry_border.insert(0, "4")  # قيمة افتراضية
        entry_border.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        # خانة لتحديد مكان إخراج التكست
        tk.Label(root, text="مكان الإخراج:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        entry_output_file = tk.Entry(root, width=40)
        entry_output_file.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        entry_output_file.insert(0, default_output_path)  # إدخال المسار الافتراضي

        button_browse = tk.Button(root, text="استعراض", command=browse_file)
        button_browse.grid(row=3, column=3, padx=5, pady=5)

        # خانة لتحديد مكان حفظ الصور
        tk.Label(root, text="مكان حفظ الصور:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        entry_output_dir = tk.Entry(root, width=40)
        entry_output_dir.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        entry_output_dir.insert(0, default_output_dir)  # إدخال المسار الافتراضي لحفظ الصور

        button_browse_dir = tk.Button(root, text="استعراض", command=browse_directory)
        button_browse_dir.grid(row=4, column=3, padx=5, pady=5)

        # زر لإنشاء الأكواد
        button_generate = tk.Button(root, text="   بدء   ", command=create_codes)
        button_generate.grid(row=5, columnspan=4, pady=10)

        # ربط الحدث WM_DELETE_WINDOW بالدالة on_closing
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # تشغيل التطبيق
        root.mainloop()


def open_qr_code_creator():
    global is_window_open
    if not is_window_open:
        is_window_open = True
        def create_qr_codes():
            try:
                # قراءة الأكواد من الملف النصي
                with open(entry_file_path.get(), 'r') as file:
                    codes = file.read().splitlines()

                # إعدادات حجم رمز QR
                box_size = int(entry_box_size.get())  # حجم كل مربع في الرمز (بكسل)
                border = int(entry_border.get())  # عرض الحدود (عدد المربعات)

                # إنشاء رموز QR
                output_dir = entry_output_dir.get()
                os.makedirs(output_dir, exist_ok=True)  # التأكد من وجود الدليل

                for code in codes:
                    qr = qrcode.QRCode(
                        version=1,  # يمكنك تغيير النسخة حسب الحاجة
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=box_size,
                        border=border,
                    )

                    qr.add_data(code)
                    qr.make(fit=True)

                    img = qr.make_image(fill_color="black", back_color="white")
                    img.save(os.path.join(output_dir, f"{code}.png"))  # حفظ الصورة باسم الكود

                messagebox.showinfo("Success", "تم إنشاء الرموز بنجاح!")

            except FileNotFoundError:
                messagebox.showerror("Error", "لم يتم العثور على الملف المحدد.")
            except Exception as e:
                messagebox.showerror("Error", f"حدث خطأ: {e}")

        def browse_file():
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            entry_file_path.delete(0, tk.END)  # مسح المحتوى الحالي
            entry_file_path.insert(0, file_path)  # إدخال المسار المحدد

        def browse_directory():
            dir_path = filedialog.askdirectory()
            entry_output_dir.delete(0, tk.END)
            entry_output_dir.insert(0, dir_path)

        def on_closing():
            global is_window_open
            is_window_open = False  # تغيير قيمة المتغير عند الإغلاق
            root.destroy()  # إغلاق النافذة

        # إنشاء نافذة التطبيق
        root = tk.Tk()
        root.title("مولد رموز QR")

        # منع تغيير حجم النافذة
        root.resizable(False, False)  # False تعني غير قابلة للتغيير

        # تحديد موقع النافذة في منتصف الشاشة
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (450 // 2)
        y = (screen_height // 2) - (300 // 2)
        root.geometry(f"450x150+{x}+{y}")

        default_output_dir = os.path.join(desktop_path, "qr")

        # إعداد واجهة المستخدم
        tk.Label(root, text="حجم مربع QR:").grid(row=0, column=0, padx=5, pady=5)
        entry_box_size = tk.Entry(root, width=10)
        entry_box_size.insert(0, "25")  # قيمة افتراضية
        entry_box_size.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(root, text="عرض الحدود:").grid(row=0, column=1, padx=5, pady=5)
        entry_border = tk.Entry(root, width=10)
        entry_border.insert(0, "4")  # قيمة افتراضية
        entry_border.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        tk.Label(root, text="حدد ملف الأكواد:").grid(row=1, column=0, padx=5, pady=5)
        entry_file_path = tk.Entry(root, width=40)
        entry_file_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="استعراض", command=browse_file).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(root, text="مكان حفظ الصور:").grid(row=2, column=0, padx=5, pady=5)
        entry_output_dir = tk.Entry(root, width=40)
        entry_output_dir.grid(row=2, column=1, padx=5, pady=5)
        entry_output_dir.insert(0, default_output_dir)  # إدخال المسار الافتراضي لحفظ الصور
        tk.Button(root, text="استعراض", command=browse_directory).grid(row=2, column=2, padx=5, pady=5)

        tk.Button(root, text="إنشاء رموز QR", command=create_qr_codes).grid(row=3, columnspan=3, pady=10)

        # ربط الحدث WM_DELETE_WINDOW بالدالة on_closing
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # تشغيل التطبيق
        root.mainloop()


def text_to_qr_code():
    global is_window_open
    if not is_window_open:
        is_window_open = True

        def create_qr_code():
            try:
                # قراءة النص من حقل الإدخال
                code = entry_text.get()
                image_name = entry_image_name.get()

                # إعدادات حجم رمز QR
                box_size = int(entry_box_size.get())  # حجم كل مربع في الرمز (بكسل)
                border = int(entry_border.get())  # عرض الحدود (عدد المربعات)

                # إنشاء رمز QR
                output_dir = entry_output_dir.get()
                os.makedirs(output_dir, exist_ok=True)  # التأكد من وجود الدليل

                qr = qrcode.QRCode(
                    version=1,  # يمكنك تغيير النسخة حسب الحاجة
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=box_size,
                    border=border,
                )

                qr.add_data(code)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                img.save(os.path.join(output_dir, f"{image_name}.png"))  # حفظ الصورة باسم المستخدم

                messagebox.showinfo("Success", "تم إنشاء رمز QR بنجاح!")

            except Exception as e:
                messagebox.showerror("Error", f"حدث خطأ: {e}")

        def browse_directory():
            dir_path = filedialog.askdirectory()
            entry_output_dir.delete(0, tk.END)
            entry_output_dir.insert(0, dir_path)

        def on_closing():
            global is_window_open
            is_window_open = False  # تغيير قيمة المتغير عند الإغلاق
            root.destroy()  # إغلاق النافذة

        # إنشاء نافذة التطبيق
        root = tk.Tk()
        root.title("تحويل نص الى باركود")

        # منع تغيير حجم النافذة
        root.resizable(False, False)

        # تحديد موقع النافذة في منتصف الشاشة
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (450 // 2)
        y = (screen_height // 2) - (300 // 2)
        root.geometry(f"450x200+{x}+{y}")

        # إعداد واجهة المستخدم
        tk.Label(root, text="النص المراد تحويله:").grid(row=0, column=0, padx=5, pady=5)
        entry_text = tk.Entry(root, width=40)
        entry_text.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="اسم الصورة:").grid(row=1, column=0, padx=5, pady=5)
        entry_image_name = tk.Entry(root, width=40)
        entry_image_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="حجم مربع QR:").grid(row=2, column=0, padx=5, pady=5)
        entry_box_size = tk.Entry(root, width=10)
        entry_box_size.insert(0, "25")  # قيمة افتراضية
        entry_box_size.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        tk.Label(root, text="عرض الحدود:").grid(row=2, column=1, padx=5, pady=5)
        entry_border = tk.Entry(root, width=10)
        entry_border.insert(0, "4")  # قيمة افتراضية
        entry_border.grid(row=2, column=1, padx=5, pady=5, sticky='e')

        tk.Label(root, text="مكان حفظ الصورة:").grid(row=3, column=0, padx=5, pady=5)
        entry_output_dir = tk.Entry(root, width=40)
        entry_output_dir.grid(row=3, column=1, padx=5, pady=5)
        default_output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "qr")
        entry_output_dir.insert(0, default_output_dir)  # إدخال المسار الافتراضي لحفظ الصور
        tk.Button(root, text="استعراض", command=browse_directory).grid(row=3, column=2, padx=5, pady=5)

        tk.Button(root, text="إنشاء رمز QR", command=create_qr_code).grid(row=4, columnspan=3, pady=10)

        # ربط الحدث WM_DELETE_WINDOW بالدالة on_closing
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # تشغيل التطبيق
        root.mainloop()



# إنشاء نافذة التطبيق
root = tk.Tk()
root.title("اختيار البرنامج")


# إعداد حجم النافذة
root.geometry("300x200")

# منع تغيير حجم النافذة
root.resizable(False, False)  # False تعني غير قابلة للتغيير

# زر لفتح مولد الأكواد الفريدة
button_unique_codes = tk.Button(root, text="مولد الأكواد الفريدة", command=open_unique_code_generator)
button_unique_codes.pack(pady=10)

# زر لفتح مولد رموز QR
button_qr_codes = tk.Button(root, text="انشاء الاكواد مع تحويلها الى QR", command=open_qr_code_generator)
button_qr_codes.pack(pady=10)

# زر لفتح برنامج إنشاء رموز QR
button_qr_creator = tk.Button(root, text="تحويل الرموز الى QR", command=open_qr_code_creator)
button_qr_creator.pack(pady=10)

# زر لفتح برنامج إنشاء رموز QR
button_qr_creator = tk.Button(root, text="تحويل نص الى باركود", command=text_to_qr_code)
button_qr_creator.pack(pady=10)

# تشغيل التطبيق
root.mainloop()