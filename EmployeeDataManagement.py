#!/usr/bin/env python
# coding: utf-8
### Employee Data Analysis
You have been provided with employee data from various departments of an organization. Your task is to analyze this data and answer the following questions:

1.What is the average salary in each department?
2.What is the attrition rate in each department?
3.Identify employees who joined the company before 2018 and have been rated with a performance rating of 5.
4.Identify the top 3 highest-paid employees in each department.
5.Find employees eligible for a special bonus based on:
Performance rating of 4 or 5.
Tenure of at least 36 years.
Age below 40.

Finally,the results will be stored in CSV file for future use.
# In[45]:


import os
import pandas as pd
def load_department_data(file_names):
    
    data = {}
    
    for file_name in file_names:
        
        if os.path.exists(file_name):
            
            department = os.path.basename(file_name).split('.')[0]
            
            data[department] = pd.read_csv(file_name)
        else:
            print(f"File {file_name} not found.Skipping......")
    
    return data

def calculate_average_salary(data):
    
    result ={}
    
    for dept,df in  data.items():
        
        if 'Salary' in df.columns:
            result[dept] = df['Salary'].mean()
        else:
            print(f"column 'Salary' not found in department {dept}.Skipping...........")
            
    return pd.DataFrame(result.items(),columns = ['Department','Average Salary'])
               

def calculate_attrition_rate(data):
    
    result ={}
    
    for dept,df in  data.items():
        
        if 'Attrition' in df.columns:
            attriction_count = df[df['Attrition'] == 'Yes'].shape[0]
            total_count  = df.shape[0]
            if total_count > 0:
                result[dept] = (attriction_count/total_count) * 100
            else:
                result[dept] == 0.0
        else:
            print(f"Column 'Attrition not found in department {dept}.Skipping...........")
        

    return pd.DataFrame(result.items(),columns = ['Department','Attrition rate(%)'])

def top_performers_before_2018(data):
    
    result ={}
    
    for dept,df in  data.items():
        
        if 'JoiningDate' in df.columns and 'PerformanceRating' in df.columns :
            
            df['JoiningDate'] = pd.to_datetime(df['JoiningDate'],dayfirst = True)
            
            filtered = df[(df['JoiningDate'].dt.year <2018) & (df['PerformanceRating'] == 5)]
            
            result[dept] = filtered[['EmployeeID','PerformanceRating','JoiningDate']]
        else:
            print(f"Column 'JoiningDate' and 'PerformanceRating' not found in department {dept}.Skipping...........")

            
    return result
                     
            
def top_3_highest_paid(data):
    
    result ={}
    
    for dept,df in  data.items():
        
        if 'Salary' in df.columns:  
            
            result[dept] = df.nlargest(3,'Salary','all')[['EmployeeID','Salary']]
            
        else:
            
            print(f"column 'Salary' not found in department {dept}.Skipping...........")
    return result
            
            
def eligible_for_bonus(data):

    result ={}
    
    for dept,df in data.items():
        
        if {'PerformanceRating','Age','Tenure'}.issubset(df.columns):
            
            filterted = df[(df['PerformanceRating'] >=4) & (df['Age'] <40) & (df['Tenure'] >=36)]
            
            result[dept] = filterted[['EmployeeID','PerformanceRating','Age','Tenure']]
            
        else:
            
            print(f"Required columns for bones eligilibility not found in department {dept}.Skipping......")
        
    return result
            

def save_to_excel(avg_salary,attrition,top_performers,top_paid,bonus_eligible,output_file = "result.xlsx"):
    
    with pd.ExcelWriter(output_file) as writer:
        
        avg_salary.to_excel(writer,sheet_name = "Average Salary",index=False)
        
        attrition.to_excel(writer,sheet_name = "Attrition Rate ",index=False)
        
        for dept,df in top_performers.items():
            if not df.empty:
                df.to_excel(writer,sheet_name = f"Top performers {dept}",index=False)
                
        for dept,df in top_paid.items():
            if not df.empty:
                df.to_excel(writer,sheet_name = f"Top paid {dept}",index=False)
                
        for dept,df in bonus_eligible.items():
            if not df.empty:
                df.to_excel(writer,sheet_name = f"Bonus employee{dept}",index=False)
        
                
        
    
        


# In[46]:


def main():
    
    file_names = input("Enter CSV file names (comma-separated):").split(',')
    
    data = load_department_data(file_names)   
    
    avg_salary = calculate_average_salary(data)
        
    attrition = calculate_attrition_rate(data)
    
    top_performers = top_performers_before_2018(data)
    
    top_paid = top_3_highest_paid(data)
    
    bonus_eligible = eligible_for_bonus(data)
    
  
    print("\n Saving results to result.xlsx........")
    
    save_to_excel(avg_salary,attrition,top_performers,top_paid,bonus_eligible)
    
    print("Result saved successfully!")
    
    
    
    


# In[47]:


main()

