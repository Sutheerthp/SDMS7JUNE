from django.db import models

class Department(models.Model):
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.dept_name)

class Programme(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=50)
    year_of_admission = models.IntegerField()
    admission_no = models.IntegerField()
    programme_id = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    uty_reg_no = models.CharField(max_length=50, unique = True)
    place = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    dob = models.DateField(null =True)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    DISTRICT = [
    ('ALAPPUZHA', 'Alappuzha'),
    ('ERNAKULAM', 'Ernakulam'),
    ('IDUKKI', 'Idukki'),
    ('KANNUR', 'Kannur'),
    ('KASARAGOD', 'Kasaragod'),
    ('KOLLAM', 'Kollam'),
    ('KOTTAYAM', 'Kottayam'),
    ('KOZHIKODE', 'Kozhikode'),
    ('MALAPPURAM', 'Malappuram'),
    ('PALAKKAD', 'Palakkad'),
    ('PATHANAMTHITTA', 'Pathanamthitta'),
    ('THIRUVANANTHAPURAM', 'Thiruvananthapuram'),
    ('THRISSUR', 'Thrissur'),
    ('WAYANAD', 'Wayanad'),
]

    district = models.CharField(max_length=50,  choices=DISTRICT, default='Active')
    pincode = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)

class Item(models.Model):
    item_name = models.CharField(max_length=50)
    ITEM_TYPE = [
         ('SPORTS', 'SPORTS'),
         ('ATHLETICS', 'ATHLETICS'),
    ]
    item_type = models.CharField(max_length=50,  choices=ITEM_TYPE, default='Active')
    no_of_players = models.IntegerField()

    def __str__(self):
        return str(self.item_name)

class Stud_item(models.Model):
    stud = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    
    PLAYER_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    player_status = models.CharField(max_length=10, choices=PLAYER_STATUS_CHOICES, default='Active')
    
    UTY_SELECTION_STATUS_CHOICES = [
        ('Selected', 'Selected'),
        ('Not Selected', 'Not Selected'),
    ]
    uty_team_selection = models.CharField(max_length=20, choices=UTY_SELECTION_STATUS_CHOICES, default='Not Selected')
    
    position = models.IntegerField(default=0)
    year = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.stud.name} - {self.item.item_name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null= True)
    date = models.DateField()
    hour_1 = models.BooleanField(default=False)
    hour_2 = models.BooleanField(default=False)
    hour_3 = models.BooleanField(default=False)
    hour_4 = models.BooleanField(default=False)
    hour_5 = models.BooleanField(default=False)

    @property
    def hour_1_missed(self):
        return not self.hour_1

    @property
    def hour_2_missed(self):
        return not self.hour_2

    @property
    def hour_3_missed(self):
        return not self.hour_3

    @property
    def hour_4_missed(self):
        return not self.hour_4

    @property
    def hour_5_missed(self):
        return not self.hour_5

    def __str__(self):
        return f"{self.student.name} - {self.date}"
