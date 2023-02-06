show databases; ## use dataase
use harsh;    ##use database as harsh 
show tables; 

## look of dataset 
select * from covid;

--  cheaking missing values  from data 
select * from covid where 
Province is NULL
or Latitude is NULL
or Longitude is NULL
or Date is NULL
or Confirmed is NULL
or Deaths is NULL
or Recovered is NULL;


-- now we perform some basic statistic operation 
## cheaking firt 10 rows of data 
select  * from covid limit 10;

## cheaking how many rows 
select count(*) as "r_o_d" from covid;

SELECT
	MIN(Confirmed) AS min_confirmed, 
	MIN(Deaths) AS min_dealths, 
	MIN(Recovered) AS min_recovered
FROM covid;
SELECT 
	MAX(Confirmed) AS min_confirmed, 
	max(Deaths) AS min_dealths, 
	max(Recovered) AS min_recovered
FROM covid;

-- total no of conformed deah 
select 
sum(Confirmed) as confm,
sum(Deaths) as deth,
sum(Recovered) as rcr
from covid;

