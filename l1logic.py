def calpoints(option1,option2,res):
    if option1=="Excellent" and option2=="Excellent":
        if int(res) >= 90:
            return 100
        elif int(res) >= 80:
            return 90
        elif int(res) >= 70:
            return 80
        else:
            return 70
    elif option1=="Good"and option2=="Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option2=="Good"and option1=="Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option1=="Satisfactory"and option2=="Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option2=="Satisfactory"and option1=="Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1=="Good"and option2=="Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option2=="Good"and option1=="Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option1=="Good" and option2=="Good":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1=="Satisfactory" and option2=="Satisfactory":
        if int(res) >= 90:
            return 80
        elif int(res) >= 80:
            return 70
        elif int(res) >= 70:
            return 60
        else:
            return 50