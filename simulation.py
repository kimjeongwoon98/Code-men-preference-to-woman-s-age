import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy.stats import norm
from scipy.integrate import odeint

def safe_pregrancy(x,c=25, sigma=10):
    #risk rate of pregrancy at age x
    #In this simulation, we assume gaussian distribution
    return (np.exp((-((x-c)/sigma)**2)/2)/(sigma))

def fertility(x, b=3, c=25, c_fertilty=2):
    #fertility rate of pregrancy at age x
    #b is a fertility of woman with minimum age, a is gradient which depends on fertility of woman with maximal age c.
    return b-((b-c_fertilty)/c)*x

def expected_fertility(x, b=3, c=25, sigma=1, c_fertilty=2, minimum=11, maximum=25):
    #This is fertility of woman which contains risk of pregrancy and fertility(gene benefits).
    B=norm.cdf(minimum, loc=c, scale=sigma) #maximum age to get pregrant
    A=norm.cdf(maximum, loc=c, scale=sigma) #minimum age to get pregrant
    
    return fertility(x,b,c,c_fertilty)*(safe_pregrancy(x,c,sigma)/abs(B-A))

def expected_fitness(i, strategy_list, percent_strategy_list, b=3, c=25, sigma=1, c_fertilty=2, p_i=1):
    #fitness of men whose strategy is i
    #strategy_list is a other's current strategy and its portion is in percent_strategy_list
    result=0 #return value

    for j in range(0,len(strategy_list),1):
        if (i<strategy_list[j]):
            result+=(expected_fertility(i, b, c, sigma, c_fertilty)*percent_strategy_list[strategy_list==i])
        elif(i==strategy_list[j]):
            result+=(expected_fertility(i, b, c, sigma, c_fertilty)*p_i*percent_strategy_list[j])
            
    return result

def average_fitness(strategy_list, percent_strategy, b=3, c=25, sigma=1, c_fertilty=2, p_i=1):
    #average fitness of men
    result=0

    for i in strategy_list:
        result+=expected_fitness(i, strategy_list, percent_strategy, b, c, sigma, c_fertilty, p_i)*percent_strategy[strategy_list==i]
    return result

def dynamics_rate_age(i, strategy_list, percent_strategy_list, b=3, c=25, sigma=1, c_fertilty=2, p_i=1, iteration=5000):
    #dynamics for strategy i
    result=np.zeros(iteration); result[0]=percent_strategy_list[strategy_list==i]
    percent_dynamics=deepcopy(percent_strategy_list) #calculate fitness for changed percentage. In this case, I only consider two strategies.
    time_step=0.1

    expected_fertility_i=expected_fertility(i, b, c, sigma, c_fertilty, strategy_list[0], strategy_list[-1])
    for j in range(1,iteration,1):
        #result[j]=result[j-1]*(1+time_step*((expected_fitness(i,strategy_list, percent_dynamics,b,c,sigma,c_fertilty,p_i))-average_fitness(strategy_list, percent_dynamics,b,c,sigma,c_fertilty,p_i)))
        result[j]=result[j-1]+result[j-1]*time_step*(p_i*expected_fertility_i*result[j-1]*(1-result[j-1])
                                            -(average_fitness(strategy_list, percent_dynamics,b,c,sigma,c_fertilty,p_i)-expected_fitness(i,strategy_list, percent_dynamics,b,c,sigma,c_fertilty,p_i)))
        percent_dynamics[strategy_list==i]=result[j];
        percent_dynamics[(percent_dynamics!=0)*(strategy_list!=i)]=1-result[j]
        
    if(result[j]>=1):
            result[j]=1

    return result

#figure1
#"""
#p_i is a measure for how men can access to women in age i, which is same as p_c if i=c
b=3; c=25; sigma=3; c_fertilty=2; p_i=1; minimum=20; maximum=25

age_list=np.linspace(20,25,100)
age_expected_fertility=expected_fertility(age_list, b, c, sigma, c_fertilty)

plt.plot(age_list, age_expected_fertility); plt.title("Age and expected fertility", fontsize=20);
plt.xlabel("age", fontsize=20); plt.ylabel("expected fertility", fontsize=20);
plt.plot(); plt.show()

#figure2
age_percentage=np.zeros(age_list.shape)+(1/age_list.shape[0])
fitness_age_list=np.zeros(age_list.shape)
for i in range(0,len(age_list),1):
    fitness_age_list[i]=expected_fitness(age_list[i],age_list,age_percentage,b,c,sigma,c_fertilty,p_i)

plt.plot(age_list, fitness_age_list); plt.title("Age and fitness when multiple strategy existed with equal rate", fontsize=20);
plt.xlabel("age", fontsize=20); plt.ylabel("fitness", fontsize=20); 
plt.plot(); plt.show()
#"""

#figure3
#Only two competes each other and compare their fitness while changing inital rate of strategies.

age_strategy=np.linspace(20,25,10);
number_data=100;
age_percentage20=np.zeros(number_data);
age_percentage25=np.zeros(number_data)+1;
age_percentage_average=np.zeros(number_data);

for i in range(1,len(age_percentage25),1):
    age_percentage20[i]+=(i/number_data)
    age_percentage25[i]-=(i/number_data)

fitness_age_list=np.zeros(age_strategy.shape)
fitness_age_list20=np.zeros(number_data)
fitness_age_list25=np.zeros(number_data)

#fitness
for i in range(0,len(fitness_age_list20),1):
    temp_percentage=np.zeros(age_strategy.shape)
    temp_percentage[0]=age_percentage20[i]
    temp_percentage[-1]=age_percentage25[i]
    
    fitness_age_list20[i]=expected_fitness(age_strategy[0],age_strategy,temp_percentage,b,c,sigma,c_fertilty,p_i)
    fitness_age_list25[i]=expected_fitness(age_strategy[-1],age_strategy,temp_percentage,b,c,sigma,c_fertilty,p_i)
    age_percentage_average[i]=average_fitness(age_strategy, temp_percentage,b,c,sigma,c_fertilty,p_i)

plt.scatter(age_percentage20, fitness_age_list20, label='Expected fitness of age 20'); 
plt.scatter(age_percentage20, fitness_age_list25, label='Expected fitness of age 25');
plt.title("Age and fitness: two kinds of strategy", fontsize=25);
plt.scatter(age_percentage20, age_percentage_average, label='Average fitness');
plt.xlabel("rate of men whose strategy is 20", fontsize=25); plt.ylabel("fitness", fontsize=25); 
plt.legend(); plt.show()

#figure4
#"""
#Various types of strategies competes each other and see the dynamics of strategies ratio.

#strategy_list=np.array([14,20]); #only two strategies are considered.
#strategy_dynamics20=dynamics_rate_age(strategy_list[1], strategy_list, percent_strategy_list, b, c, sigma, c_fertilty, p_i, iteration);

#Although only two strategies are considered,it is for generalization of multiple strategies in future research. 
strategy_list=np.linspace(20,25,10); #range of strategies to mate
time=np.linspace(0,100,10000); #time step
percent_strategy_list=np.zeros(strategy_list.shape);
percent_strategy_list[-4]=0.3; percent_strategy_list[-1]=0.7 #initial value for each strategies.
inital_i= percent_strategy_list[-1]
iteration=2000;

#calculating dynamic for rate of preferece for c=25
#Although 25 is not optimal to maximize fitness, the result for it can be used at other age if its fitness is bigger than average.
strategy_dynamics25=dynamics_rate_age(strategy_list[-1], strategy_list, percent_strategy_list, b, c, sigma, c_fertilty, p_i, iteration);

plt.scatter(range(len(strategy_dynamics25)),strategy_dynamics25, label='Dynamics of strategy '+str(strategy_list[-1]));

plt.title("Dynamics of strategy", fontsize=25);
plt.xlabel("Time", fontsize=25); plt.ylabel("Rate of strategy "+str(strategy_list[-1]), fontsize=25); 
plt.legend(); plt.show();
