
CREATE DATABASE ecommerce;
USE ecommerce;

SELECT * FROM sales;
-- 1. Total Orders
SELECT COUNT(*) AS Total_Orders
 FROM sales;
 
 -- 2. Total Sales
SELECT SUM(Net_Amount) AS Total_Sales
FROM sales;

-- 3.Top Products
SELECT Product,SUM(Net_Amount) AS Sales_Amount
FROM sales
GROUP BY Product
ORDER BY  Sales_Amount DESC;

-- 4. Top Cities
SELECT City,SUM(Net_Amount) AS Sales_Amount
FROM sales
GROUP BY City
ORDER BY  Sales_Amount DESC;

-- 5. Monthly Sales
SELECT Month,SUM(Net_Amount) AS Sales_Amount
FROM sales
GROUP BY Month;

-- 6. Highest Profit Products
SELECT Product,SUM(Profit) AS Profit
FROM sales
GROUP BY Product
ORDER BY  Profit DESC;

-- 7.Payment Mode
SELECT Payment_Mode,COUNT(*)
FROM sales
GROUP BY Payment_Mode;

-- 8.Canceled Orders
SELECT * FROM sales
WHERE Order_Status = "Cancelled";
