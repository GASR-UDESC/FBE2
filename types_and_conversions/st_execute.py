
def run_st(fb, alg):
    algorithm = fb.algorithm[alg]
    for condition in algorithm:
        condition_stmnt = condition.split(" := ")
        if condition_stmnt[1] == "FALSE" or condition_stmnt[1] == "True":
            getattr(fb, condition_stmnt[0]).value = False
            print("False conditional")	
        elif condition_stmnt[1] == "TRUE" or condition_stmnt[1] == "True":
            getattr(fb, condition_stmnt[0]).value = True
            print("True conditional")
        else:
            try:
                getattr(fb, condition_stmnt[0]).value == float(condition_stmnt[1])
                print("equals a float")
                print(getattr(fb, condition_stmn[0]).value)
            except:
                try:
                    getattr(fb, condition_stmnt[0]).value == getattr(fb, condition_stmnt[1]).value
                except:
                    statement = condition_stmnt[1].split()

                if '>' in statement:
                    statement.remove(">")
                    try:
                        value_1 = int(statement[0])
                        getattr(fb, condition_stmnt[0]).value = (value_1 > getattr(fb, statement[1]).value)
                    except:
                        try:
                            value_2 = int(statement[1])
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value > value_2)
                        except:
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value > getattr(fb, statement[1]).value)
                
                elif '<' in statement:
                    statement.remove("<")
                    try:
                        value_1 = int(statement[0])
                        getattr(fb, condition_stmnt[0]).value = (value_1 < getattr(fb, statement[1]).value)
                    except:
                        try:
                            value_2 = int(statement[1])
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value < value_2)
                        except:
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value < getattr(fb, statement[1]).value)
                
                elif '>=' in statement:
                   statement.remove(">=")
                   try:
                       value_1 = int(statement[0])
                       getattr(fb, condition_stmnt[0]).value = (value_1 >= getattr(fb, statement[1]).value)
                   except:
                       try:
                           value_2 = int(statement[1])
                           getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value >= value_2)
                       except:
                           getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value >= getattr(fb, statement[1]).value)
                
                elif '<=' in statement:	
                   statement.remove("<=")
                   try:
                       value_1 = int(statement[0])
                       getattr(fb, condition_stmnt[0]).value = (value_1 <= getattr(fb, statement[1]).value)
                   except:
                       try:
                           value_2 = int(statement[1])
                           getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value <= value_2)
                       except:
                           getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value <= getattr(fb, statement[1]).value)
                
                elif '==' in statement:
                    statement.remove("==")
                    try:
                        value_1 = int(statement[0])
                        getattr(fb, condition_stmnt[0]).value = (value_1 == getattr(fb, statement[1]).value)
                    except:
                        try:
                            value_2 = int(statement[1])
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value == value_2)
                        except:
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value == getattr(fb, statement[1]).value)
                
                elif '!=' in statement:
                    statement.remove("!=")
                    try:
                        value_1 = int(statement[0])
                        getattr(fb, condition_stmnt[0]).value = (value_1 != getattr(fb, statement[1]).value)
                    except:
                        try:
                            value_2 = int(statement[1])
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value != value_2)
                        except:
                            getattr(fb, condition_stmnt[0]).value = (getattr(fb, statement[0]).value != getattr(fb, statement[1]).value)
                
                else:
                    getattr(fb, condition_stmnt[0]).value = arithmetic(fb,statement)



def arithmetic(fb,test):							
    # ~ test = "5 + 3 * 3 / 4 - 3"
    if type(test) != list:
        test_split = test.split()
    else:
        test_split = test
    while(1):
		
        if '(' in test_split:
            i_1 = test_split.index('(')
            i_2 = test_split.index(')')
            new_val = arithmetic(test_split[i_1+1: i_2])
            del test_split[i_1:i_2+1]
            test_split.insert(i_1, new_val)
            print(test_split)
        elif '*' in test_split:
            i = test_split.index("*")
            try:
                new_val = float(test_split[i-1]) * float(test_split[i+1])
            except:
                try:
                    new_val = float(test_split[i-1]) * getattr(fb, test_split[i+1]).value
                except:
                    try:
                        new_val = getattr(fb, test_split[i-1]).value * float(test_split[i+1])
                    except:
                        new_val = getattr(fb, test_split[i-1]).value * getattr(fb, test_split[i+1]).value

            del test_split[i-1:i+2]
            test_split.insert(i-1, new_val)
            print(test_split)
        elif '/' in test_split:
            i = test_split.index("/")
            try:
                new_val = float(test_split[i-1]) / float(test_split[i+1])
            except:
                try:
                    new_val = float(test_split[i-1]) / getattr(fb, test_split[i+1]).value
                except:
                    try:
                        new_val = getattr(fb, test_split[i-1]).value / float(test_split[i+1])
                    except:
                        new_val = getattr(fb, test_split[i-1]).value / getattr(fb, test_split[i+1]).value
            
            del test_split[i-1:i+2]
            test_split.insert(i-1, new_val)
            print(test_split)
        elif '+' in test_split:
            i = test_split.index("+")
            try:
                new_val = float(test_split[i-1]) + float(test_split[i+1])
            except:
                try:
                    new_val = float(test_split[i-1]) + getattr(fb, test_split[i+1]).value
                except:
                    try:
                        new_val = getattr(fb, test_split[i-1]).value + float(test_split[i+1])
                    except:
                        print(test_split[i-1], test_split[i+1])
                        new_val = getattr(fb, test_split[i-1]).value + getattr(fb, test_split[i+1]).value
            del test_split[i-1:i+2]
            test_split.insert(i-1, new_val)
            print(test_split)
        elif '-' in test_split:
            i = test_split.index("-")
            try:
                new_val = float(test_split[i-1]) - float(test_split[i+1])
            except:
                try:
                    new_val = float(test_split[i-1]) - getattr(fb, test_split[i+1]).value
                except:
                    try:
                        new_val = getattr(fb, test_split[i-1]).value - float(test_split[i+1])
                    except:
                        new_val = getattr(fb, test_split[i-1]).value - getattr(fb, test_split[i+1]).value
            del test_split[i-1:i+2]
            test_split.insert(i-1, new_val)
            print(test_split)
        else:
            return test_split[0]



# ~ test = '5 + 3 * ( 2 + 3 ) / 3 - 1'	
# ~ print(arithmetic(test))



