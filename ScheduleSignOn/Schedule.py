import datetime
import random as random
from typing import Dict

import numpy as np

from UQCourses.Program import Program


# Create a sign-on schedule in which no courses within the same major overlap

class ScheduleSignOn:

    def __init__(self, programs: Dict[str, Program]):
        self.programs = programs
        self.timeTable = NotImplemented

    """
    Create a schedule for signons to minimise overlap of courses within the same degree.
    Constraints:
        - Signon between 9am - 5pm, Mon - Fri in a single week
        
    """
    def schedule_signon(self, year, semester: int, minimumPeriod: datetime.timedelta) -> Dict[datetime.datetime, str]:
        # get all available courses and store them as:
        # Dict {courseCode : [Programs] }

        # TODO: Add support for majors?
        availableCourses = {}
        for programName, program in self.programs.items():
            for plan, courses in program.get_plans().items():
                for course in courses:
                    if course.offered_in(year, semester):
                        availableCourses.setdefault(course, [])
                        availableCourses[course].append(program)

        print("Avail courses", availableCourses)

        # Create the self.timeTable
        self.timeTable = {}

        # Load the self.timeTable with available times
        times = [datetime.time(hour=9 + int(x) // 60, minute= int(x) % 60) for x in np.arange(0, 8 * 60,  minimumPeriod / datetime.timedelta(hours=1) * 60)]

        for day in range(0, 5):
            for time in times:
                self.timeTable.setdefault((day, time), ([], []))


        # Go through each program and assign the course into the next free slot that doesn't hold another course from
        # that program.
        # Ensure that the course is only in once and account for duel degrees
        for course, coursePrograms in availableCourses.items():
            checked = np.zeros(len(times) * 5)

            while 0 in checked:
                randNum = int(random.random() * len(times) * 5)
                day = randNum // len(times)
                time = times[randNum % len(times)]

                skip = False
                programs = self.timeTable[(day, time)][1]

                for program in programs:
                    # print(program, coursePrograms)
                    if program in coursePrograms:
                        skip = True
                        break

                if skip == False:
                    self.timeTable[(day, time)][0].append(course)

                    self.timeTable[(day, time)][1].extend((course for course in coursePrograms))
                    break

                checked[randNum] = 1

            # Check if the self.timeTable is full
            if 0 not in checked:
                self.handle_full_timeTable(self.timeTable)


        for key, value in self.timeTable.items():
            print(key, value)



    def handle_full_timeTable(self, timeTable, *args, **kwargs):
        print(timeTable)
        raise ValueError("Full timetable.")
