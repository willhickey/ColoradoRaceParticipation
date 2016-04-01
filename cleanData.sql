select category, count(*)
from eventcategory
where category like '%SW%' and standardcategoryid is null
group by category
having count(*) > 10
order by category

update eventcategory
set standardcategoryid = 5
where category = 'SW 3-4'

select count(*)
from eventcategory
where standardcategoryid is not null