-- NOTE: Identify duplicate customer journey records using ROW_NUMBER().
-- PARTITION BY groups records with the same customer, product, date, stage, and action.
-- ORDER BY JourneyID assigns a unique row number to each record within the group.

select * from
dbo.customer_journey;



WITH DuplicateRecords AS (
    SELECT 
        JourneyID,  
        CustomerID, 
        ProductID,  
        VisitDate,  
        Stage,  
        Action,  
        Duration,  
        
        ROW_NUMBER() OVER (
            
            PARTITION BY CustomerID, ProductID, VisitDate, Stage, Action  
            
            ORDER BY JourneyID  
        ) AS row_num  
    FROM 
        dbo.customer_journey  
)

SELECT *
FROM DuplicateRecords
ORDER BY JourneyID
-- WHERE row_num > 1  -- Filters out the first occurrence (row_num = 1) and only shows the duplicates (row_num > 1)
