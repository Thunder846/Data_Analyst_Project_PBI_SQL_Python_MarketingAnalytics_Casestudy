Select * from dbo.customer_reviews; 
-- This code selects review details from the customer_reviews table and uses REPLACE
-- to remove extra spaces from the ReviewText, making the text cleaner and more consistent.
SELECT 
    ReviewID,  
    CustomerID,  
    ProductID,  
    ReviewDate,  
    Rating,  
    
    REPLACE(ReviewText, '  ', ' ') AS ReviewText
FROM 
    dbo.customer_reviews;  
