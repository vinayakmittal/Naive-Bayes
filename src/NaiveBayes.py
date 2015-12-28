import math
'''
NAME- VINAYAK MITTAL
SBU ID - 110385943
NET ID - VMITTAL    

NAME - ALPIT KUMAR GUPTA
SBU ID - 110451714
NET ID - ALGUPTA
'''
def findIntegerEquivalent(line):
    line = list(line)
    for j in range(0,len(line)):
        if line[j] == ' ':
            line[j] = 0
        elif line[j] == '#':
            line[j] = 1
        elif line[j] == '+':
            line[j] = 2
            
    return line
    
def parseTrainingImages(imageFile, labelFile, digitHeight):
    img_file = open(imageFile)
    lbl_file = open(labelFile)
    count = 0            
        
    training_set = {}
    temp = []
    
    line = img_file.readline()
    while line:
        count = count + 1                                                    
        line = line.strip('\n')    
        temp.append(findIntegerEquivalent(line))                         
                                                                                                     
        if count % digitHeight == 0:
            number =  int(lbl_file.readline().strip('\n'))
            
            if number not in training_set:
                training_set[number] = []
                
            training_set[number].append(temp)
            temp = []                                            
               
        line = img_file.readline()
         
    img_file.close()
    lbl_file.close()        

    return training_set, count/digitHeight

def parseTestingImages(test_imageFile, test_labelFile, digitHeight):    
    tst_file = open(test_imageFile)
    tst_label = open(test_labelFile)
    count = 0
    img_cnt = 1
    
    line = tst_file.readline()
    temp = []
    
    testing_set = {}
    testing_label = []    
        
    while line:
        count = count + 1
        line = line.strip('\n')
        temp.append(findIntegerEquivalent(line))                         
                                                                                                     
        if count % digitHeight == 0:
            number =  int(tst_label.readline().strip('\n'))
            testing_label.append(number)
            
            if img_cnt not in testing_set:
                testing_set[img_cnt] = []
                                                
            testing_set[img_cnt].append(temp)
            img_cnt = img_cnt + 1
            temp = []                                                                    
               
        line = tst_file.readline()                
    
    tst_file.close()
    tst_label.close()
    
    return testing_set, testing_label  
        
def findPriorProbability(trainingSet, count):    
    prior_prob = {}
    
    for key, value in trainingSet.items():
        if key not in prior_prob:
            prior_prob[key] = 0                
        prior_prob[key] = len(value)/float(count)
        
    return prior_prob

def findFeaturesCount(trainingSet):
    
    cond_prob = {}    
                
    for key, value in trainingSet.items():     
                             
        if key not in cond_prob:
            cond_prob[key] = {}
                    
        temp = {}
        temp[0] = [[0 for x in range(28)] for x in range(28)]
        temp[1] = [[0 for x in range(28)] for x in range(28)]
        temp[2] = [[0 for x in range(28)] for x in range(28)]
                   
        for img in value:                    
            for i in range(28):
                for j in range(28):
                    if img[i][j] == 0:
                        temp[0][i][j] = temp[0][i][j] + 1
                    elif img[i][j] == 1:
                        temp[1][i][j] = temp[1][i][j] + 1
                    elif img[i][j] == 2:
                        temp[2][i][j] = temp[2][i][j] + 1 
                
        cond_prob[key] = temp        
    

    
    return cond_prob    
        

def findPosteriorProbability(testSet, trainingSet, prior_prob, cond_prob):
        
    bayesLabel = []    
    
    for key, value in testSet.items():        
        pos = 0
        feature_count = {}
        img = value[0]
                                                   
        for i in range(0, 28):        
            for j in range(0, 28):                
                feature = img[i][j]
                                    
                for num in range(0,10):
                    ftr_cnt = cond_prob[num][feature][i][j]                                                        
                    ftr_cnt = (ftr_cnt +1)/(float)(len(trainingSet[num])+1)
                    
                    if pos not in feature_count:
                        feature_count[pos] = []
                                            
                    feature_count[pos].append(ftr_cnt)
                
                pos = pos + 1
    
        max_value = 0
        digit = 0        
        for num in range(10):
            prod = 1
            for i in range(len(feature_count)):                    
                prod = prod*feature_count[i][num]
                if prod == 0:
                    break                            
           
            prod = prod*(prior_prob[num] + 1)
                        
            if prod > max_value:
                max_value = prod
                digit = num
                
            prod = 1 
                                    
        bayesLabel.append(digit) 
            
    return bayesLabel       
    
def predictAccuracy(testLabel, bayesLabel):
    
    match = 0          
    
    test_hit_cnt = {}  
    test_dig_cnt = {}
    dig_stat = {}
            
    for i in range(len(testLabel)):
        number = bayesLabel[i]
        
        if number not in test_hit_cnt:
            test_hit_cnt[number] = 0
        
        if number not in test_dig_cnt:
            test_dig_cnt[number] = 0
        
        test_dig_cnt[number] = test_dig_cnt[number] + 1
        
        if testLabel[i] == bayesLabel[i]:
            match =  match + 1
            test_hit_cnt[number] = test_hit_cnt[number] + 1            
        
    for i in range(10):
        dig_stat[i] = (test_hit_cnt[i]/(float)(test_dig_cnt[i])) * 100.0 
        
    accuracy = (match/(float)(len(testLabel))) * 100.0
    
    return accuracy, dig_stat
        
if __name__ == '__main__':
    imageFile = "../dataset/trainingimages.txt"
    labelFile = "../dataset/traininglabels.txt"
    digitHeight = 28
    trainingSet, count = parseTrainingImages(imageFile,labelFile, digitHeight)
    prior_prob = findPriorProbability(trainingSet, count)
    cond_prob = findFeaturesCount(trainingSet)      
        
    test_imageFile = "../dataset/testimages.txt"
    test_labelFile = "../dataset/testlabels.txt"   
    
    testSet, testLabel = parseTestingImages(test_imageFile, test_labelFile, digitHeight)                
    
    bayesLabel = findPosteriorProbability(testSet, trainingSet, prior_prob, cond_prob)
        
    accuracy, dig_stat = predictAccuracy(testLabel, bayesLabel)
    
    print "Naive Bayesian Statistics \n"
    print "Digit\tAccuracy"
    for key, value in dig_stat.items():
        print key,"\t",value,"%"
    
    print "\nNaive Bayes Classifier Accuracy=> " ,accuracy, "%"
    
     
    