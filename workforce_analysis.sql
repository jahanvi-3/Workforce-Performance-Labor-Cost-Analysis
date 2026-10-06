-- 1. View employee information
SELECT *
FROM employees;


-- 2. View employee performance data
SELECT *
FROM employee_performance;


-- 3. View labor cost data
SELECT *
FROM labor_cost;


-- 4. Employee-wise business performance and labor cost analysis
SELECT
    e.Employee_ID,
    e.Employee_Name,
    e.Department,

    SUM(p.Sales_Revenue) AS Total_Revenue,

    SUM(
        l.Base_Salary
        + l.Overtime_Cost
        + l.Training_Cost
    ) AS Total_Labor_Cost,

    AVG(p.Performance_Score) AS Avg_Performance,

    SUM(l.Overtime_Hours) AS Total_Overtime_Hours,

    CASE
        WHEN AVG(p.Performance_Score) < 60
             AND SUM(l.Overtime_Hours) > 200
             AND SUM(p.Sales_Revenue)
                 < SUM(
                     l.Base_Salary
                     + l.Overtime_Cost
                     + l.Training_Cost
                 )
        THEN 'Potential Cost Risk'

        ELSE 'Normal'
    END AS Cost_Risk

FROM employees e

JOIN employee_performance p
    ON e.Employee_ID = p.Employee_ID

JOIN labor_cost l
    ON e.Employee_ID = l.Employee_ID
    AND p.Month = l.Month

GROUP BY
    e.Employee_ID,
    e.Employee_Name,
    e.Department;


-- 5. Employees with potential cost risk
SELECT
    e.Employee_ID,
    e.Employee_Name,
    e.Department,
    AVG(p.Performance_Score) AS Avg_Performance,
    SUM(l.Overtime_Hours) AS Total_Overtime_Hours,
    SUM(p.Sales_Revenue) AS Total_Revenue,
    SUM(
        l.Base_Salary
        + l.Overtime_Cost
        + l.Training_Cost
    ) AS Total_Labor_Cost

FROM employees e

JOIN employee_performance p
    ON e.Employee_ID = p.Employee_ID

JOIN labor_cost l
    ON e.Employee_ID = l.Employee_ID
    AND p.Month = l.Month

GROUP BY
    e.Employee_ID,
    e.Employee_Name,
    e.Department

HAVING
    AVG(p.Performance_Score) < 60
    AND SUM(l.Overtime_Hours) > 200
    AND SUM(p.Sales_Revenue)
        < SUM(
            l.Base_Salary
            + l.Overtime_Cost
            + l.Training_Cost
        )

ORDER BY Avg_Performance ASC;


-- 6. Department-wise performance analysis
SELECT
    e.Department,
    COUNT(DISTINCT e.Employee_ID) AS Employee_Count,
    AVG(p.Performance_Score) AS Avg_Performance,
    SUM(p.Sales_Revenue) AS Total_Revenue,
    SUM(l.Overtime_Cost) AS Total_Overtime_Cost,
    SUM(l.Training_Cost) AS Total_Training_Cost

FROM employees e

JOIN employee_performance p
    ON e.Employee_ID = p.Employee_ID

JOIN labor_cost l
    ON e.Employee_ID = l.Employee_ID
    AND p.Month = l.Month

GROUP BY e.Department

ORDER BY Total_Revenue DESC;