import json_manager
import click
import datetime
from tabulate import tabulate


@click.group()
def cli():
    pass


# Add new Expense
@cli.command()
@click.argument('description', required=True)
@click.argument('amount', required=True, type=int)
@click.option('--date',  default=datetime.date.today(), help="Spending date")
@click.pass_context
def add(ctx, description, amount, date):
    """
        Añade los gastos
    """
    if not description.strip():
        ctx.fail("Task description is required")
    
    if not amount:
        ctx.fail("The amount spent is required")
    
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
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


# Update Expense by id
@cli.command()
@click.argument('id', type=str) #ver por que puse tipo id str y no int
@click.argument('description', type=str)
@click.argument('amount', type=int)
@click.option('--date', help="Modify the spending date")
@click.pass_context
def update(ctx, id, description, amount, date):
    """
    Actualiza los datos de los gastos

    """
    if not description.strip():
        ctx.fail("Task description is required")

    try:
        expense_id = int(id)
    except ValueError:
        ctx.fail("A numeric ID is required, try again")

    data = json_manager.read_json()
    expense_found = False

    for expense in data:
        if expense["id"] == expense_id:
            if description is not None:
                expense["description"] = description
            if amount is not None:
                expense["amount"] = amount
            if date is not None:
                 try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                    expense["date"] = date
                 except ValueError:
                    ctx.fail("Invalid date format! Please use YYYY-MM-DD.")
            expense_found = True
            break

    if expense_found:
        json_manager.add_expenses(data)
        click.echo(f"Expense with id {expense_id} has been updated")
    
    if not expense_found:
        click.echo(f"Expense with id {expense_id} not found")

# Delete task by id
@cli.command()
@click.argument("id", type=str)
@click.pass_context
def delete(ctx, id):
    """
    Borra un gasto a travez de su id
    """
    try:
        expense_id = int(id)
    except ValueError:
        ctx.fail("A numeric ID is required, try again")
    
    data = json_manager.read_json()
    expense = next((expense for expense in data if expense["id"] == expense_id), None)

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
        Muestra en forma de tabla un resumen de los gastos guardados
    """
    try:
        data = json_manager.read_json()
    except ValueError:
        ctx.fail("no hay datos guardados")

    table = [[expense["id"],expense["description"],expense["date"], expense["amount"]] for expense in data]

    headers = ["ID", "Date", "Description", "Amount"]

    click.echo(tabulate(table, headers=headers, tablefmt="plain"))


if __name__ == '__main__':
    cli()
