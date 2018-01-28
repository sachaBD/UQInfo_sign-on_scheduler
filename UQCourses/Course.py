import pickle
from abc import abstractmethod
from typing import Dict, List, Tuple

from UQCourses.Semester import Semester


class Course:

    def __init__(self, code: str, name: str, units: int, offered: List[Semester], link: str=""):
        self.code = code.strip().strip("\r\n").strip("[").strip("]")
        # TODO: Remove this
        # Currently handles [ code1000   or    code1001 ] such as for thesis subjects
        if len(self.code) != 8:
            self.code = self.code[-8:]

        self.name = name
        self.link = link
        self.units = units
        self.offered = offered

        self.extendedInfo = {}


    def add_extended_info(self, extendedInfo: Dict[str, str]) -> None:
        for key, value in extendedInfo.items():
            self.extendedInfo[key] = value


    def offered_in(self, year: int, semester: int) -> bool:
        return Semester(year, semester) in self.offered


    def get_extended_info(self) -> Dict[str, str]:
        return self.extendedInfo

    def get_info(self, key: str):
        try:
            return self.extendedInfo[key]
        except KeyError as e:
            return None


    def serialise(self, outLocation: str) -> None:
        fileOut = open(outLocation, "wb")

        pickle.dump(self, fileOut)

        fileOut.close()


    @abstractmethod
    def deserialise(self, inLocation: str) -> None:
        fileIn = open(inLocation, "rb")

        output = pickle.load(fileIn)

        fileIn.close()

        return output


    def __lt__(self, other):
        if isinstance(other, Course):
            return self.code == other.code

        return False


    def __repr__(self):
        return str(self.code) + ": units: " + str(self.units) + " : " + str(self.name)
