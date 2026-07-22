
"""
Translation dictionary for Face Attendance System
Languages: English (en), Turkish (tr), Arabic (ar)
"""

TRANSLATIONS = {
    # Layout & Navigation
    'page_title': {
        'en': 'Face Attendance System',
        'tr': 'Yüz Tanıma Sistemi',
        'ar': 'نظام الحضور بالوجه'
    },
    'gateway': {
        'en': 'Gateway',
        'tr': 'Giriş',
        'ar': 'البوابة'
    },
    'logout': {
        'en': 'Logout',
        'tr': 'Çıkış',
        'ar': 'تسجيل خروج'
    },
    'back': {
        'en': 'Back',
        'tr': 'Geri Dön',
        'ar': 'رجوع'
    },
    
    # Gateway Page (index.html)
    'campus_access_control': {
        'en': 'FACE RECOGNITION CAMPUS ACCESS CONTROL',
        'tr': 'FACE RECOGNITION İLE KAMPÜS GİRİŞ KONTROL SİSTEMİ',
        'ar': 'نظام التحكم في دخول الحرم الجامعي بالتعرف على الوجه'
    },
    'admin_portal': {
        'en': 'ADMIN PORTAL',
        'tr': 'YÖNETİCİ PORTALI',
        'ar': 'بوابة الإدارة'
    },
    'professor_portal': {
        'en': 'UNIVERSITY ATTENDANCE SYSTEM',
        'tr': 'ÜNİVERSİTE YOKLAMA SİSTEMİ',
        'ar': 'نظام الحضور الجامعي'
    },
    'manage_students': {
        'en': 'Manage Students',
        'tr': 'Öğrencileri Yönet',
        'ar': 'إدارة الطلاب'
    },
    'register_new_student': {
        'en': 'Register New Student',
        'tr': 'Yeni Öğrenci Kaydet',
        'ar': 'تسجيل طالب جديد'
    },
    'real_time_tracking': {
        'en': 'Real-time Identification',
        'tr': 'Gerçek Zamanlı Tanıma',
        'ar': 'تحديد الهوية في الوقت الحقيقي'
    },
    'auto_attendance': {
        'en': 'Automatic Attendance',
        'tr': 'Otomatik Yoklama',
        'ar': 'حضور تلقائي'
    },

    # Admin Dashboard
    'admin_dashboard_title': {
        'en': 'Admin Dashboard',
        'tr': 'Yönetici Paneli',
        'ar': 'لوحة تحكم المسؤول'
    },
    'system_management': {
        'en': 'System Management & Statistics',
        'tr': 'Sistem Yönetimi ve İstatistikler',
        'ar': 'إدارة النظام والإحصائيات'
    },
    'total_students': {
        'en': 'Total Students',
        'tr': 'Toplam Öğrenci',
        'ar': 'إجمالي الطلاب'
    },
    'student_management': {
        'en': 'Student Management',
        'tr': 'Öğrenci Yönetimi',
        'ar': 'إدارة الطلاب'
    },
    'add_student': {
        'en': 'Add New Student',
        'tr': 'Yeni Öğrenci Ekle',
        'ar': 'إضافة طالب جديد'
    },
    'loading_students': {
        'en': 'Loading students...',
        'tr': 'Öğrenciler yükleniyor...',
        'ar': 'جاري تحميل الطلاب...'
    },
    'no_students_yet': {
        'en': 'No students registered yet',
        'tr': 'Henüz kayıtlı öğrenci yok',
        'ar': 'لا يوجد طلاب مسجلين بعد'
    },
    'click_to_add': {
        'en': 'Click "Add New Student" to register',
        'tr': 'Kaydetmek için "Yeni Öğrenci Ekle"ye tıklayın',
        'ar': 'انقر على "إضافة طالب جديد" للتسجيل'
    },
    'name': {
        'en': 'Name',
        'tr': 'İsim',
        'ar': 'الاسم'
    },
    'student_id': {
        'en': 'Student ID',
        'tr': 'Öğrenci No',
        'ar': 'رقم الطالب'
    },
    'registered_date': {
        'en': 'Registered',
        'tr': 'Kayıt Tarihi',
        'ar': 'تاريخ التسجيل'
    },
    'actions': {
        'en': 'Actions',
        'tr': 'İşlemler',
        'ar': 'إجراءات'
    },
    'delete': {
        'en': 'Delete',
        'tr': 'Sil',
        'ar': 'حذف'
    },

    # Admin Login
    'admin_login_title': {
        'en': 'Admin Login',
        'tr': 'Yönetici Girişi',
        'ar': 'دخول المسؤول'
    },
    'secure_auth_required': {
        'en': 'Secure Authentication Required',
        'tr': 'Güvenli Kimlik Doğrulama Gerekli',
        'ar': 'مطلوب مصادقة آمنة'
    },
    'admin_password': {
        'en': 'Admin Password',
        'tr': 'Yönetici Şifresi',
        'ar': 'كلمة مرور المسؤول'
    },
    'enter_password': {
        'en': 'Enter password',
        'tr': 'Şifreyi giriniz',
        'ar': 'أدخل كلمة المرور'
    },
    'login_btn': {
        'en': 'Login',
        'tr': 'Giriş Yap',
        'ar': 'تسجيل الدخول'
    },
    'authorized_personnel': {
        'en': 'Authorized Personnel Only',
        'tr': 'Sadece Yetkili Personel',
        'ar': 'للموظفين المصرح لهم فقط'
    },

    # Setup Page
    'class_setup': {
        'en': 'Class Setup',
        'tr': 'Sınıf Kurulumu',
        'ar': 'إعداد الفصل'
    },
    'initialize_session': {
        'en': 'Initialize Your Class Session',
        'tr': 'Ders Oturumunu Başlatın',
        'ar': 'بدء جلسة الفصل'
    },
    'doctor_name': {
        'en': 'Doctor Name',
        'tr': 'Akademisyen Adı',
        'ar': 'اسم الدكتور'
    },
    'enter_doctor_name': {
        'en': 'Enter doctor name',
        'tr': 'Akademisyen adını giriniz',
        'ar': 'أدخل اسم الدكتور'
    },
    'course_name': {
        'en': 'Course Name',
        'tr': 'Ders Adı',
        'ar': 'اسم المادة'
    },
    'enter_course_name': {
        'en': 'Enter course name',
        'tr': 'Ders adını giriniz',
        'ar': 'أدخل اسم المادة'
    },
    'course_code': {
        'en': 'Course Code',
        'tr': 'Ders Kodu',
        'ar': 'رمز المادة'
    },
    'enter_course_code': {
        'en': 'Enter course code',
        'tr': 'Ders kodunu giriniz',
        'ar': 'أدخل رمز المادة'
    },
    'start_session': {
        'en': 'Start Session',
        'tr': 'Oturumu Başlat',
        'ar': 'بدء الجلسة'
    },
    'powered_by': {
        'en': 'Powered by MediaPipe & DeepFace',
        'tr': 'MediaPipe & DeepFace ile Güçlendirilmiştir',
        'ar': 'مدعوم بواسطة MediaPipe & DeepFace'
    },

    # Attendance Page
    'smart_attendance': {
        'en': 'Smart Attendance',
        'tr': 'Akıllı Yoklama',
        'ar': 'الحضور الذكي'
    },
    'live_session': {
        'en': 'LIVE SESSION',
        'tr': 'CANLI OTURUM',
        'ar': 'جلسة مباشرة'
    },
    'view_stats': {
        'en': 'View Statistics',
        'tr': 'İstatistikleri Görüntüle',
        'ar': 'عرض الإحصائيات'
    },
    'end_session': {
        'en': 'End Session',
        'tr': 'Oturumu Sonlandır',
        'ar': 'إنهاء الجلسة'
    },
    'live_camera_feed': {
        'en': 'Live Face Recognition Feed',
        'tr': 'Canlı Yüz Tanıma Akışı',
        'ar': 'بث التعرف على الوجه المباشر'
    },
    'live_log': {
        'en': 'Live Attendance Log',
        'tr': 'Canlı Yoklama Kaydı',
        'ar': 'سجل الحضور المباشر'
    },
    'waiting_for_students': {
        'en': 'Waiting for students...',
        'tr': 'Öğrenciler bekleniyor...',
        'ar': 'بانتظار الطلاب...'
    },
    'face_recognition_active': {
        'en': 'Face recognition active',
        'tr': 'Yüz tanıma devam ediyor',
        'ar': 'التعرف على الوجه نشط'
    },
    'refresh_log': {
        'en': 'Refresh Log',
        'tr': 'Kaydı Yenile',
        'ar': 'تحديث السجل'
    },
    'detected': {
        'en': 'Detected',
        'tr': 'Algılanan',
        'ar': 'تم الكشف عنهم'
    },
    'marked': {
        'en': 'Marked',
        'tr': 'İşaretlenen',
        'ar': 'تم تسجيلهم'
    },
    'present': {
        'en': 'Present',
        'tr': 'Mevcut',
        'ar': 'حاضر'
    },
    'status_legend': {
        'en': 'Detection Status',
        'tr': 'Algılama Durumu',
        'ar': 'حالة الكشف'
    },
    'green_new': {
        'en': 'GREEN: New Student',
        'tr': 'YEŞİL: Yeni Öğrenci',
        'ar': 'أخضر: طالب جديد'
    },
    'gold_marked': {
        'en': 'GOLD: Already Marked',
        'tr': 'ALTIN: Zaten İşaretlendi',
        'ar': 'ذهبي: مسجل مسبقاً'
    },
    'cyan_unknown': {
        'en': 'CYAN: Unknown',
        'tr': 'TURKUAZ: Bilinmiyor',
        'ar': 'أزرق سماوي: غير معروف'
    },

    # Course Stats Page
    'course_analytics': {
        'en': 'Course Analytics',
        'tr': 'Ders Analitiği',
        'ar': 'تحليلات المادة'
    },
    'attendance_dashboard': {
        'en': 'Attendance Dashboard',
        'tr': 'Yoklama Paneli',
        'ar': 'لوحة الحضور'
    },
    'start_attendance_mode': {
        'en': 'Start Attendance Mode',
        'tr': 'Yoklama Modunu Başlat',
        'ar': 'بدء وضع الحضور'
    },
    'course_overview': {
        'en': 'Course Overview',
        'tr': 'Ders Genel Bakışı',
        'ar': 'نظرة عامة على المادة'
    },
    'total_lectures': {
        'en': 'Total Lectures',
        'tr': 'Toplam Ders',
        'ar': 'إجمالي المحاضرات'
    },
    'remaining': {
        'en': 'Remaining',
        'tr': 'Kalan',
        'ar': 'المتبقي'
    },
    'capacity': {
        'en': 'Class Capacity',
        'tr': 'Sınıf Kapasitesi',
        'ar': 'سعة الفصل'
    },
    'total_attendance': {
        'en': 'Total Attendance',
        'tr': 'Toplam Katılım',
        'ar': 'إجمالي الحضور'
    },
    'attendance_timeline': {
        'en': 'Daily Attendance Timeline',
        'tr': 'Günlük Yoklama Çizelgesi',
        'ar': 'الجدول الزمني للحضور اليومي'
    },
    'day': {
        'en': 'Day',
        'tr': 'Gün',
        'ar': 'اليوم'
    },
    'date': {
        'en': 'Date',
        'tr': 'Tarih',
        'ar': 'التاريخ'
    },
    'status': {
        'en': 'Status',
        'tr': 'Durum',
        'ar': 'الحالة'
    },
    'absent': {
        'en': 'Absent',
        'tr': 'Yok',
        'ar': 'غائب'
    },
    'rate': {
        'en': 'Rate',
        'tr': 'Oran',
        'ar': 'النسبة'
    },
    'view_details': {
        'en': 'View Details',
        'tr': 'Detayları Gör',
        'ar': 'عرض التفاصيل'
    },
    'completed': {
        'en': 'Completed',
        'tr': 'Tamamlandı',
        'ar': 'مكتمل'
    },
    'in_progress': {
        'en': 'In Progress',
        'tr': 'Devam Ediyor',
        'ar': 'قيد التنفيذ'
    },
    'upcoming': {
        'en': 'Upcoming',
        'tr': 'Gelecek',
        'ar': 'قادم'
    },
    'ready_to_start': {
        'en': 'Ready to Start',
        'tr': 'Başlamaya Hazır',
        'ar': 'جاهز للبدء'
    },

    # Register Page
    'student_registration': {
        'en': 'Student Registration',
        'tr': 'Öğrenci Kaydı',
        'ar': 'تسجيل الطلاب'
    },
    'capture_face_instruction': {
        'en': 'Capture face and register new student',
        'tr': 'Yüzü tara ve yeni öğrenci kaydet',
        'ar': 'التقط الوجه وسجل طالباً جديداً'
    },
    'live_feed': {
        'en': 'Live Camera Feed',
        'tr': 'Canlı Kamera Akışı',
        'ar': 'بث الكاميرا المباشر'
    },
    'position_face': {
        'en': 'Position your face in the frame for detection',
        'tr': 'Algılama için yüzünüzü çerçeveye hizalayın',
        'ar': 'ضع وجهك في الإطار للكشف التلقائي'
    },
    'student_info': {
        'en': 'Student Information',
        'tr': 'Öğrenci Bilgileri',
        'ar': 'معلومات الطالب'
    },
    'full_name': {
        'en': 'Full Name',
        'tr': 'Ad Soyad',
        'ar': 'الاسم الكامل'
    },
    'enter_name': {
        'en': 'Enter student name',
        'tr': 'Öğrenci adını giriniz',
        'ar': 'أدخل اسم الطالب'
    },
    'enter_id': {
        'en': 'Enter student ID',
        'tr': 'Öğrenci numarasını giriniz',
        'ar': 'أدخل رقم الطالب'
    },
    'capture_register_btn': {
        'en': 'Capture Face & Register',
        'tr': 'Yüzü Tara ve Kaydet',
        'ar': 'التقاط الوجه والتسجيل'
    },
    'instructions': {
        'en': 'Instructions',
        'tr': 'Talimatlar',
        'ar': 'التعليمات'
    },
    'instruction_lighting': {
        'en': 'Ensure good lighting on your face',
        'tr': 'Yüzünüzde iyi bir aydınlatma olduğundan emin olun',
        'ar': 'تأكد من وجود إضاءة جيدة على وجهك'
    },
    'instruction_look': {
        'en': 'Look directly at the camera',
        'tr': 'Doğrudan kameraya bakın',
        'ar': 'انظر مباشرة إلى الكاميرا'
    },
    'instruction_wait': {
        'en': 'Wait for green box to appear (face detected)',
        'tr': 'Yeşil kutunun görünmesini bekleyin (yüz algılandı)',
        'ar': 'انتظر ظهور المربع الأخضر (تم اكتشاف الوجه)'
    },
    'instruction_fill': {
        'en': 'Fill in the form and click capture',
        'tr': 'Formu doldurun ve kaydet butonuna tıklayın',
        'ar': 'املأ النموذج واضغط على تسجيل'
    },
    
    # Common JS/Alerts
    'success': {
        'en': 'Success',
        'tr': 'Başarılı',
        'ar': 'نجاح'
    },
    'error': {
        'en': 'Error',
        'tr': 'Hata',
        'ar': 'خطأ'
    },
    'warning': {
        'en': 'Warning',
        'tr': 'Uyarı',
        'ar': 'تحذير'
    },
    'cancel': {
        'en': 'Cancel',
        'tr': 'İptal',
        'ar': 'إلغاء'
    },
    'yes': {
        'en': 'Yes',
        'tr': 'Evet',
        'ar': 'نعم'
    },
    'confirm_delete': {
        'en': 'Are you sure you want to delete?',
        'tr': 'Silmek istediğinizden emin misiniz?',
        'ar': 'هل أنت متأكد أنك تريد الحذف؟'
    },
    'cannot_undo': {
        'en': 'This action cannot be undone!',
        'tr': 'Bu işlem geri alınamaz!',
        'ar': 'لا يمكن التراجع عن هذا الإجراء!'
    },
    'deleting': {
        'en': 'Deleting...',
        'tr': 'Siliniyor...',
        'ar': 'جاري الحذف...'
    },
    'please_wait': {
        'en': 'Please wait',
        'tr': 'Lütfen bekleyin',
        'ar': 'يرجى الانتظار'
    },
    'deleted': {
        'en': 'Deleted!',
        'tr': 'Silindi!',
        'ar': 'تم الحذف!'
    },
    'failed_delete': {
        'en': 'Failed to delete',
        'tr': 'Silinemedi',
        'ar': 'فشل الحذف'
    },
    'authenticating': {
        'en': 'Authenticating...',
        'tr': 'Kimlik doğrulanıyor...',
        'ar': 'جاري التحقق من الهوية...'
    },
    'access_granted': {
        'en': 'Access Granted!',
        'tr': 'Giriş Başarılı!',
        'ar': 'تم السماح بالدخول!'
    },
    'redirecting': {
        'en': 'Redirecting to dashboard...',
        'tr': 'Panele yönlendiriliyorsunuz...',
        'ar': 'جاري التوجيه للوحة التحكم...'
    },
    'access_denied': {
        'en': 'Access Denied',
        'tr': 'Erişim Reddedildi',
        'ar': 'تم رفض الوصول'
    },
    'invalid_password': {
        'en': 'Invalid password',
        'tr': 'Geçersiz şifre',
        'ar': 'كلمة مرور خاطئة'
    },
    'student_exists': {
        'en': 'Student ID already registered!',
        'tr': 'Öğrenci numarası zaten kayıtlı!',
        'ar': 'رقم الطالب مسجل بالفعل!'
    },
    'face_exists': {
        'en': 'This face is already registered!',
        'tr': 'Bu yüz zaten kayıtlı!',
        'ar': 'هذا الوجه مسجل مسبقاً!'
    }
}
