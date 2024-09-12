---
layout: post
title: "HOF practice part 3"
date: 2024-09-12
---

- This program analyzes a dataset of employees working in a tech company, performing tasks like salary analysis, calculating bonuses, and filtering employees based on various criteria 

#### Problem Outline 
- We have a list of employees where each employee is represented by a dictionary containing details such as their name, salary, department,and performance rating. We'll use various techniques to process this data, including 
- **Currying** to apply bonuses 
- **Map** to adjust salaries 
- **filter** to extract specific employees
- **reduce**  to aggregate overall company data


```python
from functools import reduce

# Sample Employee Data
employees = [
    {"name": "Alice", "salary": 120000, "department": "Engineering", "rating": 4.5},
    {"name": "Bob", "salary": 80000, "department": "Marketing", "rating": 3.2},
    {"name": "Charlie", "salary": 95000, "department": "Engineering", "rating": 4.0},
    {"name": "David", "salary": 70000, "department": "HR", "rating": 3.8},
    {"name": "Eve", "salary": 150000, "department": "Engineering", "rating": 4.7},
    {"name": "Frank", "salary": 60000, "department": "HR", "rating": 2.8},
    {"name": "Grace", "salary": 110000, "department": "Marketing", "rating": 4.1},
]

# 1. Regular Function: Apply Bonus to Salary
def apply_bonus(percentage_bonus):
    """Currying Function to apply a bonus to salary."""
    def inner_bonus(employee):
        new_salary = employee['salary'] * (1 + percentage_bonus / 100)
        return {**employee, "salary": new_salary}
    return inner_bonus

# Apply a 10% bonus
apply_10_bonus = apply_bonus(10)

# 2. Using map to apply a bonus to all employees
def update_salaries_with_bonus(employee_list, bonus_function):
    """Map function to apply a bonus function to all employees."""
    return list(map(bonus_function, employee_list))

# Update the salaries for all employees with a 10% bonus
updated_salaries = update_salaries_with_bonus(employees, apply_10_bonus)

# 3. Filter Function: Employees with High Performance
def high_performance(employee):
    """Filter function to find employees with ratings above 4."""
    return employee['rating'] >= 4.0

# Using filter to find high-performance employees
high_performers = list(filter(high_performance, updated_salaries))

# 4. Reduce Function: Sum Total Salaries of All Employees
def sum_salaries(accumulator, employee):
    """Reduce function to sum up all employee salaries."""
    return accumulator + employee['salary']

# Calculate the total salary of all employees
total_salary = reduce(sum_salaries, updated_salaries, 0)

# 5. HOF: Salary Comparison Function (Returns a Function)
def salary_comparator(min_salary):
    """Higher-order function that returns a function to compare salary."""
    return lambda employee: employee['salary'] >= min_salary

# Use salary comparator to filter employees earning more than 100K
high_earners = list(filter(salary_comparator(100000), updated_salaries))

# 6. Currying: Function to Compare Ratings
def rating_comparator(min_rating):
    """Currying function to compare employee ratings."""
    return lambda employee: employee['rating'] >= min_rating

# Find employees with ratings of 4.5 or more
top_performers = list(filter(rating_comparator(4.5), updated_salaries))

# Display Results
def display_employee_data(employee_list):
    """Display employee details."""
    for emp in employee_list:
        print(f"Name: {emp['name']}, Salary: {emp['salary']}, Department: {emp['department']}, Rating: {emp['rating']}")
    print("-------------------------------")

# Main execution to display various results
if __name__ == "__main__":
    print("Updated Salaries with Bonus:")
    display_employee_data(updated_salaries)

    print("High Performers (Rating >= 4.0):")
    display_employee_data(high_performers)

    print(f"Total Company Salary (After Bonus): ${total_salary}")

    print("High Earners (Salary >= 100,000):")
    display_employee_data(high_earners)

    print("Top Performers (Rating >= 4.5):")
    display_employee_data(top_performers)

```

    Updated Salaries with Bonus:
    Name: Alice, Salary: 132000.0, Department: Engineering, Rating: 4.5
    Name: Bob, Salary: 88000.0, Department: Marketing, Rating: 3.2
    Name: Charlie, Salary: 104500.00000000001, Department: Engineering, Rating: 4.0
    Name: David, Salary: 77000.0, Department: HR, Rating: 3.8
    Name: Eve, Salary: 165000.0, Department: Engineering, Rating: 4.7
    Name: Frank, Salary: 66000.0, Department: HR, Rating: 2.8
    Name: Grace, Salary: 121000.00000000001, Department: Marketing, Rating: 4.1
    -------------------------------
    High Performers (Rating >= 4.0):
    Name: Alice, Salary: 132000.0, Department: Engineering, Rating: 4.5
    Name: Charlie, Salary: 104500.00000000001, Department: Engineering, Rating: 4.0
    Name: Eve, Salary: 165000.0, Department: Engineering, Rating: 4.7
    Name: Grace, Salary: 121000.00000000001, Department: Marketing, Rating: 4.1
    -------------------------------
    Total Company Salary (After Bonus): $753500.0
    High Earners (Salary >= 100,000):
    Name: Alice, Salary: 132000.0, Department: Engineering, Rating: 4.5
    Name: Charlie, Salary: 104500.00000000001, Department: Engineering, Rating: 4.0
    Name: Eve, Salary: 165000.0, Department: Engineering, Rating: 4.7
    Name: Grace, Salary: 121000.00000000001, Department: Marketing, Rating: 4.1
    -------------------------------
    Top Performers (Rating >= 4.5):
    Name: Alice, Salary: 132000.0, Department: Engineering, Rating: 4.5
    Name: Eve, Salary: 165000.0, Department: Engineering, Rating: 4.7
    -------------------------------

