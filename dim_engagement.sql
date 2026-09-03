-- This query cleans and transforms the engagement_data table.
-- It selects the required engagement, content, campaign, and product details.
-- standardizes ContentType values, separates combined Views and Clicks.
-- formats the EngagementDate, and excludes Newsletter content.
select * from
dbo.engagement_data

SELECT 
    EngagementID,  
    ContentID,  
	CampaignID,  
    ProductID,  

    UPPER(REPLACE(ContentType, 'Socialmedia', 'Social Media')) AS ContentType,  
    Upper(Replace(ContentType, 'blog', 'Blog')) As contentType,
    LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views,  
    RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) AS Clicks,  
    Likes,  
    
    FORMAT(CONVERT(DATE, EngagementDate), 'dd.MM.yyyy') AS EngagementDate  
FROM 
    dbo.engagement_data  
WHERE 
    ContentType != 'Newsletter';
