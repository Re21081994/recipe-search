from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from collections import Counter
from PIL import Image, ImageTk  # Import PIL for image handling

import matplotlib.pyplot as plt

from recipe import Recipe
from statistics_1 import MostCommonIngredients
from statistics_1 import RarsetIngredients

DATABASE_URL = "mysql+mysqlconnector://root:RRmm2108!@localhost/collect_data"

# Create an SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Function to retrieve recipes based on user input
def search_recipes():
    selected_component = component_entry.get()

    # Perform a select query on the database table to find recipes containing the selected component
    query = session.query(Recipe).filter(Recipe.ingredients.like(f'%{selected_component}%')).limit(20)
    results = query.all()

    # Display a message if no results are found
    if not results:
        messagebox.showinfo("No Results", "No recipes found containing the specified ingredient.")
        return

    # Display results in the GUI
    result_text.delete(1.0, END)
    for result in results:
        title = result.title.replace('"', '').replace("'", '')  # Remove quotes from title
        ingredients = result.ingredients.replace('"', '').replace("'", '')  # Remove quotes from ingredients
        directions = result.directions.replace('"', '').replace("'", '')  # Remove quotes from directions

        # Highlight recipe title
        result_text.insert(END, f"Recipe Name: {title}\n", "title")
        result_text.tag_configure("title", font=("Helvetica", 12, "bold"))

        result_text.insert(END, f"Ingredients: {ingredients}\n")
        result_text.insert(END, f"Directions: {directions}\n")
        result_text.insert(END, "\n\n")  # Add space between each recipe

# Function to calculate the most common ingredients
# Function to calculate the most common ingredients
def plot_most_common_ingredients():
    most_common_ingredients = session.query(MostCommonIngredients.ingredient, MostCommonIngredients.count).all()

    # Extract ingredient names and counts
    ingredients = [ingredient for ingredient, _ in most_common_ingredients]
    counts = [count for _, count in most_common_ingredients]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(ingredients, counts, color='skyblue')
    plt.ylabel('Count')
    plt.xlabel('Ingredient')
    plt.title('Most Common Ingredients')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

# Function to calculate the rarest ingredients
def plot_rarest_ingredients():
    rarest_ingredients = session.query(RarsetIngredients.ingredient, RarsetIngredients.count).all()

    # Extract ingredient names and counts
    ingredients = [ingredient for ingredient, _ in rarest_ingredients]
    counts = [count for _, count in rarest_ingredients]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(ingredients, counts, color='salmon')
    plt.ylabel('Count')
    plt.xlabel('Ingredient')
    plt.title('Rarest Ingredients')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()


# Create Tkinter application
root = Tk()
root.title("Recipe Search")

# Load background image
background_image = Image.open("coock.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image
background_label = Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Main frame with background color and opacity
main_frame = Frame(root, bg='white', bd=5)
main_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
# main_frame.place(relx=0.5, rely=0.5, anchor='center')

# Entry field to input recipe component
component_label = Label(main_frame, text="Enter Component:", font=("Helvetica", 12), bg='white')
component_label.grid(row=0, column=0, padx=5, pady=5)
component_entry = Entry(main_frame, font=("Helvetica", 12))
component_entry.grid(row=0, column=1, padx=5, pady=5)
# component_entry.place(relx=0.5, rely=0.5, anchor='center')

# Button to trigger search
search_button = Button(main_frame, text="Search", font=("Helvetica", 12), command=search_recipes, bg='lightgreen')
search_button.grid(row=0, column=2, padx=5, pady=5)
# search_button.place(relx=0.5, rely=0.5, anchor='center')
# Button to plot most common ingredients
plot_most_common_button = Button(root, text="Plot Most Common Ingredients", font=("Helvetica", 12), command=plot_most_common_ingredients, bg='lightblue')
plot_most_common_button.place(relx=0.1, rely=0.85, relwidth=0.35, relheight=0.05)

# Button to plot rarest ingredients
plot_rarest_button = Button(root, text="Plot Rarest Ingredients", font=("Helvetica", 12), command=plot_rarest_ingredients, bg='lightpink')
plot_rarest_button.place(relx=0.55, rely=0.85, relwidth=0.35, relheight=0.05)

# Text widget to display search results
result_frame = Frame(root, bg='white', bd=10)
result_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.5, anchor='n')

result_text = Text(result_frame, font=("Helvetica", 12), wrap=WORD)
result_text.pack(expand=True, fill=BOTH)

root.mainloop()
