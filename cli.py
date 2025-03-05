import json_manager
import click
import datetime


@click.group()
def cli():
    pass

#CAMBIAR LOS ARGUMENT POR OPTION, VER COMO FUNCIONA CORRECTAMENTE EL --HELP
# Add new Expense
@cli.command()
@click.argument('description', required=True, help="Brief description of spending")
@click.argument('amount', required=True, type=int)#, help="Spent amount")
@click.argument('date',  default=datetime.date.today())#, help="Spending date")
@click.pass_context
def add(ctx, description, amount, date):
    if description.strip() == "":
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



if __name__ == '__main__':
    cli()
