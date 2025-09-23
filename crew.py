from pydantic import BaseModel, Field
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from dotenv import load_dotenv
load_dotenv()


from crewai import LLM

# Configuration pour Claude via AWS Bedrock
# llm = LLM(
#     # model=os.environ['MODEL'],
#     model=os.getenv('MODEL'),
#     # max_tokens=int(os.getenv('MAX_TOKENS')),
#     max_tokens=2000,
#     # Optionnel : ajoutez vos credentials AWS
#     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), 
#     aws_region_name=os.getenv('REGION')
# )

llm = LLM(
    # model="ollama/deepseek-r1:latest",
    model="ollama/qwen2.5:7b",
    base_url="http://localhost:11434"
)


class GroceryItem(BaseModel):
    """Individual grocery item"""
    name: str = Field(description="Name of the grocery item")
    quantity: str = Field(description="Quantity needed (for example, '2 lbs', '1 gallon')")
    estimated_price: str = Field(description="Estimated price (for example, '$3-5')")
    category: str = Field(description="Store section (for example, 'Produce', 'Dairy')")

class MealPlan(BaseModel):
    """Simple meal plan"""
    meal_name: str = Field(description="Name of the meal")
    difficulty_level: str = Field(description="'Easy', 'Medium', 'Hard'")
    servings: int = Field(description="Number of people it serves")
    researched_ingredients: List[str] = Field(description="Ingredients found through research")


class ShoppingCategory(BaseModel):
    """Store section with items"""
    section_name: str = Field(description="Store section (for example, 'Produce', 'Dairy')")
    items: List[GroceryItem] = Field(description="Items in this section")
    estimated_total: str = Field(description="Estimated cost for this section")


class GroceryShoppingPlan(BaseModel):
    """Complete simplified shopping plan"""
    total_budget: str = Field(description="Total planned budget")
    meal_plans: List[MealPlan] = Field(description="Planned meals")
    shopping_sections: List[ShoppingCategory] = Field(description="Organized by store sections")
    shopping_tips: List[str] = Field(description="Money-saving and efficiency tips")



@CrewBase
class MealPlannerCrew():
    """Search and Summary Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def meal_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['meal_planner'],
                tools=[SerperDevTool()],
            llm=llm,
            allow_delegation=False,
                verbose=True
        )
    
    @task
    def meal_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['meal_planning_task'],
            agent=self.meal_planner(),
            output_pydantic=MealPlan,
            output_file='meals.json'
        )
    
    @agent
    def shopping_organizer(self) -> Agent:
        return Agent(
            config=self.agents_config['shopping_organizer'],
            llm=llm,
            allow_delegation=False,
                verbose=True
        )
    
    @task
    def shopping_organizer_task(self) -> Task:
        return Task(
            config=self.tasks_config['shopping_organizer_task'],
            agent=self.shopping_organizer(),
            depends_on=[self.meal_planning_task()],
            output_pydantic=GroceryShoppingPlan,
            output_file='shopping_list.json'
        )

    @agent
    def budget_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_advisor'],
                tools=[SerperDevTool()],
            llm=llm,
            allow_delegation=False,
                verbose=True
        )
    
    @task
    def budget_advisor_task(self) -> Task:
        return Task(
            config=self.tasks_config['budget_advisor_task'],
            agent=self.budget_advisor(),
            depends_on=[self.meal_planning_task(),self.shopping_organizer_task()],
            output_file='shopping_guide.md'
        )
    
    @agent
    def leftover_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['leftover_manager'],
            llm=llm,
            allow_delegation=False,
                verbose=True
        )
    @task
    def leftover_task(self) -> Task:
        return Task(
            config=self.tasks_config['leftover_task'],
            agent=self.leftover_manager()
        )

    @agent
    def summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_agent'],
            llm=llm,
            allow_delegation=False,
                verbose=True
        )
    
    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['summary_task'],
            agent=self.summary_agent(),
            depends_on=[self.meal_planning_task(),self.shopping_organizer_task(),self.budget_advisor_task(),self.leftover_task()],
            verbose=True
        )

    
    @crew
    def crew(self) -> Crew:
        """Create a Meal planner and Shopping Organizer Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )