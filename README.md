# rankingETL -> send tabuler data, rank, & load in target system 
<!--ts-->
   * [Objective](#Objective)
   * [Installation](#Installation)
     * [Run](#Run)
     * [Optional](#Optional)
   * [Process](#Process)
     * [Transform](#Transform)
     * [New_Sprints](#New_Sprints)
     * [Reporting](#Reporting)
<!--te-->

# Objective
The goal of this project is to automate daily loading & tracking of call campaigns. 

# Installation


## Run


## Optional - highly recommended:

# Process:
## Transform:
00. Create/track a 10-day sprint schedule
01. Load raw zip file
02. Load addition inventory from server
03. Clean & standardize data
04. Separate inventory into skills aka teams of employees
05. Test inventory is complete and up to date
------
06. Daily mapping on sprint schedule
07. New Inventory load balance across remaining sprint
08. Last call inventory search on the database
09. Identify rolled inventory from previous days sprint
10. Map priority based on steps 6-9
11. Split inventory by skill, group by contact id (phone#s), and score (rank order to called)
12. Append new inventory to master sprint schedule
------
13. Pivot table progress tracker 
14. Save & upload information to the cloud
15. Insert campaign into server database

## New_sprints:
0. Track 10-day sprint
1. Find next 10 business days, company custom holiday calendar
2. Find unique phone #'s from the current campaign 
3. Sort by project audit type
4. Create 5 & 10-day sprints based on audit type inventory
5. Split by skill to assign individual campaigns
