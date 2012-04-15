from GChartWrapper import *
   
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
    
    
    
def computeSchoolRatios(scomputers):
    return 1
    
    

def generateOsPieChart(osxCount, linuxCount, windowsCount):       
        
    osDataset = []
    osDataLabels = []
    if osxCount > 0:
        osDataset.append(osxCount)
        osDataLabels.append("OS X")
    if linuxCount > 0:
        osDataset.append(linuxCount)
        osDataLabels.append("LINUX")
    
    if windowsCount > 0:
        osDataset.append(windowsCount)
        osDataLabels.append("WINDOWS")               
    
    osChart = Pie3D( osDataset )
    osChart.label("OS X", "LINUX", "WINDOWS")
    osChart.color('4d89f9','c6d9fd')
    osChart.size(300,100)
        
    return osChart    
                   
             