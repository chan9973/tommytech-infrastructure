```dataview
TABLE 
contact as "Contact",
role as "Role",
location as "Location",
email as "Email",
outreach_date as "Outreach Date",
template as "Template",
status as "Status",
response as "Response",
next_action as "Next Action"
FROM "TommyTech"
WHERE contains(file.name, "client_pipeline") = false
FLATTEN link(file.name) as linked_pages
WHERE linked_pages = file.name
SORT outreach_date DESC
```