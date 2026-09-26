from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (
    Student,
    Faculty,
    Subject,
    AttendanceSession,
    AttendanceRecord,
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

def home(request):
    return render(request, "attendance/home.html")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@login_required
def dashboard(request):

    student_count = Student.objects.count()
    subject_count = Subject.objects.count()
    session_count = AttendanceSession.objects.count()

    context = {
        "student_count": student_count,
        "subject_count": subject_count,
        "session_count": session_count,
    }

    return render(
        request,
        "attendance/dashboard.html",
        context
    )


# --------------------------------------------------
# MARK ATTENDANCE
# --------------------------------------------------

@login_required
def mark_attendance(request):

    # Only faculty can mark attendance
    try:
        faculty = Faculty.objects.get(user=request.user)

    except Faculty.DoesNotExist:

        messages.error(
            request,
            "Only faculty members can mark attendance."
        )

        return redirect("dashboard")


    # Show only subjects assigned to this faculty
    subjects = Subject.objects.filter(
        faculty=faculty
    )


    # Initially show students from faculty department
    students = Student.objects.filter(
        department=faculty.department
    )


    if request.method == "POST":

        subject_id = request.POST.get("subject")
        section = request.POST.get("section")


        # Validate subject and make sure it belongs
        # to the logged-in faculty
        subject = get_object_or_404(
            Subject,
            id=subject_id,
            faculty=faculty
        )


        # Get only students from selected section
        students = Student.objects.filter(
            department=faculty.department,
            section=section
        )


        # Prevent duplicate attendance session
        existing_session = AttendanceSession.objects.filter(
            subject=subject,
            faculty=faculty,
            date=timezone.now().date(),
            section=section
        ).exists()


        if existing_session:

            messages.error(
                request,
                "Attendance has already been marked "
                "for this subject today."
            )

            return redirect("mark_attendance")


        # Create attendance session
        session = AttendanceSession.objects.create(
            subject=subject,
            faculty=faculty,
            date=timezone.now().date(),
            section=section
        )


        # Save each student's attendance
        for student in students:

            status = request.POST.get(
                f"student_{student.id}"
            )

            if status in ["P", "A"]:

                AttendanceRecord.objects.create(
                    session=session,
                    student=student,
                    status=status
                )


        messages.success(
            request,
            "Attendance saved successfully!"
        )

        return redirect("mark_attendance")


    context = {
        "students": students,
        "subjects": subjects,
    }

    return render(
        request,
        "attendance/mark_attendance.html",
        context
    )


# --------------------------------------------------
# ATTENDANCE HISTORY
# --------------------------------------------------

@login_required
def attendance_history(request):

    sessions = AttendanceSession.objects.select_related(
        "subject",
        "faculty",
        "faculty__user"
    ).order_by(
        "-date",
        "-created_at"
    )

    context = {
        "sessions": sessions
    }

    return render(
        request,
        "attendance/history.html",
        context
    )


# --------------------------------------------------
# SESSION DETAILS
# --------------------------------------------------

@login_required
def session_detail(request, session_id):

    session = get_object_or_404(
        AttendanceSession,
        id=session_id
    )


    records = session.records.select_related(
        "student",
        "student__user"
    )


    context = {
        "session": session,
        "records": records,
    }


    return render(
        request,
        "attendance/session_detail.html",
        context
    )


# --------------------------------------------------
# EDIT / CORRECT ATTENDANCE
# --------------------------------------------------

@login_required
def edit_attendance(request, record_id):

    record = get_object_or_404(
        AttendanceRecord,
        id=record_id
    )


    # Only faculty can modify attendance
    try:
        faculty = Faculty.objects.get(
            user=request.user
        )

    except Faculty.DoesNotExist:

        messages.error(
            request,
            "Only faculty members can modify attendance."
        )

        return redirect("dashboard")


    # Faculty should only edit attendance
    # for their own subject/session
    if record.session.faculty != faculty:

        messages.error(
            request,
            "You do not have permission "
            "to modify this attendance."
        )

        return redirect("attendance_history")


    if request.method == "POST":

        status = request.POST.get("status")


        if status not in ["P", "A"]:

            messages.error(
                request,
                "Invalid attendance status."
            )

            return redirect(
                "edit_attendance",
                record_id=record.id
            )


        record.status = status
        record.save()


        messages.success(
            request,
            "Attendance updated successfully!"
        )


        return redirect(
            "session_detail",
            session_id=record.session.id
        )


    return render(
        request,
        "attendance/edit_attendance.html",
        {
            "record": record
        }
    )


# --------------------------------------------------
# LOW ATTENDANCE REPORT
# --------------------------------------------------

@login_required
def low_attendance(request):

    students = Student.objects.select_related(
        "user",
        "department"
    )

    subjects = Subject.objects.all()

    report = []


    for student in students:

        for subject in subjects:

            records = AttendanceRecord.objects.filter(
                student=student,
                session__subject=subject
            )


            total_classes = records.count()


            # Skip subjects where no classes
            # have been conducted
            if total_classes == 0:
                continue


            present_classes = records.filter(
                status="P"
            ).count()


            percentage = (
                present_classes / total_classes
            ) * 100


            # Low attendance threshold
            if percentage < 75:

                report.append({
                    "student": student,
                    "subject": subject,
                    "total": total_classes,
                    "present": present_classes,
                    "percentage": round(
                        percentage,
                        2
                    ),
                })


    context = {
        "report": report
    }


    return render(
        request,
        "attendance/low_attendance.html",
        context
    )