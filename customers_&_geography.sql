-- This code displays all customers and products, then uses a LEFT JOIN
-- to add each customer's country and city from the geography table.

select * from 
dbo.customers;

select * from 
dbo.products;

SELECT 
    c.CustomerID,  
    c.CustomerName,  
    c.Email,  
    c.Gender,  
    c.Age,  
    g.Country,  
    g.City  
FROM 
    dbo.customers as c  
LEFT JOIN
    dbo.geography g  
ON 
    c.GeographyID = g.GeographyID;
