import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

def safe_pregrancy(x,c=25, sigma=10):
    #risk rate of pregrancy at age x
    #In this simulation, we assume gaussian distribution
    return (np.exp((-((x-c)/sigma)**2)/2)/(2*np.pi*sigma))

def fertility(x, b=3, c=25, c_fertilty=2):
    #fertility rate of pregrancy at age x
    #b is a fertility of woman with minimum age, a is gradient which depends on fertility of woman with maximal age c.
    return b-((b-c_fertilty)/c)*x

def expected_fertility(x, b=3, c=25, sigma=1, c_fertilty=2):
    return fertility(x)*safe_pregrancy(x)

def expected_fitness(i, stragey_list, percent_stragey_list, b=3, c=25, sigma=1, c_fertilty=2, p_i=1):
    #fitness of men whose stragey is i
    #stragey_list is a other's current stragey and its portion is in percent_stragey_list
    result=0 #return value

    for j in range(0,len(stragey_list),1):
        if (i<stragey_list[j]):
            result+=(expected_fertility(j, b, c, sigma, c_fertilty)*percent_stragey_list[stragey_list==i])
        elif(i==stragey_list[j]):
            result+=(expected_fertility(j, b, c, sigma, c_fertilty)*p_i*percent_stragey_list[j])
            
    return result

def average_fitness(stragey_list, percent_stragey, b=3, c=25, sigma=1, c_fertilty=2, p_i=1):
    #average fitness
    result=0

    for i in stragey_list:
        result+=expected_fitness(i, stragey_list, percent_stragey, b=3, c=25, sigma=1, c_fertilty=2, p_i=1)*percent_stragey[stragey_list==i]
    return result

def dynamics_rate_age(i, stragey_list, percent_stragey_list, b=3, c=25, sigma=1, c_fertilty=2, p_i=1, iteration=50000):
    #dynamics for stragey i
    result=np.zeros(iteration); result[0]=percent_stragey_list[stragey_list==i]

    for j in range(1,iteration,1):
        result[j]=result[j-1]+result[j-1]*((expected_fitness(i,stragey_list, percent_stragey_list))-average_fitness(stragey_list, percent_stragey_list))
        if(result[j]>=1):
            result[j]=1

    return result

def get_stability_point(i, stragey_list, percent_stragey_list, b=3, c=25, sigma=1, c_fertilty=2):
    #stability point of rate of stragey i
    
    #average fitness without considering stragy i
    average_fitness_without_i=average_fitness(stragey_list,percent_stragey_list)-(expected_fitness(i, stragey_list, percent_stragey_list)*percent_stragey_list[stragey_list==i])
    d=average_fitness_without_i/expected_fertility(i, b, c, sigma, c_fertilty)
    
    return min(1,1+((1-4*d)**0.5)/2)

#figure1
"""
age_list=np.linspace(11,25,100)
age_expected_fertility=expected_fertility(age_list, b=3, c=25, sigma=1, c_fertilty=2)

plt.plot(age_list, age_expected_fertility); plt.title("Age and expected fertility");
plt.xlabel("age"); plt.ylabel("expected fertility");
plt.plot(); plt.show()


#figure2
age_percentage=np.zeros(age_list.shape)+0.01
fitness_age_list=np.zeros(age_list.shape)
for i in range(0,len(age_list),1):
    fitness_age_list[i]=fitness(i,age_list,age_percentage)

plt.plot(age_list, fitness_age_list); plt.title("Age and fitness");
plt.xlabel("age"); plt.ylabel("fitness"); 
plt.plot(); plt.show()
"""


#figure3
#2 kinds of stragy competing each other, compare the variance of percentage
"""
age_stragy=np.array([11,25]);
number_data=70
age_percentage11=np.zeros(number_data)+0.1;
age_percentage25=np.zeros(number_data)+0.9
age_percentage_average=np.zeros(number_data); 

for i in range(1,len(age_percentage25),1):
    age_percentage11[i]+=(0.01*i)
    age_percentage25[i]-=(0.01*i)

fitness_age_list=np.zeros(age_stragy.shape)
fitness_age_list11=np.zeros(number_data)
fitness_age_list25=np.zeros(number_data)

#fitness
for i in range(0,len(fitness_age_list11),1):
    temp_stragy_rate=np.array([age_percentage11[i],age_percentage25[i]])t
    fitness_age_list11[i]=expected_fitness(age_stragy[0],age_stragy,temp_stragy_rate)
    fitness_age_list25[i]=expected_fitness(age_stragy[1],age_stragy,temp_stragy_rate)
    age_percentage_average[i]=average_fitness(age_stragy, temp_stragy_rate)

plt.scatter(age_percentage11, fitness_age_list11, label='Expected fitness of age 11'); plt.title("Age and fitness: 2 kinds of stragy");
plt.scatter(age_percentage11, fitness_age_list25, label='Expected fitness of age 25');
plt.scatter(age_percentage11, age_percentage_average, label='Average fitness');
plt.xlabel("rate of men whose stragy is 11"); plt.ylabel("fitness"); 
plt.legend(); plt.show()
"""

#figure4
#"""
stragey_list=np.array([11,25]);
percent_stragey_list=np.zeros(stragey_list.shape); percent_stragey_list[0]=0.3; percent_stragey_list[1]=0.7
iteration=500000;inital_rate25=percent_stragey_list[1]; inital_rate11=percent_stragey_list[0]

stability_point25=get_stability_point(stragey_list[1], stragey_list, percent_stragey_list) #stability point of stragey 25

stragy_dynamics25=dynamics_rate_age(stragey_list[1], stragey_list, percent_stragey_list, b=3, c=25, sigma=1, c_fertilty=2, p_i=1, iteration=iteration)

#stragy_dynamics11=dynamics_rate_age(stragey_list[0], stragey_list, percent_stragey_list, b=3, c=25, sigma=1, c_fertilty=2, p_i=1, iteration=iteration)

plt.scatter(range(len(stragy_dynamics25)),stragy_dynamics25, label='Dynamics of stragy 25'); plt.title("Dynamics of stragy: 2 kinds of stragy");
#plt.scatter(range(len(stragy_dynamics25)), stragy_dynamics11, label='Dynamics of stragy 11');
plt.xlabel("Time"); plt.ylabel("Rate of stragy"); 
plt.legend(); plt.show()

stragy_stability25=get_stability_point(stragey_list[1], stragey_list, percent_stragey_list, b=3, c=25, sigma=1, c_fertilty=2)
stragy_stability11=get_stability_point(stragey_list[0], stragey_list, percent_stragey_list, b=3, c=25, sigma=1, c_fertilty=2)
#"""

