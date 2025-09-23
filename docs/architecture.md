# Architecture

## Overview
The **Meal Grocery Planner** system is built on a CrewAI structure.  
It orchestrates several specialized agents, each responsible for a different step of the workflow. The Crew coordinates execution sequentially to produce structured, actionable outputs.

---

## Workflow
1. **Meal Planner Agent** creates the meal plan (meals, servings, ingredients).  
2. **Shopping Organizer Agent** transforms the plan into a grocery list, organized by store sections.  
3. **Budget Advisor Agent** validates the list against a budget and provides recommendations.  
4. **Leftover Agent** suggests meal adaptations using leftovers to reduce waste.  
5. **Summary Agent** compiles all results into a final report.  

---

## Diagram
The following diagram illustrates the architecture and workflow:

![Architecture Diagram](screenshots/archi_agent_meal_manager.png)

- **Left** → Multiple Agents (Meal Planner, Shopping Organizer, Budget Advisor, Leftover, Summary).  
- **Center** → CrewAI (orchestration and sequential process).  
- **Right** → Final Outputs (`meals.json`, `shopping_list.json`, `shopping_guide.md`, consolidated summary).