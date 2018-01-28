import pickle
from abc import abstractmethod
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from UQCourses.Course import Course
from UQCourses.Program import Program
from UQCourses.Semester import Semester


class UQCourseScraper:

    """
    A factory class which scrapes UQ pages and produces classes.
    """
    def __init__(self, sourcePage: str=""):
        self.sourcePage = sourcePage
        self.programs = {}


    """
    Scrapes the given landing page which contains a list of programs and a link to the program page. Then creates and 
    returns a project name to Program object mapping.
    """
    @abstractmethod
    def create_all_programs(sourcePage: str, saveLocation: str=None) -> Dict[str, Program]:
        firstPage = requests.get(sourcePage)
        soupedPage = BeautifulSoup(firstPage.text, "lxml")

        baseSource = "/".join(firstPage.url.split("/")[:-2])

        programs = []
        for value in soupedPage.find_all("td", {"class": "title"}):
            # print(value.get('href'))
            if value.getText().strip() != "" and len(value.getText().strip()) != 1:
                links = value.find('a')
                if links is None:
                    continue

                programs.append((value.getText().strip(), links.attrs['href']))


        outputPrograms = {}
        for program, link in programs:
            print("Loading " + program)
            # outputPrograms[program] = Program(baseSource + link)
            outputPrograms[program] = UQCourseScraper.create_program(baseSource + link)
            print("Loaded " + str(len(outputPrograms[program].plans)) + " plans.")

            # Save this program
            UQCourseScraper.serialise(outputPrograms, saveLocation)


        return outputPrograms


    @abstractmethod
    def create_program(sourcePage: str) -> Program:        
        page = requests.get(sourcePage)
        soupedPage =  BeautifulSoup(page.text, "lxml")
        baseURL = "/".join(page.url.split("/")[:-2])

        # Find name
        name = "TODO: find name"

        courseList = UQCourseScraper.find_course_list(soupedPage)

        plans = UQCourseScraper.load_plans(baseURL + courseList, baseURL)

        return Program(name, plans)
    
    
    """
    Find the location of the course list for this course.
    """
    @abstractmethod
    def find_course_list(soupedPage: BeautifulSoup):
        courseList = []
        
        for link in soupedPage.find_all('a'):
            if link.text.strip() == "course list":
                courseList = link.attrs['href']
                break
                
        return courseList


    @abstractmethod
    def load_plans(courseListURL: str, baseURL: str) -> Dict[str, List[Course]]:
        page = requests.get(courseListURL)
        soupedCourseList = BeautifulSoup(page.text, "lxml")

        plans = {}

        # Find all planList
        # This is majors or Part A, Part B etc.
        oldStyle = False

        if soupedCourseList.find_all("h1", {"class": "trigger"}) == []:
            #TODO: Improve this condition
            plansLinks = soupedCourseList.find_all("div", {"class": "courselist"})
            oldStyle = True
        else:
            plansLinks = soupedCourseList.find_all("div", {"class": "planlist"})

        # Load each plan
        for plan in plansLinks:
            if oldStyle:
                if not plan.find("h2"):
                    name = "Compulsory"
                else:
                    name = plan.find("h2").text

            else:
                name = plan.find("h1", {"class": "trigger"})

                if name is None:
                    continue
                name = name.text

            plans.setdefault(name, [])# set())

            # find all courses in the plan
            for course in plan.find_all("tr"):
                buildCourse = []
                link = ""
                for info in course.find_all("td"):
                    buildCourse.append(info.text.strip())

                    for href in info.find_all('a'):
                        # print(href.prettify())
                        try:
                            if href.attrs['class'] == ['tooltip']:
                                # print("Found tooltip")
                                continue
                        except:
                            pass

                        link = href.attrs['href']

                    if link == "":
                        print("Not link for course" + str(buildCourse[0]))

                try:
                    print(buildCourse[0])

                    print(buildCourse)
                    plans[name].append(UQCourseScraper.load_course(baseURL + link, buildCourse[0], buildCourse[2], int(buildCourse[1])))

                    print("Plan extra info", plans[name][0].get_extended_info())

                    # plans[name].add(Course(buildCourse[0], buildCourse[2], int(buildCourse[1]), baseURL + link))
                except ValueError as e:
                    print("Skipping: " + str(buildCourse) + ", " + str(link))
                except IndexError as e:
                    print("Skipping: " + str(buildCourse) + ", " + str(link))


        # Testing
        testing = False
        if testing:
            for p in plans.keys():
                print(p, plans[p])

        return plans

    """
    """
    @abstractmethod
    def load_course(link: str, courseCode: str, courseName: str, units: int) -> Course:
        print("Source: ", link)
        page = requests.get(link)
        soupedPage = BeautifulSoup(page.text, "lxml")

        newCourse = Course(courseCode, courseName, units, UQCourseScraper.get_timetable_info(soupedPage) , link)
        newCourse.add_extended_info(UQCourseScraper.get_course_info(soupedPage))

        return newCourse



    """
    Finds extended infomation on the course from the given link
    """
    @abstractmethod
    def get_course_info(soupedPage: BeautifulSoup) -> Dict[str, str]:
        courseInfo = {}

        primaryContent = soupedPage.find("div", {"id": "content-primary"})
        # a = primaryContent.find_all("p")

        for info in primaryContent.find_all("p"):
            try:
                name = info.attrs['id']
                text = info.text
                courseInfo[name[name.index('course-') + len('course-'):]] = text.strip()
            except:
                pass

        return courseInfo


    @abstractmethod
    def get_timetable_info(page: BeautifulSoup) -> List[Semester]:
        offeredSemesters = []
        counter = 1
        while True:
            try:
                courseOffering = page.find('tr', {'id': ("course-offering-" + str(counter))})

                info = courseOffering.find('a', {'id': "course-offering-" + str(counter) + "-sem"}).text.strip()

                # TODO: Improve this
                # extract the semester and year
                # Eg: Semester 1, 2018
                info = info.split(",")
                info = [i.strip() for i in info]

                if "Summer" in info[0]:
                    offeredSemesters.append(Semester(int(info[1]), 3))
                else:
                    offeredSemesters.append(Semester(info[1], int(info[0].strip("Semester "))))

            except:
                break

            counter += 1

        return offeredSemesters


    """
    Given a webpage containing uq programs.

    """
    def find_all_courses(self):
        firstPage = requests.get(self.sourcePage)
        soupedPage = BeautifulSoup(firstPage.text, "lxml")

        baseSource = "/".join(firstPage.url.split("/")[:-2])

        # tables = soupedPage.find_all("table")

        programs = []
        for value in soupedPage.find_all("td", {"class": "title"}):
            # print(value.get('href'))
            if value.getText().strip() != "" and len(value.getText().strip()) != 1:
                links = value.find('a')
                if links is None:
                    continue

                programs.append((value.getText().strip(), links.attrs['href']))


        self.programs = {}
        for p in programs:
            print("Loading " + p[0])
            self.programs[p[0]] = Program(baseSource + p[1])
            print("Loaded " + str(len(self.programs[p[0]].plans)) + " plans.")



    """
    """
    def get_all_course(self, programName: str=None):
        output = set()

        if programName is None:
            for program in self.programs.keys():
                plans = self.programs[program].get_plans()
                for plan in plans.keys():
                    for course in plans[plan]:
                        output.add(course)
            return output
        else:
            plans = self.programs[programName].get_plans()

        for plan in plans.keys():
            for course in plans[plan]:
                output.add(course)

        return output


    def get_all_programs(self) -> List[str]:
        return list(self.programs.keys())


    def get_single_programs(self) -> List[str]:
        output = []
        for program in self.programs.keys():
            if "/" not in program:
                output.append(program)
        return output


    @abstractmethod
    def serialise(scraper: 'UQCourseScraper', outLocation: str):
        if outLocation is None:
            return

        outFile = open(outLocation, "wb")

        # Only save the programs
        pickle.dump(scraper.programs, outFile)

        outFile.close()

    @abstractmethod
    def deserialise(inLocation: str) -> 'Scraper':
        inFile = open(inLocation, "rb")

        output = UQCourseScraper()
        output.programs = pickle.load(inFile)

        # TODO: remove this
        for key in output.programs.keys():
            output.programs[key].name = "Remove this"

        inFile.close()

        return output


if __name__ == "__main__":
    scraper = UQCourseScraper("https://my.uq.edu.au/programs-courses/browse.html?level=ugpg")
    scraper.find_all_courses()
    a = scraper.get_all_course("Advanced Business (Honours)")

    for b in a:
        print(b.code)
