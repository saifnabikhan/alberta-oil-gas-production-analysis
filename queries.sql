SELECT 
  Region,
  SUBSTR(Production_Month, 1, 4) AS Year,
  ROUND(SUM(Oil_Volume_m3), 0) AS Annual_Oil_m3,
  ROUND(SUM(Gas_Volume_e3m3), 0) AS Annual_Gas_e3m3
FROM alberta_og_production
GROUP BY Region, Year
ORDER BY Region, Year;



SELECT 
  Facility_Type,
  ROUND(SUM(Oil_Volume_m3), 0) AS Total_Oil_m3,
  ROUND(SUM(Gas_Volume_e3m3), 0) AS Total_Gas_e3m3,
  ROUND(AVG(Uptime_Hours), 1) AS Avg_Uptime_Hours,
  SUM(Active_Well_Count) AS Total_Well_Months
FROM alberta_og_production
GROUP BY Facility_Type
ORDER BY Total_Oil_m3 DESC;




SELECT
  Region,
  ROUND(SUM(CASE WHEN SUBSTR(Production_Month,1,4) = '2020' 
    THEN Oil_Volume_m3 END), 0) AS Oil_2020,
  ROUND(SUM(CASE WHEN SUBSTR(Production_Month,1,4) = '2024' 
    THEN Oil_Volume_m3 END), 0) AS Oil_2024,
  ROUND(
    (SUM(CASE WHEN SUBSTR(Production_Month,1,4) = '2024' THEN Oil_Volume_m3 END) -
     SUM(CASE WHEN SUBSTR(Production_Month,1,4) = '2020' THEN Oil_Volume_m3 END)) /
     SUM(CASE WHEN SUBSTR(Production_Month,1,4) = '2020' THEN Oil_Volume_m3 END) * 100
  , 1) AS Oil_Decline_Pct
FROM alberta_og_production
GROUP BY Region
ORDER BY Oil_Decline_Pct ASC;




SELECT
  CAST(SUBSTR(Production_Month, 6, 2) AS INTEGER) AS Month_Num,
  CASE CAST(SUBSTR(Production_Month, 6, 2) AS INTEGER)
    WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
    WHEN 4 THEN 'April' WHEN 5 THEN 'May' WHEN 6 THEN 'June'
    WHEN 7 THEN 'July' WHEN 8 THEN 'August' WHEN 9 THEN 'September'
    WHEN 10 THEN 'October' WHEN 11 THEN 'November' WHEN 12 THEN 'December'
  END AS Month_Name,
  ROUND(AVG(Oil_Volume_m3), 0) AS Avg_Oil_m3,
  ROUND(AVG(Gas_Volume_e3m3), 0) AS Avg_Gas_e3m3
FROM alberta_og_production
GROUP BY Month_Num
ORDER BY Month_Num;





SELECT
  Operator,
  Region,
  ROUND(SUM(Oil_Volume_m3), 0) AS Total_Oil_m3,
  ROUND(SUM(Gas_Volume_e3m3), 0) AS Total_Gas_e3m3,
  ROUND(AVG(Uptime_Hours), 1) AS Avg_Uptime
FROM alberta_og_production
GROUP BY Operator, Region
ORDER BY Total_Oil_m3 DESC
LIMIT 10;





SELECT
  Region,
  ROUND(SUM(Oil_Volume_m3), 0) AS Total_Oil_m3,
  ROUND(SUM(Water_Volume_m3), 0) AS Total_Water_m3,
  ROUND(SUM(Water_Volume_m3) / SUM(Oil_Volume_m3), 2) AS Water_Oil_Ratio
FROM alberta_og_production
GROUP BY Region
ORDER BY Water_Oil_Ratio DESC;