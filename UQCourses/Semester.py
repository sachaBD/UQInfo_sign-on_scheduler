
class Semester:

    """
    Represents a semester in which the university offers a course

    semester = 1    -> First semester
    semester = 2    -> Second semester
    semester = 3    -> Summer semester
    semester > 3    -> Other (eg. trimesters etc.)
    """
    def __init__(self, year: int, semester: int):
        self.year = year
        self.semester = semester


    def __lt__(self, other):
        if isinstance(other, Semester):
            if self.year == other.year:
                return self.semester < other.semester

            return self.year < other.year
        else:
            raise TypeError("Cannot compare Semester to a non Semester type.")


    def __le__(self, other):
        if isinstance(other, Semester):
            if self == other:
                return True

            if self.year == other.year:
                return self.semester < other.semester

            return self.year < other.year

        raise TypeError("Cannot compare Semester to a non Semester type.")


    def __eq__(self, other):
        if isinstance(other, Semester):
            return self.year == other.year and self.semester == other.semester

        return False


    def __repr__(self):
        return str(self.year) + " Sem: " + str(self.semester)


if __name__ == "__main__":
    s1 = Semester(2018, 1)
    s2 = Semester(2018, 2)
    s3 = Semester(2017, 1)
    s12 = Semester(2018, 1)

    assert (s1 == s1) == True
    assert (s1 == s12) == True

    assert (s1 < s2) == True
    assert (s1 <= s2) == True
    assert (s1 > s2) == False
    assert (s1 >= s2) == False

    assert (s1 > s12) == False
    assert (s1 < s12) == False
    assert (s1 >= s12) == True
    assert (s1 <= s12) == True

    print("Passed all tests successfully.")


