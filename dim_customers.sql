-- This code first displays all data from the products table.
-- Then, it selects specific product details and uses CASE to
-- categorize products as Low, Medium, or High based on their price.
select * from 
dbo.products;

SELECT 
    ProductID,  
    ProductName,  
    Price,  

    CASE 
        WHEN Price < 50 THEN 'Low'  
        WHEN Price BETWEEN 50 AND 200 THEN 'Medium'  
        ELSE 'High'  
    END AS PriceCategory  

FROM 
    dbo.products;  =-
