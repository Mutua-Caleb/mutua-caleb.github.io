---
layout: post
title: "Fleet Management System"
date: 2024-09-16
---

Imagine you're designing a fleet management system for a logistic company. You want to track vehicles, calculate efficiency, handle different kinds of data filtering, and aggregate results. This system needs to
1. Represent vehicles using a class with special methods(dunder methods) to compare, add vehicles, calculate fuel efficiency. 
2. Use HOF to apply actions on the vehicles dynamically, such as upgrading fuel capacity or mileage 
3. Use functional programming to process large sets of data efficiently, using  `map`  `filter` ,  `reduce` 
4. Take advantage of  `itertools`  to analyse combinations of vehicle routes for optimisation. 
5. Leverage decorators to add logging for tracking function calls or augment the behavior of certain functions
6. Implement currying for flexibility in handling vehicle related tasks dynamically 

**Step-by-step breakdown**
1. Vehicles and Fuel efficiency: 
   * each vehicle has properties like mileage, fuel capacity, and distance traveled. We'll use a class to represent vehicles  
   * The class will implement dunder methods like  `__add__` (to add two vehicles, eg. merging fuel tanks),  `__eq__`  to compare vehicles efficiency, and  `repr`  ( for a readable string representation)
2. Actions on Vehicles
   1. Functions will dynamically apply upgrades to vehicles using HOF
   2. A decorator will log each upgrade or comparison between vehicles 
3. Processing large data: 
   1.  `map` ,  `filter`  and  `reduce` will be used to analyze and transform vehicle data, e.g filtering out inefficient vehicles, mapping maintenance tasks, or aggregating total fleet capacity. 
4. Route optimisation 
   1. Use  `itertools` to generate combinations of routes that can be handled by different vehicles to optimise fuel efficiency or delivery time. 


```python
from functools import reduce, wraps
import itertools

# Custom Exceptions
class FleetError(Exception):
    """Base class for exceptions in the fleet management system."""
    pass

class InsufficientFuelError(FleetError):
    """Raised when a vehicle has insufficient fuel."""
    pass

class VehicleNotFoundError(FleetError):
    """Raised when a vehicle is not found in the fleet."""
    pass

# Decorator for logging actions
def log_action(func):
    """Decorator that logs the function calls and results."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Action: {func.__name__}, Args: {args}, Kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            print(f"Result: {result}")
            return result
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

# Vehicle Class with Additional Features
class Vehicle:
    """Represents a vehicle in the fleet."""
    def __init__(self, name, mileage, fuel_capacity, distance_traveled=0):
        """Initializes the vehicle."""
        self.name = name
        self.mileage = mileage
        self.fuel_capacity = fuel_capacity
        self.distance_traveled = distance_traveled

    def __repr__(self):
        """Returns the string representation of the vehicle."""
        return f"Vehicle({self.name}, MPG: {self.mileage}, Capacity: {self.fuel_capacity} gallons)"

    def __add__(self, other):
        """Adds two vehicles' fuel capacity."""
        if not isinstance(other, Vehicle):
            raise ValueError("Can only add two vehicles together.")
        return Vehicle(f"{self.name} & {other.name}",
                       (self.mileage + other.mileage) / 2,
                       self.fuel_capacity + other.fuel_capacity,
                       self.distance_traveled + other.distance_traveled)

    def __eq__(self, other):
        """Compares the fuel efficiency of two vehicles."""
        return self.mileage == other.mileage

    def fuel_efficiency(self):
        """Calculates fuel efficiency based on distance and fuel consumed."""
        try:
            return self.distance_traveled / self.fuel_capacity
        except ZeroDivisionError:
            raise InsufficientFuelError(f"{self.name} has insufficient fuel to calculate efficiency.")

    def to_dict(self):
        """Converts vehicle attributes to a dictionary."""
        return {
            'name': self.name,
            'mileage': self.mileage,
            'fuel_capacity': self.fuel_capacity,
            'distance_traveled': self.distance_traveled
        }

# Higher Order Functions (HOF)
@log_action
def apply_upgrade(vehicle, upgrade_function):
    """Applies a dynamic upgrade to a vehicle."""
    return upgrade_function(vehicle)

# Function with positional, keyword, and arbitrary arguments
@log_action
def vehicle_info(vehicle, *args, efficiency=True, **kwargs):
    """Returns detailed info about the vehicle."""
    info = f"Vehicle Info: {vehicle.name}, Mileage: {vehicle.mileage}, Fuel: {vehicle.fuel_capacity}"
    if efficiency:
        info += f", Efficiency: {vehicle.fuel_efficiency()} miles/gallon"
    return info

# Functional Programming with map, filter, reduce
@log_action
def fleet_analysis(fleet):
    """Performs analysis on the fleet using map, filter, reduce."""
    efficient_vehicles = [v for v in fleet if v.mileage >= 15]
    upgraded_fleet = [Vehicle(v.name, v.mileage, v.fuel_capacity * 1.1, v.distance_traveled) for v in efficient_vehicles]
    total_fuel_capacity = reduce(lambda x, y: x + y.fuel_capacity, upgraded_fleet, 0)
    return efficient_vehicles, upgraded_fleet, total_fuel_capacity

# Use itertools for combinations
@log_action
def optimize_routes(fleet, routes):
    """Generates all possible vehicle-route combinations using itertools."""
    return list(itertools.product(fleet, routes))

# Replacing the match-case block with if-elif-else logic
def analyze_vehicle(vehicle):
    """Analyzes vehicle based on mileage."""
    mileage = vehicle.mileage
    if mileage >= 20:
        return f"{vehicle.name} is highly efficient."
    elif 15 <= mileage < 20:
        return f"{vehicle.name} is moderately efficient."
    else:
        return f"{vehicle.name} is inefficient."

# Custom Exceptions and Exception Handling
@log_action
def check_fleet(fleet):
    """Checks fleet for issues and handles exceptions."""
    if not fleet:
        raise FleetError("The fleet is empty.")
    try:
        for vehicle in fleet:
            if vehicle.fuel_capacity <= 0:
                raise InsufficientFuelError(f"{vehicle.name} has no fuel.")
    except FleetError as e:
        print(f"Fleet issue detected: {e}")
        raise  # Exception chaining can happen here if needed.

# Example of set usage and list comprehensions
def set_operations(fleet):
    """Performs set operations and uses list comprehensions on the fleet."""
    vehicle_names = {v.name for v in fleet}
    vehicle_data = {v.name: v.to_dict() for v in fleet}
    print(f"Vehicle Names (Set): {vehicle_names}")
    print(f"Vehicle Data (Dict): {vehicle_data}")
    nested_comprehension = [[v.mileage, v.fuel_capacity] for v in fleet if v.mileage > 15]
    print(f"Nested Comprehension Result: {nested_comprehension}")

# Main Program
if __name__ == "__main__":
    vehicle1 = Vehicle("Truck A", mileage=12, fuel_capacity=50, distance_traveled=600)
    vehicle2 = Vehicle("Truck B", mileage=16, fuel_capacity=40, distance_traveled=800)
    vehicle3 = Vehicle("Van C", mileage=18, fuel_capacity=30, distance_traveled=500)

    fleet = [vehicle1, vehicle2, vehicle3]
    
    # Example of positional, keyword, and arbitrary argument functions
    vehicle_info(vehicle1, efficiency=True)
    
    # Error Handling and Raising Custom Exceptions
    try:
        check_fleet(fleet)
    except FleetError as e:
        print(f"Handled Fleet Error: {e}")

    # Perform fleet analysis
    fleet_analysis(fleet)
    
    # Route optimization
    routes = ['Route 1', 'Route 2', 'Route 3']
    optimize_routes(fleet, routes)
    
    # Analyze vehicles
    print(analyze_vehicle(vehicle1))

    # Set operations and comprehensions
    set_operations(fleet)
    
    # Del statement example
    del fleet[0]
    print(f"Updated Fleet: {fleet}")

```

    Action: vehicle_info, Args: (Vehicle(Truck A, MPG: 12, Capacity: 50 gallons),), Kwargs: {'efficiency': True}
    Result: Vehicle Info: Truck A, Mileage: 12, Fuel: 50, Efficiency: 12.0 miles/gallon
    Action: check_fleet, Args: ([Vehicle(Truck A, MPG: 12, Capacity: 50 gallons), Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), Vehicle(Van C, MPG: 18, Capacity: 30 gallons)],), Kwargs: {}
    Result: None
    Action: fleet_analysis, Args: ([Vehicle(Truck A, MPG: 12, Capacity: 50 gallons), Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), Vehicle(Van C, MPG: 18, Capacity: 30 gallons)],), Kwargs: {}
    Result: ([Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), Vehicle(Van C, MPG: 18, Capacity: 30 gallons)], [Vehicle(Truck B, MPG: 16, Capacity: 44.0 gallons), Vehicle(Van C, MPG: 18, Capacity: 33.0 gallons)], 77.0)
    Action: optimize_routes, Args: ([Vehicle(Truck A, MPG: 12, Capacity: 50 gallons), Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), Vehicle(Van C, MPG: 18, Capacity: 30 gallons)], ['Route 1', 'Route 2', 'Route 3']), Kwargs: {}
    Result: [(Vehicle(Truck A, MPG: 12, Capacity: 50 gallons), 'Route 1'), (Vehicle(Truck A, MPG: 12, Capacity: 50 gallons), 'Route 2'), (Vehicle(Truck A, MPG: 12, Capacity: 50 gallons), 'Route 3'), (Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), 'Route 1'), (Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), 'Route 2'), (Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), 'Route 3'), (Vehicle(Van C, MPG: 18, Capacity: 30 gallons), 'Route 1'), (Vehicle(Van C, MPG: 18, Capacity: 30 gallons), 'Route 2'), (Vehicle(Van C, MPG: 18, Capacity: 30 gallons), 'Route 3')]
    Truck A is inefficient.
    Vehicle Names (Set): {'Van C', 'Truck A', 'Truck B'}
    Vehicle Data (Dict): {'Truck A': {'name': 'Truck A', 'mileage': 12, 'fuel_capacity': 50, 'distance_traveled': 600}, 'Truck B': {'name': 'Truck B', 'mileage': 16, 'fuel_capacity': 40, 'distance_traveled': 800}, 'Van C': {'name': 'Van C', 'mileage': 18, 'fuel_capacity': 30, 'distance_traveled': 500}}
    Nested Comprehension Result: [[16, 40], [18, 30]]
    Updated Fleet: [Vehicle(Truck B, MPG: 16, Capacity: 40 gallons), Vehicle(Van C, MPG: 18, Capacity: 30 gallons)]

