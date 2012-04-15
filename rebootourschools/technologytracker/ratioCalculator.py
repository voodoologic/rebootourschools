
   
def computeDistrictRatios(schools, computers):
    
    studentsPerComputerRatioList = []
    teachersPerComputerRatioList = [] 
    computersPerSchoolCountList = []  
    for school in schools:
        computerCount = len([computer for computer in computers if computer.school == school])
        if computerCount > 0:
            ###computers per school count
            computersPerSchoolCountList.append((school, computerCount))
            
            ###students per computer ratio
            studentPerComputerRatio = float(school.student_count) / float(computerCount)
            studentsPerComputerRatioList.append((school, studentPerComputerRatio))
            
            ###teachers per computer ratio
            teachersPerComputerRatio = float(school.teacher_count) / float(computerCount)
            teachersPerComputerRatioList.append((school, teachersPerComputerRatio))
            
    ###sort all of the lists before returning them
    studentsPerComputerRatioList = sorted(studentsPerComputerRatioList, key=lambda ratio: ratio[1])[:5]
    computersPerSchoolCountList = sorted(computersPerSchoolCountList, key=lambda ratio: ratio[1])[:5]
    teachersPerComputerRatioList = sorted(teachersPerComputerRatioList, key=lambda ratio: ratio[1])[:5]
    
    return studentsPerComputerRatioList, teachersPerComputerRatioList, computersPerSchoolCountList           
             