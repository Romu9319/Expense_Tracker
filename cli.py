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
@click.argument('amount', required=True, type=float)
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
@click.option('--id', type=int, help="Indique el id del gasto")
@click.option('--description', required=False, type=str)
@click.option('--amount',required=False, type=float)
@click.option('--date', help="Modify the spending date")
@click.pass_context
def update(ctx, id, description, amount, date):
    """
    Actualiza los datos de los gastos

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
@click.argument("id", type=int)
@click.pass_context
def delete(ctx, id):
    """
    Borra un gasto a travez de su id
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
        Muestra en forma de tabla un resumen de los gastos guardados
    """
    try:
        data = json_manager.read_json()
    except ValueError:
        ctx.fail("no hay datos guardados")

    table = [[expense["id"],expense["description"],expense["date"], expense["amount"]] for expense in data]

    headers = ["ID", "Date", "Description", "Amount"]

    click.echo(tabulate(table, headers=headers, tablefmt="plain"))

@cli.command()
@click.pass_context
def summary(ctx):
    """
    Muestra un resumen del total de gastos
    """
    try:
        data = json_manager.read_json()
    except ValueError:
        ctx.fail("no hay datos guardados")

    summary_expenses  = sum(expense["amount"] for expense in data)

    if not summary_expenses:
        click.echo("No tiene gastos registrados")
    else:
        click.echo(f"Total of expenses: ${summary_expenses:.2f}")


from datetime import datetime
@cli.command()
@click.option("--month", required=True, type=int, help="Indicar el mes por el cual se filtraran los gastos")
@click.pass_context
def month(ctx, month):
    """
    Filtrara los datos por mes
    """
    try:
        data = json_manager.read_json()
    except ValueError:
        ctx.fail("no hay datos guardados")

    if month < 1 or month > 12:
        ctx.fail("el mes debe estar entre 1 y 12")

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    #dates = [(dates for dates in data)]
    expenses_month = sum(expense["amount"] for expense in data if datetime.strptime(expense["date"], "%Y-%m-%d").month == month)

    if not expenses_month:
        click.echo("No tiene gastos registrados")
    else:
        click.echo(f"Total of expenses in {months[month - 1]}: ${expenses_month:.2f}")




if __name__ == '__main__':
    cli()

