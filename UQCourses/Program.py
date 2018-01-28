from typing import List, Dict, Tuple

from UQCourses.Course import Course


class Program:

    def __init__(self, name: str, plans: Dict[str, List[Course]]):
        self.name = name
        self.plans = plans


    def get_plans(self):
        return self.plans


    def __repr__(self):
        return self.name + ", plans: " + str(self.plans.keys()) #" : " + str(self.plans)
