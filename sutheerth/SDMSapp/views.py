from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from SDMSapp.models import Student, Stud_item
from .forms import *
from django.views import View
from .forms import SearchForm
from django.contrib import messages
from django.shortcuts import render, redirect
from SDMSapp.models import Student, Programme, Department  # Import your models
from .forms import *
from datetime import datetime
from django.http import HttpResponse

#from .forms import PlayerForm, Player, DepartmentForm, Sportform


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Handle invalid login
            return render(request, 'SDMSapp/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'SDMSapp/login.html')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'SDMSapp/signup.html', {'form': form})

@login_required
def user_home(request):
    student={
        'student':Student.objects.all
    }
    return render(request, 'SDMSapp/home.html',student)


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_student') 
    else:
        form = StudentForm()
    return render(request, 'SDMSapp/addstudent.html', {'form': form})

def success_page(request):
    return render(request, 'SDMSapp/success_page.html')

def view_student(request):
    # Query all student records
    students = Student.objects.all()
    return render(request, 'SDMSapp/view_student.html', {'students': students})

def search_student(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            uty_reg_no = form.cleaned_data['uty_reg_no']
            return redirect('edit_student', uty_reg_no=uty_reg_no)
    else:
        form = SearchForm()
    return render(request, 'search_student.html', {'form': form})


@login_required
def edit_student_form(request):
    if request.method == 'POST':
        uty_reg_no = request.POST.get('uty_reg_no')
        if Student.objects.filter(uty_reg_no=uty_reg_no).exists():
            return redirect('edit_student', uty_reg_no=uty_reg_no)
        else:
            messages.error(request, "Student ID not found.")
            return redirect('edit_student_form')
    return render(request, 'SDMSapp/edit_student_form.html')

@login_required
def edit_student(request, uty_reg_no):
    if request.method == 'POST':
        name = request.POST.get('name')
        year_of_admission = request.POST.get('year_of_admission')
        admission_no = request.POST.get('admission_no')
        department_id = request.POST.get('department_id')
        phone_number = request.POST.get('phone_number')
        aadhar_number = request.POST.get('aadhar_number')
        dob = request.POST.get('dob')
        programme_id = request.POST.get('programme_id')
        place = request.POST.get('place')
        city = request.POST.get('city')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')

        department_id = request.POST.get('department')
        department = get_object_or_404(Department, dept_name=department_id)
        programme = get_object_or_404(Programme, id=programme_id)

        edit = get_object_or_404(Student, uty_reg_no=uty_reg_no)
        edit.name = name
        edit.year_of_admission = year_of_admission
        edit.admission_no = admission_no
        edit.programme = programme
        edit.place = place
        edit.department = department
        edit.phone_number = phone_number
        edit.aadhar_number = aadhar_number
        edit.dob = dob
        edit.city = city
        edit.district = district
        edit.pincode = pincode
        edit.save()

        messages.info(request, "Data Updated Successfully")
        return redirect("/")

    student = get_object_or_404(Student, uty_reg_no=uty_reg_no)
    departments = Department.objects.all()
    programmes = Programme.objects.all()
    context = {"student": student, "departments": departments, "programmes": programmes}
    return render(request, 'SDMSapp/edit_student.html', context)

@login_required
def delete_student(request, uty_reg_no):
    student = get_object_or_404(Student, uty_reg_no=uty_reg_no)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('view_student')

@login_required
def confirm_delete_student(request, uty_reg_no):
    student = get_object_or_404(Student, uty_reg_no=uty_reg_no)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('view_student')
    return render(request, 'SDMSapp/confirm_delete_student.html', {'student': student})

def user_logout(request):
    logout(request)
    return redirect('home')    

@login_required
def assign_student(request):
    if request.method == 'POST':
        form = Assign_StudentForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('assignview_student')
    else:
        form = Assign_StudentForm()
    return render(request, 'SDMSapp/assign_student.html', {'form': form})

def assignview_student(request):
        query = request.GET.get('q')
        if query:
            assignments = Stud_item.objects.filter(
                Q(stud__name__icontains=query) |
                Q(stud__uty_reg_no__icontains=query) |
                Q(item__item_name__icontains=query)
            )
        else:
            assignments = Stud_item.objects.all()
        return render(request, 'SDMSapp/search_assignments.html', {'assignments': assignments, 'query': query})

@login_required
def confirm_assign_delete(request, stud_id):
    stud_item = get_object_or_404(Stud_item, id = stud_id)
    if request.method == 'GET':
        stud_item.delete()
        return redirect('assignview_student')
    return render(request, 'SDMSapp/assign_view.html', {'stud_item': stud_item})

@login_required
def view_items(request):
    items = Item.objects.all()
    years = Stud_item.objects.values_list('year', flat=True).distinct()
    return render(request, 'SDMSapp/view_items.html', {'items': items, 'years': years})

@login_required
def view_players(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    year = request.GET.get('year')
    stud_items = Stud_item.objects.filter(item=item, year=year)
    return render(request, 'SDMSapp/view_players.html', {'item': item, 'stud_items': stud_items, 'year':year})

@login_required
def edit_assign(request, id):
    stud_item = get_object_or_404(Stud_item, id=id)
    if request.method == 'POST':
        form = AssignStudentForm(request.POST, instance=stud_item)
        if form.is_valid():
            form.save()
            return redirect('view_players', item_id=stud_item.item.id)
    else:
        form = AssignStudentForm(instance=stud_item)
    return render(request, 'SDMSapp/edit_assign.html', {'form': form})

@login_required
def edit_assignment(request, pk):
    stud_item = get_object_or_404(Stud_item, pk=pk)
    if request.method == 'POST':
        form = StudItemForm(request.POST, instance=stud_item)
        if form.is_valid():
            form.save()
            return redirect('view_items')
    else:
        form = StudItemForm(instance=stud_item)
    return render(request, 'SDMSapp/edit_assignment.html', {'form': form})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page or another view
    else:
        form = AttendanceForm()
    return render(request, 'SDMSapp/mark_attendance.html', {'form': form})

@login_required
def view_attendance(request):
    # Get attendance records for the selected date if provided
    date = request.GET.get('date', None)
    if date:
        attendance_records = Attendance.objects.filter(date=date)
    else:
        attendance_records = Attendance.objects.all()

    return render(request, 'SDMSapp/view_attendance.html', {'attendance_records': attendance_records, 'selected_date': date})


@login_required
def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'GET':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('view_attendance')  # Replace with your attendance list view name
    else:
        return redirect('view_attendance')


def upload_picture(request):
    if request.method == 'POST':
        form = PictureUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_picture')
    else:
        form = PictureUploadForm()
    return render(request, 'SDMSapp/upload_picture.html', {'form': form})

def view_pictures(request):
    items = Item.objects.all()
    pictures = []
    current_year = datetime.now().year
    if 'item' in request.GET and 'year' in request.GET:
        item_id = request.GET.get('item')
        year = request.GET.get('year')
        pictures = Picture.objects.filter(item_id=item_id, year=year)
    return render(request, 'SDMSapp/view_picture.html', {'items': items, 'pictures': pictures, 'current_year': current_year})

def download_picture(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    response = HttpResponse(picture.image, content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{picture.image.name}"'
    return response

@login_required
def assign_players(request):
    if request.method == 'POST':
        form = AssignStudentsToTeamForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            selected_students = form.cleaned_data['students']
            # Remove existing assignments for the selected item
            Stud_item.objects.filter(item=item).delete()
            # Assign selected students to the item
            for student in selected_students:
                Stud_item.objects.create(stud=student, item=item)
            return redirect('success_page')  # Redirect to a success page or another appropriate page
    else:
        item_id = request.GET.get('item_id')
        assigned_students = Stud_item.objects.filter(item_id=item_id).values_list('stud', flat=True)
        form = AssignStudentsToTeamForm(assigned_students=assigned_students)

    return render(request, 'SDMSapp/assign_players.html', {'form': form})

def view_profile(request, uty_reg_no):
    student = get_object_or_404(Student, uty_reg_no=uty_reg_no)
    return render(request, 'SDMSapp/profile.html', {'student': student})
