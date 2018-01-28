from random import random
import numpy as np
import datetime as datetime

from ScheduleSignOn.Schedule import ScheduleSignOn
from UQCourses.Course import Course
from UQCourses.Program import Program
from UQCourses.Semester import Semester


def gen_program(progName, numPlans, numCourse):
    plans = {}

    for i in range(numPlans):
        planName = progName + str(i)

        courses = []
        for i in range(numCourse):
            courseCode = ""

            for i in range(4):
                courseCode += chr(65 + int(random() * 26))

            for i in range(4):
                courseCode += str(1 + int(random() * 8))

            print(courseCode)

            courseName = ""

            for i in range(10):
                courseName += chr(65 + int(random() * 26) + 26)

            units = 2

            offered = []

            for i in range(1 + int(abs(np.random.normal()) * 2)):
                # offered.append(Semester(2018, int(random() * 2)))
                offered.append(Semester(2018, 1))

            courses.append(Course(courseCode, courseName, units, offered))

        plans[planName] = courses

    return plans



if __name__ == "__main__":
    programs = {}

    programs['Program1'] = Program("Sci", gen_program('sci', 2, 20))
    programs['Program2'] = Program("Engg", gen_program('engg', 2, 20))

    for name, program in programs.items():
        print("Program:", name)
        for planName, plan in program.get_plans().items():
            print("Plan:", planName, plan)

    scheduler = ScheduleSignOn(programs)
    scheduler = scheduler.schedule_signon(2018, 1, datetime.timedelta(hours=1))
