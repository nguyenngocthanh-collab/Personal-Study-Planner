import argparse
import click

from db import schema

from services import subject_manager as sub_mgr
from services import study_planner as planner
from services import progress_tracker as progress
from services import study_session as session
from services import search_filter as search
from services import summary as sum_mod

@click.group()
def main():
    pass
#Thêm môn học
@main.command()
@click.argument("name", type=str)
@click.argument("description", type=str)
def add_sub(name,description):
    result=sub_mgr.add_subject(name,description)
    if result:
        print(f"added {name} description: {description}")

@main.command()
def sbjlist():
    rows=sub_mgr.subject_list()
    print(
    f"{'ID':<5} {'NAME':<20} {'DESCRIPTION':<30} {'STATUS':<15}"
    )

    for row in rows:
        print(
            f"{row['id']:<5}"
            f"{row['name']:<20}"
            f"{str(row['description']):<30}"
            f"{row['status']:<15}"
        )

@main.command()
@click.argument("id")
@click.argument("name")
@click.argument("description")
def sbjedit(id, name, description):
    r=sub_mgr.subject_edit(id, name, description)
    if r:
        print(f"edited id: {id}")


@main.command()
@click.argument("id")
def delsub(id):
    r=sub_mgr.delete_subject(id)
    if r:
        print("delete successfully")

#planner
def add_plan():pass


def remove_plan():pass

#summary
def set_status():pass


def tthours():pass


def tthrs_each():pass


def completed():pass


def compare():pass

#session
def mkses():pass

#search

def search_():pass

#track

def done():pass


def cnotcomp():pass


def history():pass


if __name__ == "__main__":
    main()