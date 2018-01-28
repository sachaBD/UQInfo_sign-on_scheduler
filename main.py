import datetime as datetime

from ScheduleSignOn.Schedule import ScheduleSignOn
from LoadCourses.Scraper import UQCourseScraper

# scraper = UQCourseScraper.deserialise("equine-2018")
# schedule = ScheduleSignOn(scraper.programs)
# schedule.schedule_signon(2018, 1, datetime.timedelta(minutes=10))
from UQCourses.Program import Program

# program = Program("https://my.uq.edu.au/programs-courses/program.html?acad_prog=2342")

programs = UQCourseScraper.create_all_programs("https://my.uq.edu.au/programs-courses/browse.html?level=ugpg", "2018-1")
print(programs)


# scraper = UQCourseScaper()
# scraper.programs["Bachelor of Engineering (Honours)"] = program
# scraper.serialise("engg-2018")
# course = Course("span1000", "spanish1", 2, "https://my.uq.edu.au/programs-courses/course.html?course_code=ECON1010")
# print(course)
exit()

scraper = UQCourseScraper("https://my.uq.edu.au/programs-courses/browse.html?level=ugpg")
scraper.find_all_courses()
scraper.serialise("UQ-course-2018-sem-1")

scraper = UQCourseScraper.deserialise("UQ-course-2018-sem-1")

programs = scraper.get_single_programs()
courses = list(scraper.get_all_course(programs[0]))

for course in courses:
    print(course, course.get_extended_info().keys())

# print(scraper.get_all_course(programs[0]))
# print(scraper.get_all_course("Agribusiness"))

for program in scraper.get_single_programs():
    print(program, len(scraper.get_all_course(program)))


temp = scraper.get_all_course("Advanced Business (Honours)")


