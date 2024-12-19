from typing import List, Dict
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def convert_to_print_jobs(jobs: List[Dict]) -> List[PrintJob]:
    return [PrintJob(**job) for job in jobs]

def group_by_priority(jobs: List[PrintJob]) -> dict:
    priority_groups = defaultdict(list)
    for job in jobs:
        priority_groups[job.priority].append(job)
    return dict(sorted(priority_groups.items()))  # Sort by priority (1 is highest)

def can_print_together(jobs: List[PrintJob], constraints: PrinterConstraints) -> bool:
    total_volume = sum(job.volume for job in jobs)
    return (total_volume <= constraints.max_volume and 
            len(jobs) <= constraints.max_items)

def find_print_groups(jobs: List[PrintJob], constraints: PrinterConstraints) -> List[List[PrintJob]]:
    if not jobs:
        return []
    
    current_group = []
    current_volume = 0
    groups = []
    
    for job in jobs:
        if (len(current_group) < constraints.max_items and 
            current_volume + job.volume <= constraints.max_volume):
            current_group.append(job)
            current_volume += job.volume
        else:
            if current_group:
                groups.append(current_group)
            current_group = [job]
            current_volume = job.volume
    
    if current_group:
        groups.append(current_group)
    
    return groups

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера
    """
    # Convert input data to dataclasses
    jobs = convert_to_print_jobs(print_jobs)
    printer_constraints = PrinterConstraints(**constraints)
    
    # Group jobs by priority
    priority_groups = group_by_priority(jobs)
    
    # Process groups by priority and create batches
    final_order = []
    total_time = 0
    
    # Process each priority level
    for priority in sorted(priority_groups.keys()):
        priority_jobs = priority_groups[priority]
        groups = find_print_groups(priority_jobs, printer_constraints)
        
        for group in groups:
            # Add all jobs from group to final order
            final_order.extend([job.id for job in group])
            # Add maximum print time of the group
            total_time += max(job.print_time for job in group)
    
    return {
        "print_order": final_order,
        "total_time": total_time
    }

def test_printing_optimization():
    # Test 1: Equal priority models
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Test 2: Different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    # Test 3: Volume constraints exceeded
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Test 1 (equal priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("\nTest 2 (different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("\nTest 3 (exceeding constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")

if __name__ == "__main__":
    test_printing_optimization()