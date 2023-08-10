from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Name, Exercise, Preference, Base

import click

current_user = None

def rainbow_text(text):
    rainbow_colors = ["red", "yellow", "green", "blue", "magenta", "cyan"]
    rainbow_text = ""
    for i, char in enumerate(text):
        color = rainbow_colors[i % len(rainbow_colors)]
        rainbow_text += click.style(char, fg=color)
    return rainbow_text

@click.group()
def cli():
    pass

def test():
    click.echo("TESTING")

@click.command()
@click.option("--confirm", prompt="Are you a new user? [y/n] ", help="Confirms new or current user")
def greeting(confirm):
    """Greeting user to CLI"""
    engine = create_engine('sqlite:///exercise_app.db')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    if confirm == 'y':
        add_name = input("Enter your name: ")
        new_name = Name(name = add_name)
        session.add(new_name)
        session.commit()
        click.echo(f"Hello {add_name}, Welcome to {click.style('SQLIFTS', fg='cyan', bold=True)}!")
        click.echo("Your one place to update all your gym workouts. Let's begin planning your excerises!")
    elif confirm == 'n':
        global current_user
        current_user = input("Enter your name: ")
        click.echo(f"Welcome back {current_user}! Let's continue updating your excerises.")
    
    menu()


@click.command()
@click.option("--workout_name", prompt="Enter the name of workout ", help="The name of the workout")
@click.option("--workout_day", prompt="Enter the day of workout (Monday-Sunday) ", help="The day of workout")
@click.option("--reps", prompt="Enter the number of reps ", help="The number of reps per set")
@click.option("--sets", prompt="Enter the number of sets ", help="The number of sets per workout")
@click.option("--weight", prompt="Enter the lifting weight (in lbs)", help="The weight you are lifting for the workout")
def add(workout_name, workout_day, reps, sets, weight):
    """asks user to input workout(name, reps, sets, weight)"""
    click.echo(f"{rainbow_text('YOUR WORKOUT HAS BEEN SUCCESSFULLY ADDED!!!')}")
    click.echo(f"{click.style('Workout:', bold=True)} {workout_name}")
    click.echo(f"{click.style('Day:', bold=True)} {workout_day}")
    click.echo(f"{click.style('Reps:', bold=True)} {reps}")
    click.echo(f"{click.style('Sets:', bold=True)} {sets}")
    click.echo(f"{click.style('Weight:', bold=True)} {weight}lbs")

    engine = create_engine('sqlite:///excercise_app.db')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    workout = Workout(workout_day=workout_day, workout_name=workout_name, reps=reps, sets=sets, weight=weight)
    session.add(workout)
    session.commit()


def all():
    """Show all available workouts from exercise_app.db"""
    engine = create_engine('sqlite:///exercise_app.db')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Exercise).delete()

    exercises = ['barbell bicep curl', 
    'bench press',
    'rope tricep extension',
    'hamstring extension',
    'cable flys',
    'calf raises',
    'overhead press',
    'squats',
    'bent-over row',
    'deadlift',
    'leg extension',
    'leg press',
    'incline bench press',
    'lat pull down',
    'lateral raises',
    'upright row',
    'shrugs',
    'preacher curl',
    'close grip bench press',
    'pull ups',
    'push ups',
    'hip thrust']
    
    for exercise_name in exercises:
        exercise = Exercise(exercise = exercise_name)
        session.add(exercise)
        session.commit()

    all_exercises = session.query(Exercise).all()
    
    click.echo(f"{click.style('--------------All Workouts--------------', fg='yellow', bold=True)}")
    for exercise in all_exercises:
        click.echo(exercise)


def current():
    """Shows all current workouts added by user"""

    engine = create_engine('sqlite:///exercise_app.db')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    click.echo(current_user)

@click.command()
@click.option("--update", prompt="Enter the name of workout you would like to update", 
help="Name of workout to update")
def update(update):
    """filters a specific workout by name and then allows update"""
    engine = create_engine('sqlite:///workouts.db')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    update_workout = session.query(Workout).filter(Workout.workout_name.ilike(update)).first()
    
    if update_workout:
        click.echo(update_workout)
        update_input = input("What would you like to update? ")
        if update_input.lower() == 'name':
            input_new_name = input("Enter new name for workout: ")
            update_workout.workout_name = input_new_name
            session.commit()
            click.echo(f"{rainbow_text('WORKOUT NAME HAS BEEN SUCCESSFULLY UPDATED!!!')}")
            click.echo(update_workout)

        elif update_input.lower() == 'day':
            input_new_day = input("Enter new day for workout: ")
            update_workout.workout_day = input_new_day
            session.commit()
            click.echo(f"{rainbow_text('WORKOUT DAY HAS BEEN SUCCESSFULLY UPDATED!!!')}")
            click.echo(update_workout)

        elif update_input.lower() in ('reps', 'rep'):
            input_new_reps = input("Enter new reps for workout: ")
            update_workout.reps = input_new_reps
            session.commit()
            click.echo(f"{rainbow_text('WORKOUT REPS HAS BEEN SUCCESSFULLY UPDATED!!!')}")
            click.echo(update_workout)

        elif update_input.lower() in ('sets', 'set'):
            input_new_sets = input("Enter new set for workout: ")
            update_workout.sets = input_new_sets
            session.commit()
            click.echo(f"{rainbow_text('WORKOUT SETS HAS BEEN SUCCESSFULLY UPDATED!!!')}")
            click.echo(update_workout)

        elif update_input.lower() == 'weight':
            input_new_weight = input("Enter new weight for workout: ")
            update_workout.weight = input_new_weight
            session.commit()
            click.echo(f"{rainbow_text('WORKOUT WEIGHT HAS BEEN SUCCESSFULLY UPDATED!!!')}")
            click.echo(update_workout)
        else:
            click.echo(f"{click.style('Not Found!', fg='magenta')}")
    else:
        click.echo(f"{click.style('Workout Not Found!', fg='magenta')}")


@click.command()
@click.option("--search", prompt="Search by name or day", help="searching workouts by day or name")
def search(search):
    """search workouts by name or day from workouts.db"""
    engine = create_engine('sqlite:///workouts.db')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    if search.lower() == 'day':
        search_day = input("What day? ").lower()
        search_day_results = session.query(Workout).filter(Workout.workout_day.ilike(search_day)).all()
        if search_day_results:
            for result in search_day_results:
                click.echo(result)
        else:
            click.echo(f"{click.style(f'No workouts found on {search_day}. Try Again!', fg='magenta')}")

    elif search.lower() == 'name':
        search_name = input("What is the name of the workout? ").lower()
        search_name_results = session.query(Workout).filter(Workout.workout_name.ilike(search_name)).all()
        if search_name_results:
            for result in search_name_results:
                click.echo(result)
        else:
            click.echo(f"{click.style('No workouts found. Try Again!', fg='magenta')}")
    else:
        click.echo(f"{click.style('Invalid search. Try Again!', fg='magenta')}")


@click.command()
@click.option("--delete", prompt="Enter the name of the workout you would like to delete ",
help="deleting workout by name")
def delete(delete):
    """Delete a workout from workouts.db"""
    engine = create_engine('sqlite:///workouts.db')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    delete_workout = session.query(Workout).filter(Workout.workout_name.ilike(delete)).first()
    confirm = click.confirm("Are you sure?")

    if delete_workout:
        if confirm:
            session.delete(delete_workout)
            session.commit()
            click.echo(f"{click.style('Successfully Deleted!', fg='red')}")
        else:
            click.echo(f"{click.style('please return to Commands', fg='magenta')}") 
    else:
        click.echo(f"{click.style('Workout not Found!', fg='magenta')}")


def menu():
    """SQLIFTS interface menu"""
    choice = 0
    while choice !=5:
        click.echo(f"**********{click.style('SQLIFTS Menu', fg='cyan', bold=True)}**********")
        click.echo("1# View all available workouts")
        click.echo("2# View all current workouts")
        click.echo("3# Add workout")
        click.echo("4# Modify current workouts")
        click.echo("5# Delete a workout")
        click.echo("6# Quit")
        
        choice = int(input('Enter your option: '))

        if choice == 1:
            all()
        elif choice == 2:
            current()
        elif choice == 3:
            add()
        elif choice == 4:
            update()
        elif choice == 5:
            delete()
        elif choice == 6:
            exit
            

cli.add_command(greeting)
cli.add_command(add)
cli.add_command(update)
cli.add_command(search)
cli.add_command(delete)

if __name__ == '__main__':
    cli()