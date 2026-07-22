"""
Flask Application for Face Attendance System - 4-Phase Workflow
Phase 1: Gateway, Phase 2: Admin Portal, Phase 3: Professor Portal, Phase 4: Smart Attendance
"""

from flask import Flask, render_template, Response, request, jsonify, session, redirect, url_for, send_file
from camera_engine import CameraEngine

import os
from functools import wraps
import time
from datetime import datetime
import pandas as pd
from io import BytesIO

app = Flask(__name__)
from translations import TRANSLATIONS

app.secret_key = os.urandom(24)

ADMIN_PASSWORD = "admin123"

camera_engine = None


def init_camera():
    """Initialize the camera engine singleton"""
    global camera_engine
    if camera_engine is None:
        try:
            camera_engine = CameraEngine("mongo_config.json")
        except Exception as e:
            print(f"[Error] Failed to initialize camera engine: {e}")
            return None
    return camera_engine


def require_session(f):
    """Decorator to require active class session"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'course_code' not in session:
            return redirect(url_for('doctor_login'))
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== LANGUAGE SETTINGS ====================

@app.context_processor
def inject_language():
    """Make translation function available to all templates"""
    lang = session.get('lang', 'tr')

    def t(key):
        """Translate key to current language"""
        if key in TRANSLATIONS and lang in TRANSLATIONS[key]:
            return TRANSLATIONS[key][lang]
        return key

    return dict(lang=lang, t=t, is_rtl=(lang == 'ar'))


@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    """Set the session language"""
    if lang_code in ['en', 'tr', 'ar']:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))


# ==================== PHASE 1: GATEWAY ====================

@app.route('/')
def index():
    """Main gateway page with dual portals"""
    if 'lang' not in session:
        session['lang'] = 'tr'
    return render_template('index.html')


# ==================== PHASE 2: ADMIN PORTAL ====================

@app.route('/admin_login')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')


@app.route('/admin_auth', methods=['POST'])
def admin_auth():
    """Admin password authentication"""
    password = request.json.get('password', '')

    if password == ADMIN_PASSWORD:
        session['is_admin'] = True
        return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
    else:
        return jsonify({'success': False, 'message': 'Invalid password'}), 401


@app.route('/admin_dashboard')
@require_admin
def admin_dashboard():
    """Admin dashboard with student management"""
    return render_template('admin_dashboard.html')


@app.route('/api/get_all_students')
@require_admin
def get_all_students():
    """Get all registered students from Firebase"""
    engine = init_camera()
    if engine is None:
        return jsonify({'success': False, 'students': []}), 500

    try:
        students_ref = engine.db.collection('students')
        docs = students_ref.stream()

        students = []
        for doc in docs:
            data = doc.to_dict()
            students.append({
                'id': doc.id,
                'student_id': data.get('student_id', ''),
                'name': data.get('name', 'Unknown'),
                'registered_at': data.get('registered_at', None)
            })

        students.sort(key=lambda x: x.get('registered_at') or '', reverse=True)

        return jsonify({'success': True, 'students': students, 'total': len(students)})
    except Exception as e:
        print(f"[Error] Failed to fetch students: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/delete_student/<student_id>', methods=['DELETE'])
@require_admin
def delete_student(student_id):
    """Delete a student from Firebase"""
    engine = init_camera()
    if engine is None:
        return jsonify({'success': False, 'message': 'Camera not initialized'}), 500

    try:
        engine.db.collection('students').document(student_id).delete()
        engine.last_cache_update = 0

        print(f"[Admin] Deleted student: {student_id}")
        return jsonify({'success': True, 'message': f'Student {student_id} deleted successfully'})
    except Exception as e:
        print(f"[Error] Failed to delete student: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin_logout')
def admin_logout():
    """Logout from admin panel"""
    session.pop('is_admin', None)
    return redirect(url_for('index'))


# ==================== PHASE 3: DOCTOR PORTAL (COURSE-BASED) ====================

@app.route('/doctor_login')
def doctor_login():
    """Auto-login with default course data"""
    session['course_code'] = 'DEFAULT'
    session['course_name'] = 'Bartın Üniversitesi'
    session['doctor_name'] = 'Professor'
    session['start_date'] = datetime.now()
    session['total_lectures'] = 16
    session['class_capacity'] = 50

    print(f"[Doctor] Auto-logged in with default course data")
    return redirect(url_for('course_stats'))


@app.route('/course_stats')
@require_session
def course_stats():
    """Course analytics dashboard with detailed daily attendance timeline"""
    from datetime import timedelta

    course_code = session.get('course_code')
    class_capacity = session.get('class_capacity', 0)
    total_lectures = 30

    turkish_days = {
        0: 'Pazartesi',
        1: 'Salı',
        2: 'Çarşamba',
        3: 'Perşembe',
        4: 'Cuma',
        5: 'Cumartesi',
        6: 'Pazar'
    }

    start_date = session.get('start_date')
    start_dt = None
    if start_date:
        try:
            if hasattr(start_date, 'seconds'):
                start_dt = datetime.fromtimestamp(start_date.seconds).replace(tzinfo=None)
            else:
                start_dt = start_date
                if hasattr(start_dt, 'tzinfo') and start_dt.tzinfo is not None:
                    start_dt = start_dt.replace(tzinfo=None)
        except Exception as e:
            print(f"[Error] Failed to parse start_date: {e}")

    current_day = 1
    if start_dt:
        days_diff = (datetime.now() - start_dt).days
        current_day = max(1, days_diff + 1)

    engine = init_camera()

    lecture_timeline = []
    total_present = 0
    total_absent = 0
    today = datetime.now().date()

    for i in range(total_lectures):
        lecture_date = start_dt + timedelta(days=i) if start_dt else None

        if lecture_date:
            lecture_date_only = lecture_date.date()
            lecture_date_str = lecture_date_only.strftime('%Y-%m-%d')

            weekday_index = lecture_date_only.weekday()
            turkish_day_name = turkish_days[weekday_index]

            day_present = 0
            day_absent = 0

            if engine:
                try:
                    attendance_ref = engine.db.collection('attendance')
                    query = attendance_ref.where('course_code', '==', course_code).where('lecture_date', '==', lecture_date_str)
                    docs = list(query.stream())
                    day_present = len(docs)
                    day_absent = class_capacity - day_present
                except Exception as e:
                    print(f"[Error] Failed to query attendance for {lecture_date_str}: {e}")

            if lecture_date_only < today:
                status = "Completed"
            elif lecture_date_only == today:
                if day_present > 0:
                    status = "In Progress"
                else:
                    status = "Ready to Start"
            else:
                status = "Upcoming"
                day_present = '-'
                day_absent = '-'
        else:
            lecture_date_only = None
            turkish_day_name = "N/A"
            day_present = '-'
            day_absent = '-'
            status = "Unknown"

        if status in ['Completed', 'In Progress'] and day_present != '-':
            attendance_rate = round((day_present / class_capacity * 100), 1) if class_capacity > 0 else 0
        else:
            attendance_rate = None

        lecture_timeline.append({
            'day_num': i + 1,
            'date': lecture_date_only,
            'turkish_day': turkish_day_name,
            'status': status,
            'present': day_present,
            'absent': day_absent,
            'attendance_rate': attendance_rate
        })

        if status == "Completed" and day_present != '-':
            total_present += day_present
            total_absent += day_absent

    remaining_lectures = max(0, total_lectures - current_day)

    return render_template(
        'course_stats.html',
        course_code=session.get('course_code'),
        course_name=session.get('course_name'),
        doctor_name=session.get('doctor_name'),
        current_week=current_day,
        total_lectures=total_lectures,
        remaining_lectures=remaining_lectures,
        class_capacity=class_capacity,
        total_present=total_present,
        total_absent=total_absent,
        lecture_timeline=lecture_timeline
    )


# ==================== PHASE 4: SMART ATTENDANCE ====================

@app.route('/start_attendance_session', methods=['POST'])
@require_session
def start_attendance_session():
    """Start attendance session from course stats with custom duration"""
    data = request.json or {}
    custom_duration = data.get('duration', 90)

    try:
        custom_duration = int(custom_duration)
        if custom_duration < 1:
            custom_duration = 90
    except (ValueError, TypeError):
        custom_duration = 90

    session['session_start'] = time.time()
    session['lecture_duration'] = custom_duration

    return jsonify({'success': True, 'redirect': url_for('attendance')})


@app.route('/attendance')
@require_session
def attendance():
    """Smart attendance tracking page with countdown timer"""
    engine = init_camera()
    if engine:
        engine.stop_camera()
        engine.reset_session()
        engine.start_camera(mode='attendance')

    return render_template(
        'attendance.html',
        doctor_name=session.get('doctor_name'),
        course_name=session.get('course_name'),
        course_code=session.get('course_code'),
        duration=session.get('lecture_duration', 90),
        start_time=session.get('session_start', time.time())
    )


@app.route('/register')
def register():
    """Student registration page (can be accessed from admin or professor)"""
    engine = init_camera()
    if engine:
        engine.stop_camera()
        engine.start_camera(mode='registration')

    return render_template('register.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route for MJPEG"""
    def generate():
        engine = init_camera()
        if engine is None:
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n\r\n'
            return

        while True:
            frame = engine.get_frame()
            if frame is None:
                time.sleep(0.1)
                continue

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )

    return Response(
        generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/api/capture_face', methods=['POST'])
def capture_face():
    """Capture face for registration"""
    data = request.json
    name = data.get('name', '').strip()
    student_id = data.get('student_id', '').strip()

    if not all([name, student_id]):
        return jsonify({'success': False, 'message': 'Name and ID are required'}), 400

    engine = init_camera()
    if engine is None:
        return jsonify({'success': False, 'message': 'Camera not initialized'}), 500

    result = engine.capture_face()
    if result is None:
        return jsonify({'success': False, 'message': 'No face detected. Please position your face in the frame.'}), 400

    face_img, embedding = result

    success, msg_key = engine.register_student(name, student_id, embedding)

    if success:
        return jsonify({'success': True, 'message': f'Successfully registered {name}!'})
    else:
        from translations import TRANSLATIONS
        lang = session.get('lang', 'en')
        message = TRANSLATIONS.get(msg_key, {}).get(lang, 'Registration failed')

        return jsonify({'success': False, 'message': message}), 400


@app.route('/api/get_recognized_students')
def get_recognized_students():
    """Get list of recognized students in current session (only NEW ones)"""
    engine = init_camera()
    if engine is None:
        return jsonify({'students': []})

    recognized = engine.recognized_students

    students = []
    for student_id, info in recognized.items():
        students.append({
            'student_id': student_id,
            'name': info['name'],
            'timestamp': time.strftime('%H:%M:%S', time.localtime(info['timestamp'])),
            'is_marked': student_id in engine.attendance_marked
        })

    students.sort(key=lambda x: x['timestamp'], reverse=True)

    return jsonify({'students': students})


@app.route('/api/mark_attendance', methods=['POST'])
def api_mark_attendance():
    """Mark attendance for recognized students (auto-called from frontend)"""
    if 'course_code' not in session:
        return jsonify({'success': False, 'message': 'No active session'}), 400

    engine = init_camera()
    if engine is None:
        return jsonify({'success': False, 'message': 'Camera not initialized'}), 500

    session_info = {
        'doctor_name': session.get('doctor_name'),
        'course_name': session.get('course_name'),
        'course_code': session.get('course_code')
    }

    newly_marked = []
    for student_id in engine.recognized_students.keys():
        if student_id not in engine.attendance_marked:
            if engine.mark_attendance(student_id, session_info):
                newly_marked.append({
                    'student_id': student_id,
                    'name': engine.recognized_students[student_id]['name']
                })

    return jsonify({
        'success': True,
        'marked_count': len(newly_marked),
        'students': newly_marked
    })


@app.route('/api/session_stats')
def session_stats():
    """Get current session statistics"""
    engine = init_camera()
    if engine is None:
        return jsonify({'total_recognized': 0, 'total_marked': 0})

    return jsonify({
        'total_recognized': len(engine.recognized_students),
        'total_marked': len(engine.attendance_marked)
    })


@app.route('/api/get_lecture_details/<course_code>/<date_str>')
def get_lecture_details(course_code, date_str):
    """Get list of students who attended a specific lecture"""
    engine = init_camera()
    if engine is None:
        return jsonify({'success': False, 'message': 'System not initialized'}), 500

    try:
        attendance_ref = engine.db.collection('attendance')
        query = attendance_ref.where('course_code', '==', course_code).where('lecture_date', '==', date_str)
        docs = query.stream()

        students = []
        for doc in docs:
            data = doc.to_dict()
            marked_at_str = data.get('marked_at', '')
            try:
                marked_time = marked_at_str.split(' ')[1] if ' ' in marked_at_str else marked_at_str
            except Exception:
                marked_time = 'N/A'

            students.append({
                'student_id': data.get('student_id', 'Unknown'),
                'name': data.get('name', 'Unknown'),
                'marked_at': marked_time
            })

        students.sort(key=lambda x: x['marked_at'])

        return jsonify({
            'success': True,
            'students': students,
            'total': len(students)
        })
    except Exception as e:
        print(f"[Error] Failed to fetch lecture details: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/export_attendance/<course_code>/<date_str>')
def export_attendance(course_code, date_str):
    """Export attendance list for a specific lecture to Excel"""
    engine = init_camera()
    if engine is None:
        return jsonify({'success': False, 'message': 'System not initialized'}), 500

    try:
        attendance_ref = engine.db.collection('attendance')
        query = attendance_ref.where('course_code', '==', course_code).where('lecture_date', '==', date_str)
        docs = query.stream()

        attendance_data = []
        for doc in docs:
            data = doc.to_dict()
            marked_at_str = data.get('marked_at', '')
            try:
                marked_time = marked_at_str.split(' ')[1] if ' ' in marked_at_str else marked_at_str
            except Exception:
                marked_time = 'N/A'

            attendance_data.append({
                'Student Name': data.get('name', 'Unknown'),
                'Student ID': data.get('student_id', 'Unknown'),
                'Time Marked': marked_time
            })

        attendance_data.sort(key=lambda x: x['Time Marked'])

        df = pd.DataFrame(attendance_data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Attendance')

            worksheet = writer.sheets['Attendance']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length

        output.seek(0)

        filename = f'Attendance_{course_code}_{date_str}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"[Error] Failed to export attendance: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/delete_attendance/<course_code>/<date_str>', methods=['DELETE'])
def delete_attendance(course_code, date_str):
    """Delete attendance records for a specific lecture"""
    engine = init_camera()
    if engine is None:
        return jsonify({'success': False, 'message': 'System not initialized'}), 500

    try:
        attendance_ref = engine.db.collection('attendance')
        query = attendance_ref.where('course_code', '==', course_code).where('lecture_date', '==', date_str)
        docs = query.stream()

        count = 0
        for doc in docs:
            doc.reference.delete()
            count += 1

        print(f"[Admin] Deleted {count} attendance records for {course_code} on {date_str}")
        return jsonify({'success': True, 'count': count})

    except Exception as e:
        print(f"[Error] Failed to delete attendance: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/end_session', methods=['GET', 'POST'])
def end_session():
    """End the current session with proper attendance finalization"""
    from datetime import timedelta

    engine = init_camera()

    if request.method == 'POST':
        course_code = session.get('course_code')

        if engine and course_code:
            session_info = {
                'doctor_name': session.get('doctor_name'),
                'course_name': session.get('course_name'),
                'course_code': course_code
            }

            final_marked = []
            for student_id in engine.recognized_students.keys():
                if student_id not in engine.attendance_marked:
                    if engine.mark_attendance(student_id, session_info):
                        final_marked.append({
                            'student_id': student_id,
                            'name': engine.recognized_students[student_id]['name']
                        })

            start_date = session.get('start_date')
            if start_date:
                try:
                    if hasattr(start_date, 'seconds'):
                        start_dt = datetime.fromtimestamp(start_date.seconds).replace(tzinfo=None)
                    else:
                        start_dt = start_date
                        if hasattr(start_dt, 'tzinfo') and start_dt.tzinfo is not None:
                            start_dt = start_dt.replace(tzinfo=None)

                    today = datetime.now()
                    days_since_start = (today - start_dt).days
                    current_lecture_week = (days_since_start // 7) + 1

                    print(f"[Session End] Course: {course_code}, Week: {current_lecture_week}")
                    print(f"[Session End] Total Marked: {len(engine.attendance_marked)}")
                    print(f"[Session End] Final Marked: {len(final_marked)}")

                except Exception as e:
                    print(f"[Error] Failed to identify current lecture: {e}")

    if engine:
        engine.stop_camera()
        engine.reset_session()

    is_admin = session.get('is_admin', False)
    has_course = 'course_code' in session

    session.pop('session_start', None)
    session.pop('lecture_duration', None)

    if is_admin:
        return redirect(url_for('admin_dashboard'))
    elif has_course:
        return redirect(url_for('course_stats'))

    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
