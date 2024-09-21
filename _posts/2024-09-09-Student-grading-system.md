---
layout: post
title: " Practicing Higher Order Functions and Regular Functions part 1 "
date: 2024-09-09
permalink: /posts/:title
categories: [Reading Python]
---

- let's create a simple student grading system where we use both regular functions and higher-order functions to implement different features 
- This project has the following features

  - **calculate total marks** for each student 
  - **determine grades** based on total marks 
  - **filter** students who passed(scored more than 40)
  - **create a higher-order function** that dynamically generates functions for bonuses
- The program has the following components 
  - **Normal functions** to calculate the total marks and determine grades 
  - **Higher-order functions** for applying dynamic bonuses to the marks and filtering students 
  


```python
# Student data: Each tuple contains (name, subject marks)
students = [
    ("Alice", [80, 75, 90]),
    ("Bob", [40, 42, 39]),
    ("Charlie", [30, 28, 35]),
    ("David", [85, 88, 90]),
    ("Eve", [60, 62, 70])
]

# 1. Normal Function to calculate total marks for each student
def calculate_total(marks):
    return sum(marks)

# 2. Normal Function to determine the grade based on average marks
def determine_grade(total_marks, num_subjects):
    average_marks = total_marks / num_subjects
    if average_marks >= 75:
        return "A"
    elif average_marks >= 60:
        return "B"
    elif average_marks >= 50:
        return "C"
    elif average_marks >= 40:
        return "D"
    else:
        return "F"

# 3. Higher-order function that returns a function to apply bonus
def bonus_adder(bonus):
    def add_bonus(marks):
        return [mark + bonus for mark in marks]
    return add_bonus

# Apply a bonus of 5 marks to all students
add_five_bonus = bonus_adder(5)

# 4. Higher-order function to filter students who passed based on original marks
def filter_passed_students(students, passing_func):
    return [student for student in students if passing_func(student)]

# Define passing criteria as scoring more than 40 marks on average (using original marks)
def has_passed(student):
    name, marks = student
    return calculate_total(marks) / len(marks) >= 40

# 5. Let's process the data
def process_students(students, add_bonus_func=None):
    for student in students:
        name, original_marks = student
        num_subjects = len(original_marks)
        
        # Calculate total marks BEFORE applying the bonus for grading
        total_marks_before_bonus = calculate_total(original_marks)
        grade = determine_grade(total_marks_before_bonus, num_subjects)
        
        # Apply bonus if bonus function is provided
        if add_bonus_func:
            marks_after_bonus = add_bonus_func(original_marks)
        else:
            marks_after_bonus = original_marks
        total_marks_after_bonus = calculate_total(marks_after_bonus)
        
        print(f"Student: {name}")
        print(f"Original Marks: {original_marks}")
        print(f"Total Marks (after bonus): {total_marks_after_bonus}")
        print(f"Grade (before bonus): {grade}")
        print("-" * 20)

# 6. Display all students' grades
print("All Students Grades:")
process_students(students, add_five_bonus)

# 7. Display only passed students based on original marks (without bonus)
passed_students = filter_passed_students(students, has_passed)
print("Passed Students:")
for student in passed_students:
    print(student[0])
```

    All Students Grades:
    Student: Alice
    Original Marks: [80, 75, 90]
    Total Marks (after bonus): 260
    Grade (before bonus): A
    --------------------
    Student: Bob
    Original Marks: [40, 42, 39]
    Total Marks (after bonus): 136
    Grade (before bonus): D
    --------------------
    Student: Charlie
    Original Marks: [30, 28, 35]
    Total Marks (after bonus): 108
    Grade (before bonus): F
    --------------------
    Student: David
    Original Marks: [85, 88, 90]
    Total Marks (after bonus): 278
    Grade (before bonus): A
    --------------------
    Student: Eve
    Original Marks: [60, 62, 70]
    Total Marks (after bonus): 207
    Grade (before bonus): B
    --------------------
    Passed Students:
    Alice
    Bob
    David
    Eve

