import pandas as pd
def integrate_glassdoor():
    #loading the glassdoor main table salary and reviews table in a pandas dataframe
    #NOTE: the glassdoor dataset is under the directory glassdoor_data
    glassdoor=pd.read_csv('glassdoor_data/glassdoor.csv')
    glassdoor_reviews=pd.read_csv('glassdoor_data/glassdoor_reviews.csv')
    salary=pd.read_csv('glassdoor_data/glassdoor_salary_salaries.csv')

    #storing the features of the glassdoor dataset
    gs_columns=glassdoor.columns.values.tolist()
    rv_columns=glassdoor_reviews.columns.values.tolist()
    salary_columns=salary.columns.values.tolist()

    #the list of columns to be taken from the master glassdoor dataset
    glassdoor=glassdoor.loc[:,['gaTrackerData.empId',
                             'gaTrackerData.empName',
                             'gaTrackerData.empSize',
                             'gaTrackerData.industry',
                             'header.locId',
                             'header.location',
                             'header.payHigh',
                             'reviews',
                             'header.payLow',
                             'header.payMed',
                             'header.payPeriod',
                             'header.salaryHigh',
                             'header.salaryLow',
                             'header.salarySource',
                             'job.description',
                             'salary.country.currency.currencyCode',
                             'salary.country.currency.id',
                             'salary.country.currency.name',
                                'salary.salaries',
                            ]]

     #list of columns to be taken from the glassdoor review dataset
     glassdoor_reviews=glassdoor_reviews.loc[:,['id',
     'index',
     'reviews.val.cons',
     'reviews.val.pros',
     'reviews.val.reviewRatings.careerOpportunities',
     'reviews.val.reviewRatings.compBenefits',
     'reviews.val.reviewRatings.overall',
     'reviews.val.reviewRatings.worklifeBalance',
     'reviews.val.title',
    ]]

    #joining the glassdoor main table with reviews based on the reviews and id column

    glassdoor_join_reviews=glassdoor.merge(glassdoor_reviews,left_on='reviews',right_on='id')

    #joining the above table with the salary table to get the salary insights
    glassdoor_temp=glassdoor_join_reviews.merge(salary,left_on='salary.salaries',right_on='id')

    glassdoor_temp.to_csv('glassdoor_final.csv')
    
if __name__ == '__main__':
    integrate_glassdoor()