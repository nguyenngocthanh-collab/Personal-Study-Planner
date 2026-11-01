import argparse
from datetime import datetime
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
@main.command()
@click.argument("subid")
@click.argument("title")
@click.argument("planned_duration")
def add_plan(subid, title, planned_duration):
    result = planner.add_plan(subid, title, datetime.now(), planned_duration)
    if result:
        print(f"added plan: {title}")


@main.command()
@click.argument("id")
def remove_plan(id):
    r = planner.remove_plan(id)
    if r:
        print("delete successfully")

#summary
@main.command()
@click.argument("id")
@click.argument("status")
def set_status(id, status):
    r = planner.set_status(id, status)
    if r:
        print(f"edited id: {id}")


@main.command()
def tthours():
    total = sum_mod.total_hour()
    print(f"total hours: {total}")


@main.command()
def tthrs_each():
    rows = sum_mod.totalhr_each()
    print(
    f"{'ID':<5} {'NAME':<20} {'MINUTES':<15} {'SESSIONS':<10}"
    )

    for row in rows:
        print(
            f"{row['id']:<5}"
            f"{row['name']:<20}"
            f"{str(row['minutes']):<15}"
            f"{str(row['sessions']):<10}"
        )


@main.command()
def completed():
    res = sum_mod.completed()
    rate = sum_mod.comrate()
    print(f"completed: {res['done']}/{res['total']} ({rate}%)")


@main.command()
def compare():
    rows = sum_mod.compare()
    print(
    f"{'ID':<5} {'NAME':<20} {'PLANNED':<15} {'ACTUAL':<15}"
    )

    for row in rows:
        print(
            f"{row['id']:<5}"
            f"{row['name']:<20}"
            f"{str(row['planned']):<15}"
            f"{str(row['actual']):<15}"
        )

#session
@main.command()
@click.argument("subid")
@click.argument("actual_duration")
@click.argument("plan_id", default=0, required=False)
def mkses(subid, actual_duration, plan_id):
    r = session.make_session(subid, plan_id, actual_duration)
    if r:
        print(f"added session id: {r}")

#search

@main.command()
@click.argument("keyword", required=False)
@click.option("--title", default=None)
@click.option("--subid", default=None)
@click.option("--status", default=None)
@click.option("--date", default=None)
def search_(keyword, title, subid, status, date):
    search_title = title if title is not None else keyword
    rows = search.search_plans(
        title=search_title,
        subject_id=subid,
        status=status,
        planned_date=date
    )
    print(
    f"{'ID':<5} {'SUB_ID':<8} {'TITLE':<25} {'DATE':<12} {'DURATION':<10} {'STATUS':<12}"
    )

    for row in rows:
        print(
            f"{row['id']:<5}"
            f"{row['subject_id']:<8}"
            f"{row['title']:<25}"
            f"{str(row['planned_date']):<12}"
            f"{str(row['planned_duration']):<10}"
            f"{row['status']:<12}"
        )

#track

@main.command()
@click.argument("id")
def done(id):
    r = progress.done_plan(id)
    if r:
        print(f"done id: {id}")


@main.command()
def cnotcomp():
    rows = progress.check_undone()
    print(
    f"{'ID':<5} {'SUB_ID':<8} {'TITLE':<25} {'DATE':<12} {'DURATION':<10} {'STATUS':<12}"
    )

    for row in rows:
        print(
            f"{row['id']:<5}"
            f"{row['subject_id']:<8}"
            f"{row['title']:<25}"
            f"{str(row['planned_date']):<12}"
            f"{str(row['planned_duration']):<10}"
            f"{row['status']:<12}"
        )


@main.command()
def history():
    rows = progress.history()
    print(
    f"{'ID':<5} {'SUB_ID':<8} {'PLAN_ID':<10} {'DATE':<22} {'DURATION':<10}"
    )

    for row in rows:
        print(
            f"{row['id']:<5}"
            f"{row['subject_id']:<8}"
            f"{str(row['plan_id']):<10}"
            f"{str(row['study_date'])[:19]:<22}"
            f"{str(row['actual_duration']):<10}"
        )


if __name__ == "__main__":
    main()