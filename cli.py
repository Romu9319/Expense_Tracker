import json_manager
import click
import datetime
from datetime import date
from tabulate import tabulate


@click.group()
def cli():
    pass


@cli.command()
@click.option('--description', required=True, help="Add a description about your expense")
@click.option('--amount', required=True, type=float, help="Enter the amount spent")
@click.option('--date',  default=datetime.date.today(), help="Spending date")
@click.pass_context
def add(ctx, description, amount, date):
    """
    Add a description of the expenses and the amount spent
    """
    if not description.strip():
        ctx.fail("Task description is required")
    
    if not amount:
        ctx.fail("The amount spent is required")
    
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        ctx.fail("Invalid date format! Please use YYYY-MM-DD.")

    data = json_manager.read_json()
    expense_id = max((expense["id"] for expense in data), default=0) + 1
    new_expense = {
        "id": expense_id,
        "description": description,
        "amount": amount,
        "date": date
    }

    data.append(new_expense)
    json_manager.add_expenses(data)
    click.echo(f"New expense with id {expense_id} has been added")


@cli.command()
@click.option('--id', required=True, type=int, help="Indique el id del gasto")
@click.option('--description', required=False, type=str, help="Add a description about your expense")
@click.option('--amount',required=False, type=float, help="Enter the amount spent")
@click.option('--date', help="Modify the spending date")
@click.pass_context
def update(ctx, id, description, amount, date):
    """
    A way to update the description of the expenses and their quantity 
    """
    if description is not None and not description.strip():
        ctx.fail("Task description is required")    

    data = json_manager.read_json()
    expense_found = False

    for expense in data:
        if expense["id"] == id:
            if description:
                expense["description"] = description
            if amount:
                expense["amount"] = amount
            if date:
                 try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                    expense["date"] = date
                 except ValueError:
                    ctx.fail("Invalid date format! Please use YYYY-MM-DD.")
            expense_found = True
            break

    if expense_found:
        json_manager.add_expenses(data)
        click.echo(f"Expense with id {id} has been updated")
    
    if not expense_found:
        click.echo(f"Expense with id {id} not found")

# Delete task by id
@cli.command()
@click.option("--id", required=True, type=int)
@click.pass_context
def delete(ctx, id):
    """
    Delete the record of an expense through its id
    """    
    data = json_manager.read_json()
    expense = next((expense for expense in data if expense["id"] == id), None)

    if not expense:
        click.echo(f"Expense with id {id} not found")
    else: 
        data.remove(expense)
        json_manager.add_expenses(data)
        click.echo(f"Expense with id {id} has been deleted")

@cli.command() #### APLICAR CONTROL DE ERRORES
@click.pass_context
def list_expenses(ctx):
    """
    Displays a table with the summary of expenses
    """
    try:
        data = json_manager.read_json()
    except ValueError:
        ctx.fail("There are no recorded expenses")

    table = [[expense["id"],expense["description"],expense["date"], expense["amount"]] for expense in data]

    headers = ["ID", "Date", "Description", "Amount"]

    click.echo(tabulate(table, headers=headers, tablefmt="plain"))

@cli.command()
@click.pass_context
def summary(ctx):
    """
    Shows a summary of total expenses
    """
    try:
        data = json_manager.read_json()
    except ValueError:
        ctx.fail("There are no recorded expenses")

    summary_expenses  = sum(expense["amount"] for expense in data)

    if not summary_expenses:
        click.echo("There are no recorded expenses")
    else:
        click.echo(f"Total of expenses: ${summary_expenses:.2f}")


@cli.command()
@click.argument("month", required=True, type=int)
@click.pass_context
def month(ctx, month):
    """
    Filter expenses per month
    """
    if month < 1 or month > 12:
        ctx.fail("You must select a month between 1 and 12 ")
    
    
    try:
        data = json_manager.read_json()
        if not isinstance(data, list):
            ctx.fail("Expenses file could be in incorrect or damaged format.")
        if not data:
            ctx.fail("There are no recorded expenses.")
    except (ValueError, FileNotFoundError) as e:
        ctx.fail(f"Error reading data: {str(e)}")

    
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    
    try:
        expenses_month = sum(
            expense["amount"] 
            for expense in data 
            if expense["date"] and expense["amount"] and isinstance(expense["amount"], (int, float))
            and datetime.datetime.strptime(expense["date"], "%Y-%m-%d").month == month
        )
    except (KeyError, ValueError, TypeError) as e:
        ctx.fail(f"Error processing data: {str(e)}")


    if not expenses_month:
        click.echo(f"There are not recorded expenses for {months[month - 1]}")
    else:
        click.echo(f"Total of expenses in {months[month - 1]}: ${expenses_month:.2f}")


if __name__ == '__main__':
    cli()

