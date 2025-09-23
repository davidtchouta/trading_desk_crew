import sys
from crew import MealPlannerCrew

from rich.console import Console
from rich.markdown import Markdown

def main():
    inputs={
        "meal_name": "Chicken Stir Fry",
        "servings": 3,
        "budget": "$25",                           
        "dietary_restrictions": ["no nuts"],       
        "cooking_skill": "intermediate",                
    }
    return MealPlannerCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    print("Welcome to your Meal Analyst")
    print('--------------------------------')
    result = main()
    print("\n\n############################")
    print("## Here is the report")
    print("########################\n\n")
    # print(result)
    # Écrire dans un fichier markdown
    with open("results.md", "w", encoding="utf-8") as f:
        f.write(result.raw)
    console = Console()
    md = Markdown(result.raw)
    console.print(md)